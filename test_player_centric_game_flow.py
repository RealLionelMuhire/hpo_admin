#!/usr/bin/env python3
"""
Test script for the new player-centric game workflow
Tests the complete flow from game creation to answer submission
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"🎮 {title}")
    print(f"{'='*60}")

def print_step(step_num, description):
    print(f"\n📍 Step {step_num}: {description}")
    print("-" * 50)

def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request and return response"""
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, params=params, headers=headers)
        
        print(f"🌐 {method} {endpoint}")
        if data:
            print(f"📤 Request: {json.dumps(data, indent=2)}")
        if params:
            print(f"📤 Params: {params}")
        
        print(f"📊 Status: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            response_data = response.json()
            print(f"📥 Response: {json.dumps(response_data, indent=2)}")
            return response_data
        else:
            print(f"📥 Response: {response.text}")
            return {"error": "Non-JSON response", "content": response.text}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return {"error": str(e)}

def register_test_players():
    """Register test players for the game"""
    
    print_section("PLAYER REGISTRATION")
    
    # Generate unique usernames with timestamp
    timestamp = int(time.time())
    
    players = [
        {
            "username": f"charlie_{timestamp}",
            "email": f"charlie_{timestamp}@test.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "phone": "0781234567",
            "player_name": "Charlie Test",
            "age_group": "15-19",
            "province": "kigali",
            "district": "gasabo"
        },
        {
            "username": f"dave_{timestamp}",
            "email": f"dave_{timestamp}@test.com", 
            "password": "testpass123",
            "password_confirm": "testpass123",
            "phone": "0781234568",
            "player_name": "Dave Test",
            "age_group": "15-19",
            "province": "kigali",
            "district": "gasabo"
        },
        {
            "username": f"yves_{timestamp}",
            "email": f"yves_{timestamp}@test.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "phone": "0781234569", 
            "player_name": "Yves Test",
            "age_group": "15-19",
            "province": "kigali",
            "district": "gasabo"
        },
        {
            "username": f"geno_{timestamp}",
            "email": f"geno_{timestamp}@test.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "phone": "0781234570",
            "player_name": "Geno Test", 
            "age_group": "15-19",
            "province": "kigali",
            "district": "gasabo"
        }
    ]
    
    registered_players = []
    
    for i, player_data in enumerate(players):
        print(f"\n👤 Registering Player {i+1}: {player_data['username']}")
        
        result = make_request("POST", "/api/players/register/", player_data)
        
        if result.get("message") == "Player registered successfully":
            player_info = result.get("player", {})
            token = result.get("token")
            
            registered_players.append({
                "id": player_info.get("id"),
                "username": player_data["username"],
                "player_name": player_data["player_name"],
                "token": token
            })
            
            print(f"✅ Player {player_data['username']} registered successfully!")
            print(f"🎟️ Player ID: {player_info.get('id')}")
            print(f"🔑 Token: {token}")
        else:
            print(f"❌ Failed to register {player_data['username']}")
            print(f"📄 Error: {result.get('error', 'Unknown error')}")
    
    if len(registered_players) != 4:
        print(f"\n❌ Only {len(registered_players)}/4 players registered successfully!")
        return None
    
    print(f"\n✅ All {len(registered_players)} players registered successfully!")
    return registered_players

def test_player_centric_workflow():
    """Test the complete player-centric game workflow"""
    
    # Step 0: Register test players
    players = register_test_players()
    if not players:
        print("❌ Player registration failed. Cannot continue with test.")
        return False
    
    print_section("PLAYER-CENTRIC GAME WORKFLOW TEST")
    
    # Step 1: Create Game with only participant count
    print_step(1, "Create Game (Frontend)")
    game_data = make_request("POST", "/api/games/create/", {
        "participant_count": 4
    })
    
    if not game_data.get("success"):
        print("❌ Game creation failed!")
        return False
    
    match_id = game_data["game"]["match_id"]
    print(f"✅ Game created! Match ID: {match_id}")
    
    time.sleep(1)
    
    # Step 2: Simulate frontend distributing match_id to players
    print_step(2, "Frontend distributes Match ID to all players")
    print(f"📡 Match ID distributed: {match_id}")
    print("🎯 All players now have the same match_id to submit their results")
    
    time.sleep(1)
    
    # Step 3: Each player submits their individual result
    print_step(3, "Individual Player Submissions")
    
    # Charlie (Winner) submits
    print(f"\n🏆 {players[0]['player_name']} (Winner) submits result:")
    charlie_result = make_request("POST", "/api/games/submit-player-result/", {
        "match_id": match_id,
        "player_id": players[0]["id"],
        "username": players[0]["username"],
        "player_name": players[0]["player_name"],
        "team": 1,
        "marks_earned": 1,
        "is_winner": True,
        "lost_card": None,
        "question_answered": False,
        "answer_correct": False
    })
    
    if charlie_result.get("success"):
        print(f"✅ {players[0]['player_name']}'s result submitted successfully!")
    else:
        print(f"❌ {players[0]['player_name']}'s submission failed!")
    
    time.sleep(1)
    
    # Dave (Loser) submits
    print(f"\n😞 {players[1]['player_name']} (Loser) submits result:")
    dave_result = make_request("POST", "/api/games/submit-player-result/", {
        "match_id": match_id,
        "player_id": players[1]["id"],
        "username": players[1]["username"],
        "player_name": players[1]["player_name"],
        "team": 2,
        "marks_earned": 0,
        "is_winner": False,
        "lost_card": "S3",
        "question_answered": False,
        "answer_correct": False
    })
    
    if dave_result.get("success"):
        print("✅ Dave's result submitted successfully!")
    else:
        print("❌ Dave's submission failed!")
    
    time.sleep(1)
    
    # Charlie (Winner) submits
    print("\n🏆 Charlie (Winner) submits his result:")
    charlie_result = make_request("POST", "/api/games/submit-player-result/", {
        "match_id": match_id,
        "player_id": 3,
        "username": "charlie",
        "player_name": "Charlie Brown",
        "team": 1,
        "marks_earned": 1,
        "is_winner": True,
        "lost_card": None,
        "question_answered": False,
        "answer_correct": False
    })
    
    if charlie_result.get("success"):
        print("✅ Charlie's result submitted successfully!")
    else:
        print("❌ Charlie's submission failed!")
    
    time.sleep(1)
    
    # Yves (Winner) submits
    print("\n🏆 Yves (Winner) submits his result:")
    yves_result = make_request("POST", "/api/games/submit-player-result/", {
        "match_id": match_id,
        "player_id": 18,
        "username": "yves",
        "player_name": "geeno",
        "team": 1,
        "marks_earned": 1,
        "is_winner": True,
        "lost_card": None,
        "question_answered": False,
        "answer_correct": False
    })
    
    if yves_result.get("success"):
        print("✅ Yves's result submitted successfully!")
    else:
        print("❌ Yves's submission failed!")
    
    time.sleep(1)
    
    # Geno (Loser) submits
    print("\n😞 Geno (Loser) submits his result:")
    geno_result = make_request("POST", "/api/games/submit-player-result/", {
        "match_id": match_id,
        "player_id": 19,
        "username": "geno",
        "player_name": "Geno Yves Cadiot",
        "team": 2,
        "marks_earned": 0,
        "is_winner": False,
        "lost_card": "HJ",
        "question_answered": False,
        "answer_correct": False
    })
    
    if geno_result.get("success"):
        print("✅ Geno's result submitted successfully!")
    else:
        print("❌ Geno's submission failed!")
    
    time.sleep(1)
    
    # Step 4: Each player gets their specific response
    print_step(4, "Players Get Their Specific Responses")
    
    # Charlie gets fun fact
    print("\n🎉 Charlie gets his fun fact (winner response):")
    charlie_response = make_request("GET", f"/api/games/{match_id}/responses/", 
                                 params={"player_id": 3})
    
    if charlie_response.get("success"):
        print("✅ Charlie received his fun fact!")
    else:
        print("❌ Charlie's response retrieval failed!")
    
    time.sleep(1)
    
    # Dave gets question
    print("\n❓ Dave gets his question (loser response):")
    dave_response = make_request("GET", f"/api/games/{match_id}/responses/", 
                               params={"player_id": 4})
    
    if dave_response.get("success"):
        print("✅ Dave received his question!")
    else:
        print("❌ Dave's response retrieval failed!")
    
    time.sleep(1)
    
    # Step 5: Losing players submit answers
    print_step(5, "Losing Players Submit Answers")
    
    # Dave submits answer
    print("\n📝 Dave submits his answer:")
    dave_answer = make_request("POST", "/api/games/submit-answer/", {
        "match_id": match_id,
        "player_id": 4,
        "username": "dave",
        "answer": "Spades"
    })
    
    if dave_answer.get("success"):
        print("✅ Dave's answer submitted successfully!")
        if dave_answer.get("result", {}).get("is_correct"):
            print("🎯 Dave's answer was CORRECT!")
        else:
            print("❌ Dave's answer was INCORRECT!")
    else:
        print("❌ Dave's answer submission failed!")
    
    time.sleep(1)
    
    # Geno submits answer
    print("\n📝 Geno submits his answer:")
    geno_answer = make_request("POST", "/api/games/submit-answer/", {
        "match_id": match_id,
        "player_id": 19,
        "username": "geno",
        "answer": "Hearts"
    })
    
    if geno_answer.get("success"):
        print("✅ Geno's answer submitted successfully!")
        if geno_answer.get("result", {}).get("is_correct"):
            print("🎯 Geno's answer was CORRECT!")
        else:
            print("❌ Geno's answer was INCORRECT!")
    else:
        print("❌ Geno's answer submission failed!")
    
    time.sleep(1)
    
    # Step 6: Check final game status
    print_step(6, "Check Final Game Status")
    game_status = make_request("GET", f"/api/games/{match_id}/status/")
    
    if game_status.get("success"):
        print("✅ Game status retrieved successfully!")
        game_info = game_status.get("game", {})
        print(f"🎮 Game Status: {game_info.get('status')}")
        print(f"👥 Participants: {game_info.get('participant_count')}")
        if game_info.get("winning_team"):
            print(f"🏆 Winning Team: {game_info.get('winning_team')}")
    else:
        print("❌ Game status retrieval failed!")
    
    print_section("TEST COMPLETED")
    print("🎉 Player-centric workflow test finished!")
    print(f"🆔 Match ID used: {match_id}")
    print("\n📋 Summary:")
    print("✅ 1. Game created with participant count only")
    print("✅ 2. Match ID distributed to all players")
    print("✅ 3. Each player submitted individual results")
    print("✅ 4. Players received personalized responses")
    print("✅ 5. Losing players submitted answers")
    print("✅ 6. Final game status checked")
    
    return True

def test_simple_game_creation():
    """Test just the simplified game creation"""
    print_section("SIMPLIFIED GAME CREATION TEST")
    
    print_step(1, "Test Basic Game Creation")
    
    # Test different participant counts
    for count in [1, 2, 4, 6]:
        print(f"\n🎲 Testing {count} participant(s)")
        game_data = make_request("POST", "/api/games/create/", {
            "participant_count": count
        })
        
        if game_data.get("success"):
            match_id = game_data["game"]["match_id"]
            print(f"✅ {count}-player game created! Match ID: {match_id}")
        else:
            print(f"❌ {count}-player game creation failed!")
        
        time.sleep(0.5)

if __name__ == "__main__":
    print("🚀 Starting Game API Tests")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Register test players first
        register_test_players()
        
        time.sleep(2)
        
        # Test simple game creation
        test_simple_game_creation()
        
        time.sleep(2)
        
        # Test complete workflow
        test_player_centric_workflow()
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
    
    print(f"\n🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
