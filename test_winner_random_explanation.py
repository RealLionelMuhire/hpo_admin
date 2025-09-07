#!/usr/bin/env python3
"""
Test script to verify winner gets random question explanation
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

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

def test_winner_random_explanation():
    """Test that winners get random question explanations"""
    
    print_header("WINNER RANDOM EXPLANATION TEST")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    explanations_received = []
    
    # Test multiple games to see different explanations
    for i in range(3):
        print(f"\n🎮 Testing Game {i+1}/3")
        
        # Create Game
        game_data = make_request("POST", "/api/games/create/", {
            "participant_count": 2
        })
        
        if not game_data.get("success"):
            print("❌ Game creation failed!")
            continue
        
        match_id = game_data["game"]["match_id"]
        print(f"✅ Game created: {match_id}")
        
        # Winner submits result
        winner_result = make_request("POST", "/api/games/submit-completed/", {
            "match_id": match_id,
            "player_id": i*2+1,
            "username": f"winner_{i+1}",
            "team": 1,
            "is_winner": True,
            "lost_card": None
        })
        
        if winner_result.get("success"):
            explanation = winner_result.get('response', {}).get('explanation')
            explanations_received.append(explanation)
            print(f"🎯 Winner explanation: {explanation}")
            
            # Check if it's NOT the old generic message
            if explanation != "Congratulations on your victory!":
                print("✅ Winner received educational explanation!")
            else:
                print("⚠️ Winner still getting generic message")
        else:
            print("❌ Winner submission failed!")
    
    # Summary
    print_header("TEST RESULTS")
    print(f"📊 Total explanations received: {len(explanations_received)}")
    
    for i, explanation in enumerate(explanations_received, 1):
        print(f"Game {i}: {explanation[:100]}...")
    
    # Check for variety
    unique_explanations = set(explanations_received)
    print(f"\n🎯 Unique explanations: {len(unique_explanations)}")
    
    if len(unique_explanations) > 1:
        print("✅ Winners are receiving different random explanations!")
    elif len(unique_explanations) == 1 and explanations_received[0] != "Congratulations on your victory!":
        print("✅ Winners are receiving educational explanations (may be same due to small question pool)")
    else:
        print("❌ Winners are still getting generic messages")

def main():
    """Run the test"""
    try:
        test_winner_random_explanation()
        print_header("TEST COMPLETED! 🎉")
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
