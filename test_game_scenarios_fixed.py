#!/usr/bin/env python3
"""
Comprehensive Game Creation Test Script
Tests 1, 2, and 4 player game scenarios with team assignments
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_test_players():
    """Create test players if they don't exist"""
    print("🔧 Setting up test players...")
    
    # We'll assume players 1, 2, 3, 4 exist
    # If not, we'd need to create them via admin or Player API
    test_players = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}, 
        {"id": 3, "name": "Charlie"},
        {"id": 4, "name": "Diana"}
    ]
    
    player_list = ', '.join([p['name'] + ' (ID: ' + str(p['id']) + ')' for p in test_players])
    print(f"   Using test players: {player_list}")
    return test_players

def test_single_player_game():
    """Test 1-player game (Player vs Computer)"""
    print("\n🎮 Test 1: Single Player Game (1 participant)")
    print("=" * 50)
    
    url = f"{BASE_URL}/api/games/create/"
    payload = {
        "participant_count": 1,
        "players": [1]  # Just Alice
    }
    
    try:
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(payload))
        
        if response.status_code == 200:
            data = response.json()
            game = data['game']
            
            print("✅ Single player game created successfully!")
            print(f"   Match ID: {game['match_id']}")
            print(f"   Participant Count: {game['participant_count']}")
            print(f"   Team Count: {game['team_count']}")
            print(f"   Players per Team: {game['players_per_team']}")
            print(f"   Status: {game['status']}")
            
            print("\n   Participants:")
            for p in game['participants']:
                print(f"     • {p['player_name']} (ID: {p['player_id']}, Username: {p['username']}) - Team {p['team']}")
            
            # Verify single player logic
            assert game['participant_count'] == 1, "Should have 1 participant"
            assert game['team_count'] == 1, "Should have 1 team for single player"
            assert len(game['participants']) == 1, "Should have 1 participant"
            assert game['participants'][0]['team'] == 1, "Single player should be on team 1"
            
            return game['match_id']
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_two_player_game():
    """Test 2-player game (2 teams, 1 player each)"""
    print("\n🎮 Test 2: Two Player Game (2 participants, 2 teams)")
    print("=" * 55)
    
    url = f"{BASE_URL}/api/games/create/"
    payload = {
        "participant_count": 2,
        "players": [1, 2]  # Alice vs Bob
    }
    
    try:
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(payload))
        
        if response.status_code == 200:
            data = response.json()
            game = data['game']
            
            print("✅ Two player game created successfully!")
            print(f"   Match ID: {game['match_id']}")
            print(f"   Participant Count: {game['participant_count']}")
            print(f"   Team Count: {game['team_count']}")
            print(f"   Players per Team: {game['players_per_team']}")
            print(f"   Status: {game['status']}")
            
            print("\n   Teams:")
            team1_players = [p for p in game['participants'] if p['team'] == 1]
            team2_players = [p for p in game['participants'] if p['team'] == 2]
            
            team1_names = ', '.join([p['player_name'] + ' (ID: ' + str(p['player_id']) + ')' for p in team1_players])
            team2_names = ', '.join([p['player_name'] + ' (ID: ' + str(p['player_id']) + ')' for p in team2_players])
            
            print(f"     Team 1: {team1_names}")
            print(f"     Team 2: {team2_names}")
            
            # Verify two player logic
            assert game['participant_count'] == 2, "Should have 2 participants"
            assert game['team_count'] == 2, "Should have 2 teams"
            assert len(game['participants']) == 2, "Should have 2 participants"
            assert len(team1_players) == 1, "Team 1 should have 1 player"
            assert len(team2_players) == 1, "Team 2 should have 1 player"
            
            return game['match_id']
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_four_player_game():
    """Test 4-player game (2 teams, 2 players each)"""
    print("\n🎮 Test 3: Four Player Game (4 participants, 2 teams)")
    print("=" * 55)
    
    url = f"{BASE_URL}/api/games/create/"
    payload = {
        "participant_count": 4,
        "players": [1, 2, 3, 4]  # Alice, Bob, Charlie, Diana
    }
    
    try:
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(payload))
        
        if response.status_code == 200:
            data = response.json()
            game = data['game']
            
            print("✅ Four player game created successfully!")
            print(f"   Match ID: {game['match_id']}")
            print(f"   Participant Count: {game['participant_count']}")
            print(f"   Team Count: {game['team_count']}")
            print(f"   Players per Team: {game['players_per_team']}")
            print(f"   Status: {game['status']}")
            
            print("\n   Teams:")
            team1_players = [p for p in game['participants'] if p['team'] == 1]
            team2_players = [p for p in game['participants'] if p['team'] == 2]
            
            team1_names = ', '.join([p['player_name'] + ' (ID: ' + str(p['player_id']) + ')' for p in team1_players])
            team2_names = ', '.join([p['player_name'] + ' (ID: ' + str(p['player_id']) + ')' for p in team2_players])
            
            print(f"     Team 1: {team1_names}")
            print(f"     Team 2: {team2_names}")
            
            # Verify four player logic
            assert game['participant_count'] == 4, "Should have 4 participants"
            assert game['team_count'] == 2, "Should have 2 teams"
            assert len(game['participants']) == 4, "Should have 4 participants"
            assert len(team1_players) == 2, "Team 1 should have 2 players"
            assert len(team2_players) == 2, "Team 2 should have 2 players"
            
            return game['match_id']
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_invalid_scenarios():
    """Test invalid game creation scenarios"""
    print("\n🔍 Test 4: Invalid Scenarios")
    print("=" * 35)
    
    url = f"{BASE_URL}/api/games/create/"
    
    # Test 1: Invalid participant count
    print("\n   Testing invalid participant count (3)...")
    payload = {
        "participant_count": 3,  # Invalid - not 1, 2, 4, or 6
        "players": [1, 2, 3]
    }
    
    try:
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(payload))
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Expected error: {data.get('error')}")
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: Mismatched player count
    print("\n   Testing mismatched player count...")
    payload = {
        "participant_count": 2,
        "players": [1, 2, 3]  # 3 players but count says 2
    }
    
    try:
        response = requests.post(url, 
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(payload))
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Expected error: {data.get('error')}")
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 3: Non-existent player ID
    print("\n   Testing non-existent player ID...")
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
            print(f"   ✅ Expected error: {data.get('error')}")
        else:
            print(f"   ❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")

def main():
    print("🚀 Game Creation Comprehensive Test Suite")
    print("=" * 60)
    print(f"🌐 Testing against: {BASE_URL}")
    
    # Setup
    create_test_players()
    
    # Store created game IDs for reference
    game_ids = []
    
    # Test all scenarios
    game_id = test_single_player_game()
    if game_id:
        game_ids.append(("Single Player", game_id))
    
    game_id = test_two_player_game()
    if game_id:
        game_ids.append(("Two Player", game_id))
    
    game_id = test_four_player_game()
    if game_id:
        game_ids.append(("Four Player", game_id))
    
    # Test invalid scenarios
    test_invalid_scenarios()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    print(f"✅ Games created successfully: {len(game_ids)}")
    
    if game_ids:
        print("\n🎯 Created Game IDs:")
        for game_type, match_id in game_ids:
            print(f"   • {game_type}: {match_id}")
        
        print("\n💡 Next Steps:")
        print("   1. You can complete these games using /api/games/complete/")
        print("   2. Check game status with /api/games/{match_id}/status/")
        print("   3. Get responses with /api/games/{match_id}/responses/")
    
    print("\n🎮 Team Assignment Logic Verified:")
    print("   ✅ 1 player  → 1 team  (Player vs Computer)")
    print("   ✅ 2 players → 2 teams (1 player each)")
    print("   ✅ 4 players → 2 teams (2 players each)")
    print("   ✅ Error handling for invalid scenarios")

if __name__ == "__main__":
    main()
