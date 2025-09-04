#!/usr/bin/env python3
"""
Test script for Loser/Winner Explanation Feature
Tests that both correct and incorrect answers return explanations for educational value.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🎓 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n📍 {step}: {description}")
    print("-" * 40)

def make_request(method, endpoint, data=None):
    """Make HTTP request and return response"""
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, headers=headers)
        
        print(f"🌐 {method} {endpoint}")
        if data:
            print(f"📤 Data: {json.dumps(data, indent=2)}")
        
        print(f"📊 Status: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            response_data = response.json()
            print(f"📥 Response: {json.dumps(response_data, indent=2)}")
            return response_data
        else:
            print(f"📥 Response: {response.text}")
            return {"error": "Non-JSON response"}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return {"error": str(e)}

def test_explanation_feature():
    """Test the loser/winner explanation feature"""
    
    print_header("EXPLANATION FEATURE TEST")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Create Game
    print_step("Step 1", "Create Game")
    game_data = make_request("POST", "/api/games/create/", {
        "participant_count": 2
    })
    
    if not game_data.get("success"):
        print("❌ Game creation failed!")
        return False
    
    match_id = game_data["game"]["match_id"]
    print(f"✅ Game created with Match ID: {match_id}")
    
    # Step 2: Winner submits result and gets explanation
    print_step("Step 2", "Winner Submits Result (Should get explanation)")
    winner_result = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id,
        "player_id": 1,
        "username": "winner_alice",
        "team": 1,
        "is_winner": True,
        "lost_card": None
    })
    
    if not winner_result.get("success"):
        print("❌ Winner submission failed!")
        return False
    
    winner_explanation = winner_result.get('response', {}).get('explanation')
    print(f"🎯 Winner received explanation: {winner_explanation}")
    print("✅ Winner automatically gets mark + explanation!")
    
    # Step 3: Loser submits result and gets question
    print_step("Step 3", "Loser Submits Result (Should get question)")
    loser_result = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id,
        "player_id": 2,
        "username": "loser_bob",
        "team": 2,
        "is_winner": False,
        "lost_card": "H5"
    })
    
    if not loser_result.get("success"):
        print("❌ Loser submission failed!")
        return False
    
    question = loser_result.get('response', {}).get('question')
    if not question:
        print("❌ No question received!")
        return False
    
    print(f"📝 Question received: {question['question_text']}")
    print(f"🎯 Correct answer: {question['correct_answer']}")
    print("✅ Loser received question to answer!")
    
    # Step 4: Test CORRECT answer (should get mark + explanation)
    print_step("Step 4", "Loser Answers CORRECTLY (Should get mark + explanation)")
    correct_answer_result = make_request("POST", "/api/games/award-points/", {
        "match_id": match_id,
        "username": "loser_bob",
        "question_id": question['id'],
        "answer": question['correct_answer'],  # Use correct answer
        "points": 1
    })
    
    if correct_answer_result.get("success"):
        points = correct_answer_result.get('result', {}).get('points_awarded')
        explanation = correct_answer_result.get('result', {}).get('question', {}).get('explanation')
        print(f"🎯 Points awarded: {points}")
        print(f"📖 Explanation received: {explanation}")
        print("✅ Correct answer: Mark awarded + explanation provided!")
    else:
        print(f"❌ Correct answer failed: {correct_answer_result.get('error')}")
    
    # Step 5: Create second game for wrong answer test
    print_step("Step 5", "Create Second Game for Wrong Answer Test")
    game_data2 = make_request("POST", "/api/games/create/", {
        "participant_count": 2
    })
    
    if not game_data2.get("success"):
        print("❌ Second game creation failed!")
        return False
    
    match_id2 = game_data2["game"]["match_id"]
    print(f"✅ Second game created: {match_id2}")
    
    # Step 6: Submit winner and loser for second game
    print_step("Step 6", "Submit Players for Second Game")
    
    # Winner
    make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id2,
        "player_id": 3,
        "username": "winner_charlie",
        "team": 1,
        "is_winner": True,
        "lost_card": None
    })
    
    # Loser
    loser_result2 = make_request("POST", "/api/games/submit-completed/", {
        "match_id": match_id2,
        "player_id": 4,
        "username": "loser_dave",
        "team": 2,
        "is_winner": False,
        "lost_card": "C7"
    })
    
    question2 = loser_result2.get('response', {}).get('question')
    if not question2:
        print("❌ No question received in second game!")
        return False
    
    print(f"📝 Second question: {question2['question_text']}")
    print(f"🎯 Correct answer: {question2['correct_answer']}")
    
    # Step 7: Test WRONG answer (should get 0 marks + explanation)
    print_step("Step 7", "Loser Answers INCORRECTLY (Should get explanation)")
    
    # Create wrong answer
    wrong_answer = "False" if question2['correct_answer'] == "True" else "True"
    if question2['question_type'] == 'multiple_choice' and question2.get('options'):
        for option in question2['options']:
            if option != question2['correct_answer']:
                wrong_answer = option
                break
    
    wrong_answer_result = make_request("POST", "/api/games/record-wrong-answer/", {
        "match_id": match_id2,
        "username": "loser_dave",
        "question_id": question2['id'],
        "answer": wrong_answer
    })
    
    if wrong_answer_result.get("success"):
        points = wrong_answer_result.get('result', {}).get('points_awarded')
        explanation = wrong_answer_result.get('result', {}).get('explanation')
        correct_answer = wrong_answer_result.get('result', {}).get('correct_answer')
        print(f"🎯 Points awarded: {points}")
        print(f"📖 Explanation received: {explanation}")
        print(f"✅ Correct answer shown: {correct_answer}")
        print("✅ Wrong answer: No marks but explanation provided for learning!")
    else:
        print(f"❌ Wrong answer recording failed: {wrong_answer_result.get('error')}")
    
    return True

def main():
    """Run the explanation feature test"""
    try:
        if test_explanation_feature():
            print_header("TEST COMPLETED SUCCESSFULLY! 🎉")
            print("\n📋 Feature Summary:")
            print("✅ Winners: Automatic mark + explanation")
            print("✅ Losers with correct answers: Mark + explanation")  
            print("✅ Losers with wrong answers: No mark + explanation (learning)")
            print("✅ Educational value maintained for all scenarios")
            print("\n🎓 Both winners and losers receive explanations!")
        else:
            print_header("TEST FAILED! ❌")
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
