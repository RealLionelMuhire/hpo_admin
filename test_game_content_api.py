#!/usr/bin/env python3
"""
Test script for GameContent GET API endpoints
Run this script to test the available GameContent API endpoints
"""

import requests
import json
from urllib.parse import urljoin

# Base URL - update this to match your server
BASE_URL = "http://localhost:8000"  # Change to your server URL

def test_get_all_content():
    """Test getting all game content"""
    print("🔍 Testing: Get All Game Content")
    url = urljoin(BASE_URL, "/api/game-content/")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: Found {data.get('count', 0)} content items")
            if data.get('content'):
                print(f"   First item: {data['content'][0]['title']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    print()

def test_get_filtered_content():
    """Test getting filtered game content"""
    print("🔍 Testing: Get Filtered Game Content")
    url = urljoin(BASE_URL, "/api/game-content/")
    params = {
        'language': 'english',
        'status': 'published'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: Found {data.get('count', 0)} English content items")
            print(f"   Filters applied: {data.get('filters_applied')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    print()

def test_get_content_detail(content_id=1):
    """Test getting specific content detail"""
    print(f"🔍 Testing: Get Content Detail (ID: {content_id})")
    url = urljoin(BASE_URL, f"/api/game-content/{content_id}/")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            content = data.get('content', {})
            print(f"✅ Success: Retrieved '{content.get('title', 'Unknown')}'")
            print(f"   View count: {content.get('view_count', 0)}")
            print(f"   Subtopics: {content.get('all_subtopics', [])}")
        elif response.status_code == 404:
            print(f"❌ Content with ID {content_id} not found")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    print()

def test_get_content_by_language_age():
    """Test getting content by language and age group"""
    print("🔍 Testing: Get Content by Language and Age Group")
    url = urljoin(BASE_URL, "/api/game-content/english/15-19/")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: Found {data.get('count', 0)} items for English 15-19 age group")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    print()

def main():
    print("🚀 GameContent API Testing Script")
    print("=" * 50)
    
    # Test all endpoints
    test_get_all_content()
    test_get_filtered_content()
    test_get_content_detail(1)
    test_get_content_by_language_age()
    
    print("📋 Available GET Endpoints:")
    print("  1. GET /api/game-content/ - Get all content (with filtering)")
    print("  2. GET /api/game-content/{id}/ - Get specific content detail")
    print("  3. GET /api/game-content/{language}/{age_group}/ - Get by language/age")
    print()
    print("📝 Available Filters for endpoint 1:")
    print("  - language: english, french, kinyarwanda")
    print("  - age_group: 6-10, 11-14, 15-19, 20+")
    print("  - topic: (partial text match)")
    print("  - subtopic: (partial text match)")
    print("  - content_type: question, fact, story, challenge")
    print("  - status: draft, published, archived")

if __name__ == "__main__":
    main()
