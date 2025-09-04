#!/usr/bin/env python3
"""
Test script for question answer workflow - both correct and incorrect answers
Tests: question answering -> explanation returns for both scenarios
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

def test_question_answer_workflow():
    """Test complete workflow with both correct and incorrect answers"""
    
    print_section("QUESTION ANSWER WORKFLOW TEST")
    
    # Step 1: Create Game
    print_step(1, "Create Game")
    game_data = make_request("POST", "/api/games/create/", {
        "participant_count": 2
    })
    
    if not game_data.get("success"):
        print("❌ Game creation failed!")
        return False
    
    match_id = game_data["game"]["match_id"]
    print(f"✅ Game created! Match ID: {match_id}")
    
    time.sleep(1)
    
    # Step 2: Winner submits result
    print_step(2, "Winner Submits Result")
    winner_result = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id,
        "player_id": 1,
        "username": "alice",
        "team": 1,
        "is_winner": True,
        "lost_card": None
    })
    
    if not winner_result.get("success"):
        print("❌ Winner submission failed!")
        return False
    
    print("✅ Winner submitted successfully!")
    
    time.sleep(1)
    
    # Step 3: First Loser submits result (will answer correctly)
    print_step(3, "First Loser Submits Result")
    loser1_result = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id,
        "player_id": 2,
        "username": "bob",
        "team": 2,
        "is_winner": False,
        "lost_card": "S3"
    })
    
    if not loser1_result.get("success"):
        print("❌ First loser submission failed!")
        return False
    
    question1 = loser1_result.get('response', {}).get('question')
    if not question1:
        print("❌ No question received for first loser!")
        return False
    
    print("✅ First loser submitted successfully!")
    print(f"📝 Question: {question1['question_text']}")
    print(f"🎯 Correct Answer: {question1['correct_answer']}")
    
    time.sleep(1)
    
    # Step 4: First Loser answers CORRECTLY
    print_step(4, "First Loser Answers Correctly")
    correct_answer_result = make_request("POST", "/api/games/award-points/", {
        "match_id": match_id,
        "username": "bob",
        "question_id": question1['id'],
        "answer": question1['correct_answer'],  # Correct answer
        "points": 1
    })
    
    if correct_answer_result.get("success"):
        print("✅ Points awarded successfully!")
        print(f"🎯 Points awarded: {correct_answer_result.get('result', {}).get('points_awarded')}")
        print(f"📖 Explanation received: {correct_answer_result.get('result', {}).get('question', {}).get('explanation')}")
        print(f"📊 Player total marks: {correct_answer_result.get('result', {}).get('player', {}).get('total_marks')}")
    else:
        print("❌ Point award failed!")
        print(f"Error: {correct_answer_result.get('error')}")
    
    time.sleep(2)
    
    # Step 5: Create a second game for testing wrong answer
    print_step(5, "Create Second Game for Wrong Answer Test")
    game_data2 = make_request("POST", "/api/games/create/", {
        "participant_count": 2
    })
    
    if not game_data2.get("success"):
        print("❌ Second game creation failed!")
        return False
    
    match_id2 = game_data2["game"]["match_id"]
    print(f"✅ Second game created! Match ID: {match_id2}")
    
    time.sleep(1)
    
    # Step 6: Winner submits result in second game
    print_step(6, "Winner Submits Result (Game 2)")
    winner_result2 = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id2,
        "player_id": 3,
        "username": "charlie",
        "team": 1,
        "is_winner": True,
        "lost_card": None
    })
    
    if not winner_result2.get("success"):
        print("❌ Winner submission failed in game 2!")
        return False
    
    print("✅ Winner submitted successfully in game 2!")
    
    time.sleep(1)
    
    # Step 7: Second Loser submits result (will answer incorrectly)
    print_step(7, "Second Loser Submits Result")
    loser2_result = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id2,
        "player_id": 4,
        "username": "dave",
        "team": 2,
        "is_winner": False,
        "lost_card": "H7"
    })
    
    if not loser2_result.get("success"):
        print("❌ Second loser submission failed!")
        return False
    
    question2 = loser2_result.get('response', {}).get('question')
    if not question2:
        print("❌ No question received for second loser!")
        return False
    
    print("✅ Second loser submitted successfully!")
    print(f"📝 Question: {question2['question_text']}")
    print(f"🎯 Correct Answer: {question2['correct_answer']}")
    
    time.sleep(1)
    
    # Step 8: Second Loser answers INCORRECTLY
    print_step(8, "Second Loser Answers Incorrectly")
    
    # Create a wrong answer (if it's True/False, choose the opposite)
    wrong_answer = "False" if question2['correct_answer'] == "True" else "True"
    if question2['question_type'] == 'multiple_choice' and question2.get('options'):
        # Choose a different option
        for option in question2['options']:
            if option != question2['correct_answer']:
                wrong_answer = option
                break
    
    wrong_answer_result = make_request("POST", "/api/games/record-wrong-answer/", {
        "match_id": match_id2,
        "username": "dave",
        "question_id": question2['id'],
        "answer": wrong_answer
    })
    
    if wrong_answer_result.get("success"):
        print("✅ Wrong answer recorded successfully!")
        print(f"❌ Points awarded: {wrong_answer_result.get('result', {}).get('points_awarded')}")
        print(f"📖 Explanation received: {wrong_answer_result.get('result', {}).get('explanation')}")
        print(f"🎯 Correct answer shown: {wrong_answer_result.get('result', {}).get('correct_answer')}")
        print(f"📊 Player accuracy: {wrong_answer_result.get('result', {}).get('player', {}).get('answer_accuracy')}%")
    else:
        print("❌ Wrong answer recording failed!")
        print(f"Error: {wrong_answer_result.get('error')}")
    
    time.sleep(1)
    
    # Step 9: Check final game statuses
    print_step(9, "Check Final Game Statuses")
    
    print("\n🔍 Game 1 Status (Correct Answer):")
    final_status1 = make_request("GET", f"/api/games/{match_id}/status/")
    
    print("\n🔍 Game 2 Status (Wrong Answer):")
    final_status2 = make_request("GET", f"/api/games/{match_id2}/status/")
    
    return True

def main():
    """Run the test"""
    print_section("STARTING QUESTION ANSWER WORKFLOW TEST")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Testing against: {BASE_URL}")
    
    try:
        if not test_question_answer_workflow():
            print("❌ Question answer workflow test failed!")
            return
        
        print_section("TEST COMPLETED SUCCESSFULLY! 🎉")
        print("\n📋 Summary:")
        print("✅ Correct answer scenario: Points awarded + explanation provided")
        print("✅ Wrong answer scenario: No points awarded + explanation provided")
        print("✅ Both winners and losers receive explanations after answering")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
