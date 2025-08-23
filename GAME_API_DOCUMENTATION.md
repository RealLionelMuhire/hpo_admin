# Game API Documentation

This document describes the Game MVC system that allows players to participate in card games where winners receive fun facts and losers answer questions.

## Game Flow Overview

1. **Create Game**: Create a new game session with 1, 2, 4, or 6 participants
2. **Complete Game**: Mark the game as completed with winning team
3. **Get Responses**: Winners get fun facts, losers get questions
4. **Submit Answers**: Losing players submit answers to their questions
5. **Check Status**: Monitor game progress and results

## API Endpoints

All endpoints are **unauthenticated** and use JSON for request/response.

### 1. Create Game
```
POST /api/games/create/
```

**Request Body:**
```json
{
    "participant_count": 2,
    "players": [
        {"username": "player1", "player_name": "Alice"},
        {"username": "player2", "player_name": "Bob"}
    ]
}
```

**Valid participant counts:** 1, 2, 4, 6
- 1 participant = Player vs Computer (1 team)
- 2+ participants = 2 teams (participants split evenly)

**Response:**
```json
{
    "success": true,
    "game": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "participant_count": 2,
        "team_count": 2,
        "players_per_team": 1,
        "status": "active",
        "participants": [
            {"username": "player1", "player_name": "Alice", "team": 1},
            {"username": "player2", "player_name": "Bob", "team": 2}
        ]
    }
}
```

### 2. Complete Game
```
POST /api/games/complete/
```

**Request Body:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "winning_team": 1,
    "cards_played": ["S3", "HJ", "DA"]
}
```

**Response:**
```json
{
    "success": true,
    "game": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "completed",
        "winning_team": 1,
        "team1_marks": 1,
        "team2_marks": 0,
        "completed_at": "2025-08-23T10:30:00Z"
    }
}
```

### 3. Get Game Responses
```
GET /api/games/{match_id}/responses/
```

Returns different responses for winners and losers:

**Response:**
```json
{
    "success": true,
    "game": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "completed",
        "winning_team": 1
    },
    "responses": [
        {
            "username": "player1",
            "player_name": "Alice",
            "team": 1,
            "is_winner": true,
            "response_type": "fun_fact",
            "fun_fact": "Did you know that the heart suit represents emotions and love?",
            "card": "HJ",
            "card_info": {
                "suit": "Hearts",
                "value": "J",
                "pointValue": 3,
                "symbol": "♥"
            }
        },
        {
            "username": "player2",
            "player_name": "Bob",
            "team": 2,
            "is_winner": false,
            "response_type": "question",
            "card": "S3",
            "card_info": {
                "suit": "Spades",
                "value": "3",
                "pointValue": 0,
                "symbol": "♠"
            },
            "question": {
                "id": 123,
                "question_text": "What suit is associated with conflict?",
                "question_type": "multiple_choice",
                "options": ["Hearts", "Spades", "Clubs", "Diamonds"],
                "difficulty": "easy",
                "points": 1
            }
        }
    ]
}
```

### 4. Submit Answer
```
POST /api/games/submit-answer/
```

**Request Body:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "player2",
    "answer": "Spades"
}
```

**Response:**
```json
{
    "success": true,
    "result": {
        "is_correct": true,
        "correct_answer": "Spades",
        "explanation": "Spades represent conflict and challenges in card symbolism.",
        "points_earned": 1
    }
}
```

### 5. Get Game Status
```
GET /api/games/{match_id}/status/
```

**Response:**
```json
{
    "success": true,
    "game": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "participant_count": 2,
        "team_count": 2,
        "status": "completed",
        "winning_team": 1,
        "cards_in_play": ["S3", "HJ", "DA"],
        "created_at": "2025-08-23T10:00:00Z",
        "completed_at": "2025-08-23T10:30:00Z",
        "participants": [
            {
                "username": "player1",
                "player_name": "Alice",
                "team": 1,
                "is_winner": true,
                "marks_earned": 1,
                "lost_card": null,
                "question_answered": false,
                "answer_correct": false
            },
            {
                "username": "player2",
                "player_name": "Bob",
                "team": 2,
                "is_winner": false,
                "marks_earned": 0,
                "lost_card": "S3",
                "question_answered": true,
                "answer_correct": true
            }
        ],
        "result": {
            "team1_marks": 1,
            "team2_marks": 0,
            "result_summary": {
                "winning_team": 1,
                "cards_played": ["S3", "HJ", "DA"],
                "completed_at": "2025-08-23T10:30:00Z"
            }
        }
    }
}
```

### 6. Get Player Statistics
```
GET /api/players/{username}/stats/
```

**Response:**
```json
{
    "success": true,
    "player": {
        "username": "alice",
        "player_name": "Alice",
        "created_at": "2025-08-20T10:00:00Z",
        "last_active": "2025-08-23T11:00:00Z"
    },
    "statistics": {
        "total_games": 15,
        "wins": 10,
        "losses": 5,
        "win_rate": 66.67,
        "total_marks": 10,
        "average_marks_per_game": 0.67,
        "current_streak": 3,
        "longest_streak": 5,
        "answer_accuracy": 85.0,
        "last_played": "2025-08-23T10:30:00Z",
        "last_result": "won"
    },
    "recent_games": [
        {
            "match_id": "550e8400-e29b-41d4-a716-446655440000",
            "date": "2025-08-23T10:00:00Z",
            "participants": 2,
            "team": 1,
            "won": true,
            "marks_earned": 1,
            "card_assigned": null,
            "question_answered": false,
            "answer_correct": false,
            "game_status": "completed"
        }
    ]
}
```

### 7. Get Leaderboard
```
GET /api/leaderboard/?metric=win_rate&limit=10
```

**Query Parameters:**
- `metric`: 'win_rate', 'total_marks', 'games_won', 'answer_accuracy', 'win_streak'
- `limit`: number of players to return (default 10)

**Response:**
```json
{
    "success": true,
    "metric": "win_rate",
    "total_players": 10,
    "leaderboard": [
        {
            "rank": 1,
            "username": "alice",
            "player_name": "Alice",
            "games_played": 15,
            "games_won": 10,
            "total_marks": 10,
            "win_rate": 66.67,
            "answer_accuracy": 85.0,
            "current_win_streak": 3,
            "longest_win_streak": 5,
            "last_played": "2025-08-23T10:30:00Z"
        },
        {
            "rank": 2,
            "username": "bob",
            "player_name": "Bob",
            "games_played": 12,
            "games_won": 7,
            "total_marks": 7,
            "win_rate": 58.33,
            "answer_accuracy": 78.0,
            "current_win_streak": 0,
            "longest_win_streak": 3,
            "last_played": "2025-08-23T09:15:00Z"
        }
    ]
}
```

## Game Logic

### Teams and Marks
- **1 participant**: 1 team (player vs computer)
- **2+ participants**: 2 teams (split evenly)
- **Winning team members**: Each gets 1 mark
- **Losing team members**: Each gets 0 marks

### Winner Responses
Winners receive fun facts from the `explanation` field of questions associated with cards that losing players received.

### Loser Responses
Losing players receive questions associated with their assigned card and must answer them.

### Card Assignment
When a game is completed, losing players are randomly assigned cards from:
1. Cards played during the game (if provided)
2. Random cards from all available cards (if no cards specified)

### Player Statistics Tracking
The system automatically tracks comprehensive statistics for each player:

**Game Statistics:**
- `games_played`: Total number of games participated in
- `games_won`: Total number of games won
- `games_lost`: Total number of games lost
- `total_game_marks`: Total marks earned from all games
- `win_rate`: Calculated percentage (games_won / games_played * 100)
- `average_marks_per_game`: Average marks per game

**Question Statistics:**
- `questions_answered`: Total questions answered in games
- `correct_answers`: Total correct answers given
- `answer_accuracy`: Calculated percentage (correct_answers / questions_answered * 100)

**Achievements & Streaks:**
- `current_win_streak`: Current consecutive wins
- `longest_win_streak`: Longest win streak achieved
- `last_game_played`: Timestamp of last game participation
- `last_game_result`: 'won' or 'lost'

**Automatic Updates:**
- Statistics are automatically updated when games are completed
- Question statistics are updated when losing players submit answers
- Win streaks are maintained and updated based on game outcomes

## Example Game Flow

1. **Create a 2-player game:**
```bash
curl -X POST http://localhost:8000/api/games/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "participant_count": 2,
    "players": [
      {"username": "alice", "player_name": "Alice"},
      {"username": "bob", "player_name": "Bob"}
    ]
  }'
```

2. **Complete the game (Alice wins):**
```bash
curl -X POST http://localhost:8000/api/games/complete/ \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "YOUR_MATCH_ID",
    "winning_team": 1,
    "cards_played": ["HJ", "S3"]
  }'
```

3. **Get responses:**
```bash
curl http://localhost:8000/api/games/YOUR_MATCH_ID/responses/
```

4. **Bob submits his answer:**
```bash
curl -X POST http://localhost:8000/api/games/submit-answer/ \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "YOUR_MATCH_ID",
    "username": "bob",
    "answer": "Spades"
  }'
```

5. **Check Alice's statistics:**
```bash
curl http://localhost:8000/api/players/alice/stats/
```

6. **View leaderboard by win rate:**
```bash
curl "http://localhost:8000/api/leaderboard/?metric=win_rate&limit=5"
```

## Database Models

### Game
- `match_id`: Unique game identifier (UUID)
- `participant_count`: Number of players (1, 2, 4, 6)
- `team_count`: Calculated (1 for single player, 2 for multiplayer)
- `status`: waiting, active, completed, cancelled
- `winning_team`: 1 or 2 (null if not finished)
- `cards_in_play`: JSON list of cards used

### GameParticipant
- Links players to games
- `team`: 1 or 2
- `is_winner`: Boolean
- `marks_earned`: Integer (1 for winners, 0 for losers)
- `lost_card`: Card assigned to losing players
- `question_answered`: Boolean
- `answer_correct`: Boolean

### GameResult
- Stores final game results
- `team1_marks`: Total marks for team 1
- `team2_marks`: Total marks for team 2
- `result_summary`: JSON summary

### GameResponse
- Stores player responses
- `response_type`: 'fun_fact' or 'question'
- `fun_fact_text`: For winners
- `question`: For losers
- `player_answer`: Submitted answer
- `is_correct`: Answer correctness

## Error Handling

All endpoints return consistent error responses:

```json
{
    "success": false,
    "error": "Error description"
}
```

Common HTTP status codes:
- `400`: Bad Request (invalid data)
- `404`: Not Found (game/player not found)
- `500`: Internal Server Error

## Admin Interface

All game models are registered in Django admin with comprehensive views:
- Game management and monitoring
- Participant tracking
- Result analysis
- Response management

Access admin at: `/admin/`

## Notes

- All endpoints are unauthenticated for easy integration
- Players are automatically created if they don't exist
- Questions must be pre-populated in the database
- Cards follow standard format: S3, HJ, DA, etc. (Suit + Value)
- Fun facts come from question explanations
