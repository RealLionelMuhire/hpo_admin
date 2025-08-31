#!/usr/bin/env python3
"""
Test script for the updated Game Creation API
Tests the new format where only player IDs are required
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_game_new_format():
    """Test creating a game with the new player ID format"""
    print("🎮 Testing: Create Game with Player IDs")
    url = f"{BASE_URL}/api/games/create/"
    
    # New format - just player IDs
    payload = {
        "participant_count": 2,
        "players": [1, 2]  # Just player IDs
    }
    
    try:
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(payload))
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success: Game created successfully")
            print(f"   Match ID: {data['game']['match_id']}")
            print(f"   Participants: {len(data['game']['participants'])}")
            for p in data['game']['participants']:
                print(f"     - Player {p['player_id']}: {p['username']} ({p['player_name']}) - Team {p['team']}")
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error message: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Raw response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    print()

def test_create_game_invalid_player_id():
    """Test creating a game with non-existent player ID"""
    print("🔍 Testing: Create Game with Invalid Player ID")
    url = f"{BASE_URL}/api/games/create/"
    
    payload = {
        "participant_count": 2,
        "players": [1, 999]  # Player 999 probably doesn't exist
    }
    
    try:
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(payload))
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Expected Error: Invalid player ID properly handled")
            print(f"   Error message: {data.get('error')}")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    print()

def main():
    print("🚀 Game Creation API Testing (New Format)")
    print("=" * 50)
    
    print("📝 New API Format:")
    print("  POST /api/games/create/")
    print("  {")
    print("    \"participant_count\": 2,")
    print("    \"players\": [1, 2]  // Just player IDs")
    print("  }")
    print()
    
    # Test valid creation
    test_create_game_new_format()
    
    # Test invalid player ID
    test_create_game_invalid_player_id()
    
    print("📋 Key Changes:")
    print("  ✅ Players array now contains only player IDs")
    print("  ✅ No need to send username/player_name")
    print("  ✅ Player info is fetched from database using ID")
    print("  ✅ Response includes player_id in participants")
    print("  ✅ Proper error handling for non-existent players")

if __name__ == "__main__":
    main()
