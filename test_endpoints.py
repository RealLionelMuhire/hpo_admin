#!/usr/bin/env python3
import requests
import json
import uuid

# Test data
base_url = "http://localhost:8000"

# Test 1: Submit Completed Game
print("=== Test 1: Submit Completed Game ===")
test_data = {
    "match_id": str(uuid.uuid4()),
    "game_data": {
        "participant_count": 2,
        "winning_team": 1,
        "cards_chosen": ["S3", "HJ"],
        "game_duration": 300
    },
    "players": [
        {
            "player_id": 1,
            "username": "alice",
            "player_name": "Alice Smith",
            "team": 1,
            "marks_earned": 1,
            "is_winner": True,
            "lost_card": None,
            "question_answered": False,
            "answer_correct": False
        },
        {
            "player_id": 2,
            "username": "bob",
            "player_name": "Bob Johnson",
            "team": 2,
            "marks_earned": 0,
            "is_winner": False,
            "lost_card": "S3",
            "question_answered": False,
            "answer_correct": False
        }
    ],
    "responses": [
        {
            "player_id": 1,
            "response_type": "fun_fact",
            "fun_fact_text": "Did you know that spades represent challenges?",
            "card": "S3"
        },
        {
            "player_id": 2,
            "response_type": "question",
            "question_id": 1,
            "card": "S3"
        }
    ]
}

try:
    response = requests.post(f"{base_url}/api/games/submit-completed/", 
                           json=test_data, 
                           headers={"Content-Type": "application/json"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    match_id = response.json().get("game", {}).get("match_id")
except Exception as e:
    print(f"Error: {e}")
    match_id = None

print("\n" + "="*50)

# Test 2: Get Game Responses
if match_id:
    print("=== Test 2: Get Game Responses ===")
    try:
        response = requests.get(f"{base_url}/api/games/{match_id}/responses/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "="*50)

# Test 3: Award Points
print("=== Test 3: Award Points ===")
try:
    award_data = {
        "match_id": match_id or str(uuid.uuid4()),
        "username": "bob",
        "question_id": 1,
        "answer": "Kigali",
        "points": 1
    }
    response = requests.post(f"{base_url}/api/games/award-points/", 
                           json=award_data, 
                           headers={"Content-Type": "application/json"})
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50)

# Test 4: Get Player Stats
print("=== Test 4: Get Player Stats ===")
try:
    response = requests.get(f"{base_url}/api/players/alice/stats/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50)

# Test 5: Get Leaderboard
print("=== Test 5: Get Leaderboard ===")
try:
    response = requests.get(f"{base_url}/api/leaderboard/?metric=win_rate&limit=3")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50)

# Test 6: Get Questions by Card
print("=== Test 6: Get Questions by Card ===")
try:
    response = requests.get(f"{base_url}/api/cards/S3/questions/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
