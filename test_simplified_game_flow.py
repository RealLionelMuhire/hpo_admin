#!/usr/bin/env python3
"""
Test script for the simplified player-centric game workflow
Tests: game creation -> player submissions -> automatic responses -> mark awards
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

def test_simplified_workflow():
    """Test the simplified player-centric game workflow"""
    
    print_section("SIMPLIFIED PLAYER-CENTRIC GAME WORKFLOW TEST")
    
    # Step 1: Create Game with only participant count
    print_step(1, "Create Game (Frontend)")
    game_data = make_request("POST", "/api/games/create/", {
        "participant_count": 2
    })
    
    if not game_data.get("success"):
        print("❌ Game creation failed!")
        return False
    
    match_id = game_data["game"]["match_id"]
    print(f"✅ Game created! Match ID: {match_id}")
    
    time.sleep(1)
    
    # Step 2: Winner submits result (simplified payload)
    print_step(2, "Winner Submits Result")
    winner_result = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id,
        "player_id": 1,  # Assuming existing player
        "username": "alice",
        "team": 1,
        "is_winner": True,
        "lost_card": None  # Winners don't need lost_card
    })
    
    if winner_result.get("success"):
        print("✅ Winner submission successful!")
        print(f"🏆 Winner response type: {winner_result.get('response', {}).get('type')}")
        if winner_result.get('response', {}).get('explanation'):
            print(f"📖 Explanation: {winner_result['response']['explanation']}")
    else:
        print("❌ Winner submission failed!")
        print(f"Error: {winner_result.get('error')}")
    
    time.sleep(1)
    
    # Step 3: Loser submits result (with lost_card)
    print_step(3, "Loser Submits Result")
    loser_result = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id,
        "player_id": 2,  # Assuming existing player
        "username": "bob", 
        "team": 2,
        "is_winner": False,
        "lost_card": "S3"  # Loser must specify which card they lost
    })
    
    if loser_result.get("success"):
        print("✅ Loser submission successful!")
        print(f"❓ Loser response type: {loser_result.get('response', {}).get('type')}")
        
        # Check if question was provided
        question = loser_result.get('response', {}).get('question')
        if question:
            print(f"📝 Question: {question['question_text']}")
            print(f"🎯 Correct Answer: {question['correct_answer']}")
            print(f"🃏 Card: {question['card']}")
            
            # Step 4: Simulate frontend answer validation and award points
            print_step(4, "Frontend Validates Answer and Awards Points")
            
            # Simulate correct answer
            award_result = make_request("POST", "/api/games/award-points/", {
                "match_id": match_id,
                "username": "bob",
                "question_id": question['id'],
                "answer": question['correct_answer'],  # Correct answer
                "points": 1
            })
            
            if award_result.get("success"):
                print("✅ Points awarded successfully!")
                print(f"🎯 Points awarded: {award_result.get('result', {}).get('points_awarded')}")
                print(f"📊 Player total marks: {award_result.get('result', {}).get('player', {}).get('total_marks')}")
            else:
                print("❌ Point award failed!")
                print(f"Error: {award_result.get('error')}")
    else:
        print("❌ Loser submission failed!")
        print(f"Error: {loser_result.get('error')}")
    
    time.sleep(1)
    
    # Step 5: Check final game status
    print_step(5, "Check Final Game Status")
    final_status = make_request("GET", f"/api/games/{match_id}/status/")
    
    if final_status.get("success"):
        print("✅ Game status retrieved!")
        print(f"🎮 Game Status: {final_status.get('game', {}).get('status')}")
        print(f"🏁 Completed: {final_status.get('game', {}).get('completed_at')}")
    
    return True

def test_multiple_game_sizes():
    """Test game creation with different participant counts"""
    
    print_section("MULTIPLE GAME SIZE TEST")
    
    participant_counts = [1, 2, 4, 6]
    success_count = 0
    
    for count in participant_counts:
        print_step(count, f"Testing {count} participant game")
        
        game_data = make_request("POST", "/api/games/create/", {
            "participant_count": count
        })
        
        if game_data.get("success"):
            print(f"✅ {count}-player game created successfully!")
            print(f"🆔 Match ID: {game_data['game']['match_id']}")
            print(f"👥 Teams: {game_data['game']['team_count']}")
            success_count += 1
        else:
            print(f"❌ {count}-player game creation failed!")
            print(f"Error: {game_data.get('error')}")
        
        time.sleep(0.5)
    
    print(f"\n📊 Game Creation Results: {success_count}/{len(participant_counts)} successful")
    return success_count == len(participant_counts)

def main():
    """Run all tests"""
    print_section("STARTING SIMPLIFIED GAME WORKFLOW TESTS")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing against: {BASE_URL}")
    
    try:
        # Test 1: Multiple game sizes
        if not test_multiple_game_sizes():
            print("❌ Multiple game size test failed!")
            return
        
        time.sleep(2)
        
        # Test 2: Complete simplified workflow
        if not test_simplified_workflow():
            print("❌ Simplified workflow test failed!")
            return
        
        print_section("ALL TESTS COMPLETED SUCCESSFULLY! 🎉")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
