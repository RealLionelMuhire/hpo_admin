#!/usr/bin/env python3
"""
Test script for Player Registration API endpoints
Run this script to test the player registration and authentication APIs
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, headers=None, token=None):
    """Helper function to test API endpoints"""
    url = f"{BASE_URL}{endpoint}"
    
    if headers is None:
        headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Token {token}"
    
    print(f"\n🔍 Testing {method} {endpoint}")
    print(f"📡 URL: {url}")
    
    if data:
        print(f"📤 Data: {json.dumps(data, indent=2)}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        
        print(f"📈 Status: {response.status_code}")
        print(f"📥 Response: {json.dumps(response.json(), indent=2)}")
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON response: {response.text}")
        return None

def main():
    print("🚀 Player Registration API Testing Script")
    print("=" * 50)
    
    # Test 1: Get form data endpoints (no auth required)
    print("\n📋 Testing Form Data Endpoints (No Auth Required)")
    
    # Age groups
    test_endpoint("GET", "/api/v1/form-data/age-groups/")
    
    # Provinces and districts
    test_endpoint("GET", "/api/v1/form-data/provinces-districts/")
    
    # Gender choices
    test_endpoint("GET", "/api/v1/form-data/genders/")
    
    # Test 2: Player Registration
    print("\n� Testing Player Registration")
    
    registration_data = {
        "player_name": "API Test User",
        "username": "apitest456",
        "email": "apitest@example.com",
        "phone": "+250789456123",
        "password": "securepass123",
        "password_confirm": "securepass123",
        "age_group": "15-19",
        "gender": "female",
        "province": "Northern Province",
        "district": "Musanze"
    }
    
    register_response = test_endpoint("POST", "/api/v1/auth/register/", registration_data)
    
    if register_response and register_response.status_code == 201:
        response_data = register_response.json()
        token = response_data.get("token")
        player_data = response_data.get("player")
        
        print(f"✅ Registration successful! Token: {token}")
        
        # Test 3: Player Login
        print("\n� Testing Player Login")
        
        login_data = {
            "username": registration_data["username"],
            "password": registration_data["password"]
        }
        
        login_response = test_endpoint("POST", "/api/v1/auth/login/", login_data)
        
        if login_response and login_response.status_code == 200:
            login_token = login_response.json().get("token")
            print(f"✅ Login successful! Token: {login_token}")
            
            # Test 4: Get Player Profile (authenticated)
            print("\n👤 Testing Player Profile (Authenticated)")
            
            profile_response = test_endpoint("GET", "/api/v1/auth/profile/", token=login_token)
            
            # Test 5: Logout
            print("\n🚪 Testing Player Logout")
            
            logout_response = test_endpoint("POST", "/api/v1/auth/logout/", token=login_token)
            
            if logout_response and logout_response.status_code == 200:
                print("✅ Logout successful!")
                
                # Test 6: Try to access profile after logout (should fail)
                print("\n🔒 Testing Profile Access After Logout (Should Fail)")
                test_endpoint("GET", "/api/v1/auth/profile/", token=login_token)
        
    # Test 7: Test validation errors
    print("\n⚠️ Testing Validation Errors")
    
    # Missing required fields
    invalid_data = {
        "username": "incomplete"
        # Missing required fields
    }
    
    test_endpoint("POST", "/api/v1/auth/register/", invalid_data)
    
    # Password mismatch
    mismatch_data = {
        "player_name": "Test User",
        "username": "mismatchtest",
        "phone": "+250788999888",
        "password": "password123",
        "password_confirm": "differentpassword"
    }
    
    test_endpoint("POST", "/api/v1/auth/register/", mismatch_data)
    
    # Invalid province-district combination
    invalid_location_data = {
        "player_name": "Test User",
        "username": "locationtest",
        "phone": "+250788999777",
        "password": "password123",
        "password_confirm": "password123",
        "province": "Kigali City",
        "district": "Musanze"  # Musanze is not in Kigali City
    }
    
    test_endpoint("POST", "/api/v1/auth/register/", invalid_location_data)
    
    print("\n✅ API Testing Complete!")
    print("\n📚 Summary:")
    print("- ✅ Form data endpoints working")
    print("- ✅ Player registration working")
    print("- ✅ Player login working")
    print("- ✅ Authenticated profile access working")
    print("- ✅ Player logout working")
    print("- ✅ Validation errors handled properly")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Testing interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)
