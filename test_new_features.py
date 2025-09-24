#!/usr/bin/env python3
"""
Test script to verify:
1. The /test endpoint returns HTTP 200
2. The new age group choice (10-24) is available in GameContent model
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint():
    """Test the /test endpoint"""
    print("🧪 Testing /test endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/test/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Test endpoint working correctly!")
            return True
        else:
            print("❌ Test endpoint failed!")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_age_group_choices():
    """Test that the age group choices include the new 10-24 option"""
    print("\n🧪 Testing age group choices...")
    
    try:
        # Import here to avoid issues if Django isn't properly set up
        import sys
        import os
        sys.path.append('/home/leo/hpo/hpo_django/hpo_admin')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hpo.settings')
        
        import django
        django.setup()
        
        from hpo_app.models import GameContent
        
        age_choices = GameContent.AGE_GROUP_CHOICES
        print(f"Available age group choices: {age_choices}")
        
        # Check if '10-24' is in the choices
        age_group_values = [choice[0] for choice in age_choices]
        if '10-24' in age_group_values:
            print("✅ New age group '10-24' is available!")
            return True
        else:
            print("❌ New age group '10-24' not found!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing age group choices: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting tests...\n")
    
    test1_passed = test_endpoint()
    test2_passed = test_age_group_choices()
    
    print("\n📊 Test Results:")
    print(f"Test endpoint: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Age group choices: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed!")

if __name__ == "__main__":
    main()
