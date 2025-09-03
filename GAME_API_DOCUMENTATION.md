# Game API Documentation

This document describes the simplified Game MVC system that allows players to participate in card games with a player-centric workflow.

## Game Flow Overview

1. **Create Game**: Frontend creates a game session with only participant count and receives a match_id
2. **Distribute Match ID**: Frontend distributes the match_id to all players  
3. **Individual Player Submission**: Each player submits their win/loss result using the same match_id
4. **Automatic Response Generation**: System automatically generates appropriate responses (winners get explanations, losers get questions)
5. **Frontend Answer Validation**: For losers, frontend validates answers and calls award-points endpoint if correct

**Important Game Logic:**
- **Winners**: Automatically get 1 mark and receive explanation (fun fact) from question model
- **Losers**: Get full question object, frontend validates answer, backend awards mark if correct
- **No "question_answered" or "answer_correct" fields** needed in the submission for winners
- **Simplified workflow** reduces code duplication and clarifies responsibilities

## Post-Game Response Logic

### Winners
- Automatically receive 1 mark
- Get explanation/fun fact from a question related to their context
- No additional action needed

### Losers  
- Receive full question object including `correct_answer`
- Frontend is responsible for answer validation
- If correct answer: frontend calls `/api/games/award-points/` to award 1 mark
- If wrong answer: no mark awarded

## API Endpoints

All endpoints are **unauthenticated** and use JSON for request/response.

### 1. Create Game
```
POST /api/games/create/
```

**Description**: Create a new game session by specifying only the participant count. The server generates a unique match_id that will be distributed to all players.

**Request Body:**
```json
{
    "participant_count": 4
}
```

**Valid participant counts:** 1, 2, 4, 6
- 1 participant = Player vs Computer (no teams)
- 2+ participants = 2 teams (players assigned when they submit results)

**Response:**
```json
{
    "success": true,
    "game": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "participant_count": 4,
        "team_count": 2,
        "status": "waiting",
        "created_at": "2025-09-03T10:00:00Z"
    }
}
```

### 2. Submit Completed Game Result (Player-Centric)
```
POST /api/games/submit-completed/
```

**Description**: Each player individually submits their game result using the shared match_id. The system automatically generates appropriate responses and awards marks.

**Request Body:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 1,
    "username": "alice",
    "team": 1,
    "is_winner": true,
    "lost_card": null
}
```

**For Losers (include lost_card):**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 2,
    "username": "bob",
    "team": 2,
    "is_winner": false,
    "lost_card": "S3"
}
```

**Winner Response:**
```json
{
    "success": true,
    "message": "Game result submitted successfully",
    "player": {
        "player_id": 1,
        "username": "alice",
        "team": 1,
        "is_winner": true,
        "marks_earned": 1
    },
    "response": {
        "type": "explanation",
        "explanation": "Did you know that the 3 of Spades represents new beginnings and challenges?",
        "marks_earned": 1
    },
    "game_status": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "participants_submitted": 2,
        "participants_expected": 4,
        "status": "waiting",
        "completed": false
    }
}
```

**Loser Response:**
```json
{
    "success": true,
    "message": "Game result submitted successfully", 
    "player": {
        "player_id": 2,
        "username": "bob",
        "team": 2,
        "is_winner": false,
        "marks_earned": 0
    },
    "response": {
        "type": "question",
        "question": {
            "id": 123,
            "question_text": "What does the 3 of Spades traditionally represent?",
            "question_type": "multiple_choice",
            "options": ["New beginnings", "Challenges", "Both", "Neither"],
            "correct_answer": "Both",
            "explanation": "The 3 of Spades represents both new beginnings and challenges in traditional card meaning.",
            "points": 1,
            "difficulty": "easy",
            "card": "S3",
            "card_info": {
                "suit": "Spades",
                "value": "3",
                "pointValue": 0,
                "symbol": "♠",
                "id": "S3"
            }
        },
        "instruction": "Answer this question correctly to earn 1 mark"
    },
    "game_status": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "participants_submitted": 2,
        "participants_expected": 4,
        "status": "waiting",
        "completed": false
    }
}
```
**Request Body:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 3,
    "username": "player3",
    "question_id": 124,
    "answer": "The Battle of Waterloo",
    "points": 15
}
```

**Note**: Both `player_id` and `username` are required for proper player identification and database synchronization.
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

### 2. Submit Player Result
```
POST /api/games/submit-completed/
```

**Description**: Each player individually submits their game result using the shared match_id. Players submit whether they won or lost, along with their player information.

**Request Body for Winner:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 1,
    "username": "alice",
    "player_name": "Alice",
    "team": 1,
    "marks_earned": 1,
    "is_winner": true,
    "lost_card": null,
    "question_answered": false,
    "answer_correct": false
}
```

**Request Body for Loser:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 2,
    "username": "bob", 
    "player_name": "Bob",
    "team": 2,
    "marks_earned": 0,
    "is_winner": false,
    "lost_card": "S3",
    "question_answered": false,
    "answer_correct": false
}
```

**Response:**
```json
{
    "success": true,
    "message": "Player result submitted successfully",
    "player": {
        "player_id": 1,
        "username": "alice",
        "team": 1,
        "is_winner": true,
        "marks_earned": 1
    },
    "game_status": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "participants_submitted": 2,
        "participants_expected": 4,
        "status": "in_progress"
    }
}
```

**Note**: 
- Each player submits their individual result using the same match_id
- The game status will show how many players have submitted vs expected
- Once all players submit, the game status becomes "completed"

### 3. Get Player-Specific Game Responses
```
GET /api/games/{match_id}/responses/?player_id={player_id}
```

**Description**: Each player gets their specific response based on their win/loss status from the shared match_id. Winners get fun facts, losers get questions to answer.

**Example Request:**
```
GET /api/games/550e8400-e29b-41d4-a716-446655440000/responses/?player_id=1
```

**Response for Winner:**
```json
{
    "success": true,
    "player": {
        "player_id": 1,
        "username": "alice",
        "player_name": "Alice",
        "team": 1,
        "is_winner": true
    },
    "response": {
        "response_type": "fun_fact",
        "fun_fact": "Did you know that the heart suit represents emotions and love?",
        "card": "HJ",
        "card_info": {
            "suit": "Hearts",
            "value": "J",
            "pointValue": 3,
            "symbol": "♥"
        }
    }
}
```

**Response for Loser:**
```json
{
    "success": true,
    "player": {
        "player_id": 2,
        "username": "bob",
        "player_name": "Bob",
        "team": 2,
        "is_winner": false
    },
    "response": {
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
            "language": "kinyarwanda",
            "question_text": "What suit is associated with conflict?",
            "question_type": "multiple_choice",
            "options": ["Hearts", "Spades", "Clubs", "Diamonds"],
            "correct_answer": "Spades",
            "difficulty": "easy",
            "points": 1
        }
    }
}
```

### 4. Submit Answer
```
POST /api/games/submit-answer/
```

**Description**: Losing players submit their answers to the questions they received. This is the traditional endpoint that validates answers server-side.

**Request Body:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 2,
    "username": "bob",
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
        "points_earned": 1,
        "player": {
            "username": "bob",
            "total_correct_answers": 15,
            "total_questions_answered": 20,
            "answer_accuracy": 75.0
        }
    }
}
```

### 3. Award Points to Losers
```
POST /api/games/award-points/
```

**Description**: Award points to a losing player after the frontend validates their answer is correct. This endpoint is called by the frontend after it compares the player's answer with the `correct_answer` field from the question object.

**Request Body:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "username": "bob",
    "question_id": 123,
    "answer": "Both",
    "points": 1
}
```

**Response:**
```json
{
    "success": true,
    "message": "Awarded 1 point(s) to bob for correct answer",
    "result": {
        "points_awarded": 1,
        "player": {
            "username": "bob",
            "total_marks": 1,
            "total_correct_answers": 15,
            "total_questions_answered": 20,
            "answer_accuracy": 75.0
        },
        "question": {
            "id": 123,
            "explanation": "The 3 of Spades represents both new beginnings and challenges in traditional card meaning.",
            "points": 1
        }
    }
}
```

**Features:**
- Backend validates the answer for security (even though frontend already validated)
- Updates player's game marks and overall statistics
- Updates game result team marks
- Prevents duplicate point awards
- Returns explanation for educational value

### 4b. Record Wrong Answer
```
POST /api/games/record-wrong-answer/
```

**Description**: Record a wrong answer (no points awarded) after the UI validates the answer is incorrect.

**Request Body:**
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 2,
    "username": "player2",
    "question_id": 123,
    "answer": "Hearts"
}
```

**Note**: Both `player_id` and `username` are required for proper player identification and database synchronization.

**Response:**
```json
{
    "success": true,
    "result": {
        "points_awarded": 0,
        "correct_answer": "Spades",
        "explanation": "Spades represent conflict and challenges in card symbolism.",
        "player": {
            "username": "player2",
            "total_correct_answers": 14,
            "total_questions_answered": 20,
            "answer_accuracy": 70.0
        }
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
        "cards_chosen": ["S3", "HJ"],
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
                "cards_chosen": ["S3", "HJ"],
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

### 8. Get Questions by Card
```
GET /api/cards/{card_id}/questions/
```

Get all questions associated with a specific card (useful for UI to show available questions).

**Example:**
```bash
curl https://admin.hporwanda.org/api/cards/S3/questions/
```

**Response:**
```json
{
    "success": true,
    "card": "S3",
    "card_info": {
        "suit": "Spades",
        "value": "3",
        "pointValue": 0,
        "symbol": "♠",
        "id": "S3"
    },
    "count": 1,
    "questions": [
        {
            "id": 1,
            "language": "kinyarwanda",
            "question_text": "Capital City of Rwanda",
            "question_type": "multiple_choice",
            "options": ["Bujumbura", "Kampala", "Kigali", "Kinshasa"],
            "correct_answer": "Kigali",
            "explanation": "Kigali is the capital and largest city of Rwanda.",
            "points": 1,
            "difficulty": "easy",
            "card": "S3",
            "card_info": {
                "suit": "Spades",
                "value": "3",
                "pointValue": 0,
                "symbol": "♠",
                "id": "S3"
            },
            "created_at": "2025-08-21T22:06:17.364764+00:00"
        }
    ]
}
```

### 9. Get Leaderboard
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
Players on the **winning team** (based on their initial team assignment) receive fun facts from the `explanation` field of questions associated with cards chosen during gameplay.

### Loser Responses  
Players on the **losing team** (based on their initial team assignment) receive questions associated with the cards and must answer them to earn additional points.

### Card Assignment and Response Logic
When a game is completed:
1. Cards are chosen during gameplay (provided in the `cards_chosen` field)
2. **Losing team members** receive questions from the chosen cards
3. **Winning team members** receive fun facts (explanations) from questions associated with the same cards
4. If no specific cards are chosen, random cards are assigned

**Important Response Rules:**
- Team assignment determines response type: **losing team gets questions**, **winning team gets explanations**
- All players return to their **initial assigned teams** for response determination
- Questions contain both the question text (for losers) and explanation text (for winners)
- Winners automatically receive educational content without needing to answer questions

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

### Player-Centric Game Workflow (Recommended)

1. **Frontend creates a game with participant count:**
```bash
curl -X POST http://localhost:8000/api/games/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "participant_count": 4
  }'
```

Response contains match_id: `550e8400-e29b-41d4-a716-446655440000`

2. **Frontend distributes match_id to all players**

3. **Each player submits their individual result:**

**Alice (Winner) submits:**
```bash
curl -X POST http://localhost:8000/api/games/submit-completed/ \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 1,
    "username": "alice",
    "player_name": "Alice",
    "team": 1,
    "marks_earned": 1,
    "is_winner": true,
    "lost_card": null,
    "question_answered": false,
    "answer_correct": false
  }'
```

**Bob (Loser) submits:**
```bash
curl -X POST http://localhost:8000/api/games/submit-completed/ \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 2,
    "username": "bob",
    "player_name": "Bob",
    "team": 2,
    "marks_earned": 0,
    "is_winner": false,
    "lost_card": "S3",
    "question_answered": false,
    "answer_correct": false
  }'
```

4. **Each player gets their specific response:**

**Alice gets fun fact:**
```bash
curl "http://localhost:8000/api/games/550e8400-e29b-41d4-a716-446655440000/responses/?player_id=1"
```

**Bob gets question:**
```bash
curl "http://localhost:8000/api/games/550e8400-e29b-41d4-a716-446655440000/responses/?player_id=2"
```

5. **Losing players submit answers:**
```bash
curl -X POST http://localhost:8000/api/games/submit-answer/ \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "player_id": 2,
    "username": "bob",
    "answer": "Spades"
  }'
```

6. **Continue with UI Answer Validation Workflow (Optional):**

For more advanced UI interactions, losing players can also use:
- `/api/games/award-points/` for correct answers
- `/api/games/record-wrong-answer/` for incorrect answers

### Legacy Complete Game Workflow

For backward compatibility, the system still supports submitting complete game data all at once:

1. **Create a 2-player game:**
```bash
curl -X POST http://localhost:8000/api/games/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "participant_count": 2,
    "players": [
        {
            "player_id": 1,
            "team": 1
        },
        {
            "player_id": 2,
            "team": 2
        }
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
    "cards_chosen": ["HJ", "S3"]
  }'
```

3. **Get responses:**
```bash
curl http://localhost:8000/api/games/YOUR_MATCH_ID/responses/
```

4. **Bob's UI validates his answer and awards points (if correct):**
```bash
# If answer is correct:
curl -X POST http://localhost:8000/api/games/award-points/ \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "YOUR_MATCH_ID",
    "username": "bob",
    "question_id": 1,
    "answer": "Kigali",
    "points": 1
  }'

# If answer is wrong:
curl -X POST http://localhost:8000/api/games/record-wrong-answer/ \
  -H "Content-Type: application/json" \
  -d '{
    "match_id": "YOUR_MATCH_ID",
    "username": "bob",
    "question_id": 1,
    "answer": "Bujumbura"
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

### 10. Game Content API Endpoints

The system includes comprehensive game content management for educational materials in multiple languages and age groups.

#### 10a. Get Game Content
```
GET /api/game-content/
```

**Query Parameters:**
- `language`: Filter by language (english, kinyarwanda, french, swahili)
- `age_group`: Filter by age group (10-14, 15-19, 20-24, 25+)
- `topic`: Filter by topic (partial match)
- `subtopics`: Filter by subtopics (comma-separated)
- `content_type`: Filter by content type (educational, fun_fact, trivia, cultural, historical, scientific, general)
- `status`: Filter by status (default: published)

**Example:**
```bash
curl "http://localhost:8000/api/game-content/?language=english&age_group=15-19&topic=history"
```

**Response:**
```json
{
    "success": true,
    "count": 2,
    "filters_applied": {
        "language": "english",
        "age_group": "15-19",
        "topic": "history",
        "subtopics": null,
        "content_type": null,
        "status": "published"
    },
    "content": [
        {
            "id": 1,
            "title": "History of Rwanda",
            "language": "english",
            "age_group": "15-19",
            "topic": "History",
            "subtopics": ["Rwanda Independence", "Colonial Period", "Pre-colonial Rwanda"],
            "info": "Rwanda gained independence from Belgium on July 1, 1962...",
            "content_type": "historical",
            "difficulty_level": "intermediate",
            "status": "published",
            "tags": ["rwanda", "history", "independence", "africa"],
            "card_association": "S3",
            "view_count": 45,
            "usage_count": 12,
            "created_at": "2025-08-24T10:00:00Z",
            "updated_at": "2025-08-24T10:00:00Z"
        }
    ]
}
```

#### 10b. Get Game Content Detail
```
GET /api/game-content/{content_id}/
```

**Response:**
```json
{
    "success": true,
    "content": {
        "id": 1,
        "title": "History of Rwanda",
        "language": "english",
        "age_group": "15-19",
        "topic": "History",
        "subtopics": ["Rwanda Independence", "Colonial Period", "Pre-colonial Rwanda"],
        "info": "Detailed content information...",
        "content_type": "historical",
        "difficulty_level": "intermediate",
        "status": "published",
        "tags": ["rwanda", "history", "independence", "africa"],
        "card_association": "S3",
        "view_count": 46,
        "usage_count": 12,
        "created_at": "2025-08-24T10:00:00Z",
        "updated_at": "2025-08-24T10:00:00Z",
        "published_at": "2025-08-24T10:05:00Z",
        "created_by": {
            "name": "Admin User",
            "email": "admin@example.com"
        },
        "approved_by": {
            "name": "Admin User",
            "email": "admin@example.com"
        }
    }
}
```

#### 10c. Get Content by Language and Age Group
```
GET /api/game-content/{language}/{age_group}/
```

**Example:**
```bash
curl "http://localhost:8000/api/game-content/english/15-19/?topic=history"
```

#### 10d. Create Game Content
```
POST /api/game-content/create/
```

**Request Body:**
```json
{
    "title": "New Educational Content",
    "language": "english",
    "age_group": "15-19",
    "topic": "Science",
    "subtopics": ["Physics", "Chemistry", "Biology"],
    "info": "Detailed educational content...",
    "content_type": "educational",
    "difficulty_level": "intermediate",
    "status": "draft",
    "tags": "science, education, youth",
    "card_association": "DA"
}
```

**Response:**
```json
{
    "success": true,
    "content": {
        "id": 9,
        "title": "New Educational Content",
        "language": "english",
        "age_group": "15-19",
        "topic": "Science",
        "subtopics": ["Physics", "Chemistry", "Biology"],
        "status": "draft",
        "created_at": "2025-08-24T11:00:00Z"
    }
}
```

#### 10e. Increment Content Usage
```
POST /api/game-content/increment-usage/
```

**Request Body:**
```json
{
    "content_id": 1
}
```

**Response:**
```json
{
    "success": true,
    "content": {
        "id": 1,
        "title": "History of Rwanda",
        "usage_count": 13,
        "view_count": 46
    }
}
```

## Database Models

### Game
- `match_id`: Unique game identifier (UUID)
- `participant_count`: Number of players (1, 2, 4, 6)
- `team_count`: Calculated (1 for single player, 2 for multiplayer)
- `status`: waiting, active, completed, cancelled
- `winning_team`: 1 or 2 (null if not finished)
- `cards_chosen`: JSON list of cards chosen by losing players

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

### GameContent
- Stores educational content for games
- `title`: Content title
- `language`: Content language (english, kinyarwanda, french, swahili)
- `age_group`: Target age group (10-14, 15-19, 20-24, 25+)
- `topic`: Main topic/subject area
- `subtopics`: JSON array of related subtopics
- `info`: Main educational content
- `content_type`: Type of content (educational, fun_fact, trivia, cultural, historical, scientific, general)
- `difficulty_level`: Content difficulty (beginner, intermediate, advanced)
- `status`: Publication status (draft, review, approved, published, archived)
- `tags`: Comma-separated tags for categorization
- `card_association`: Optional card association
- `view_count`: Number of views
- `usage_count`: Number of times used in games

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
- For detailed player statistics implementation, see `PLAYER_STATISTICS_SUMMARY.md`
