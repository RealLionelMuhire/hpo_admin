# Complete Game Submission Workflow

## Overview

The system now supports submitting complete game data from the UI, ensuring proper synchronization across all Django models. This new workflow is designed for scenarios where the UI manages the entire game session and submits the final results to the backend.

## New Endpoint: Submit Completed Game

**URL**: `POST /api/games/submit-completed/`

**Purpose**: Submit a fully completed game with all participant data, ensuring synchronization with:
- **Games** model (main game record)
- **GameParticipants** model (player participation records)
- **GameResponses** model (winner fun facts and loser questions)
- **GameResults** model (final game outcome)
- **Players** model (updated statistics)
- **Questions** model (attempt count tracking)

## Required Data Structure

### Game Data
```json
{
    "match_id": "550e8400-e29b-41d4-a716-446655440000",
    "game_data": {
        "participant_count": 2,
        "winning_team": 1,
        "cards_chosen": ["S3", "HJ"],
        "game_duration": 300,
        "created_at": "2025-08-23T10:00:00Z",
        "completed_at": "2025-08-23T10:05:00Z"
    }
}
```

### Players Data (with Player IDs for Sync)
```json
{
    "players": [
        {
            "player_id": 1,          // REQUIRED for database sync
            "username": "alice",
            "player_name": "Alice",
            "team": 1,
            "marks_earned": 1,
            "is_winner": true,
            "lost_card": null,
            "question_answered": false,
            "answer_correct": false
        },
        {
            "player_id": 2,          // REQUIRED for database sync
            "username": "bob", 
            "player_name": "Bob",
            "team": 2,
            "marks_earned": 0,
            "is_winner": false,
            "lost_card": "S3",
            "question_answered": false,
            "answer_correct": false
        }
    ]
}
```

### Responses Data
```json
{
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
            "question_id": 123,
            "card": "S3"
        }
    ]
}
```

## Model Synchronization

### 1. Games Model
- Creates new `Game` record with status 'completed'
- Sets winning team, cards chosen, timestamps
- Links to all participants

### 2. GameParticipants Model  
- Creates `GameParticipant` record for each player
- Uses `player_id` to link to existing `Player` records
- Tracks team, winner status, marks earned, cards lost
- Records question answering status

### 3. GameResponses Model
- Creates `GameResponse` records for each player
- Winners get fun_fact responses
- Losers get question responses linked to specific questions
- Enables later answer tracking

### 4. GameResults Model
- Creates `GameResult` record with team marks
- Stores comprehensive result summary
- Tracks game duration and completion details

### 5. Players Model (Statistics Update)
- Updates game statistics using `update_game_stats()` method
- Increments games played, wins/losses, marks earned
- Updates win streaks and accuracy percentages
- Records last game played timestamp

### 6. Questions Model (Reference Linking)
- Links questions to game responses for tracking
- Enables question analytics through response data
- Questions remain unchanged (no attempt counting at question level)

## Validation and Error Handling

### Required Field Validation
- `match_id`: Must be unique (prevents duplicate games)
- `game_data`: participant_count, winning_team, cards_chosen
- `players`: player_id, username, team, is_winner
- `player_id`: Must exist in database (enforces sync)

### Card Validation
- Validates cards against `Question.CARD_CHOICES`
- Ensures only valid card IDs are accepted

### Player Sync Validation
- Checks that all `player_id`s exist in the database
- Updates player info if username/name changes
- Returns error if player ID not found

### Transaction Safety
- Uses `transaction.atomic()` for data consistency
- Rollback on any error during creation process
- Ensures all-or-nothing data updates

## Response Data

### Success Response
```json
{
    "success": true,
    "game": {
        "match_id": "550e8400-e29b-41d4-a716-446655440000",
        "status": "completed",
        "participant_count": 2,
        "team_count": 2,
        "winning_team": 1,
        "cards_chosen": ["S3", "HJ"],
        "created_at": "2025-08-23T10:00:00Z",
        "completed_at": "2025-08-23T10:05:00Z",
        "participants": [
            {
                "player_id": 1,
                "username": "alice",
                "player_name": "Alice",
                "team": 1,
                "is_winner": true,
                "marks_earned": 1,
                "lost_card": null,
                "question_answered": false,
                "answer_correct": false
            }
        ],
        "result": {
            "team1_marks": 1,
            "team2_marks": 0,
            "result_summary": {
                "winning_team": 1,
                "cards_chosen": ["S3", "HJ"],
                "completed_at": "2025-08-23T10:05:00Z",
                "game_duration": 300
            }
        }
    },
    "sync_status": {
        "players_updated": 2,
        "participants_created": 2,
        "responses_created": 2,
        "questions_linked": 1
    }
}
```

### Sync Status Details
- `players_updated`: Number of player records updated
- `participants_created`: Number of game participants created
- `responses_created`: Number of game responses created
- `questions_linked`: Number of questions linked to responses

## Benefits of This Approach

### 1. Complete Data Integrity
- All related models updated in single transaction
- No orphaned records or incomplete game states
- Consistent state across entire system

### 2. Player Synchronization
- Uses player IDs for reliable database linking
- Updates player statistics automatically
- Maintains player identity across games

### 3. Question Analytics
- Tracks question usage and difficulty
- Enables game balancing based on question performance
- Supports question recommendation algorithms

### 4. Game Auditability
- Complete game history with all participants
- Detailed response tracking for analysis
- Comprehensive game duration and timing data

### 5. Scalable Architecture
- Single endpoint handles complex game submission
- Reduces API calls from UI
- Enables batch processing of game data

## Integration with Existing Features

### Compatible with UI-Driven Answer Validation
After submitting a completed game, the UI can still use:
- `/api/games/award-points/` for correct answers
- `/api/games/record-wrong-answer/` for incorrect answers
- `/api/cards/{card_id}/questions/` for question data

### Admin Interface Integration
- All submitted data appears in Django admin
- Game monitoring and management
- Player statistics tracking
- Question usage analytics

### Leaderboard and Statistics
- Player stats automatically updated
- Leaderboard reflects new game results
- Win streaks and accuracy calculated

## Example Complete Workflow

```javascript
// 1. UI collects game data during gameplay
const gameData = {
    match_id: generateUUID(),
    game_data: {
        participant_count: 2,
        winning_team: 1,
        cards_chosen: ["S3", "HJ"],
        game_duration: 300
    },
    players: [
        {
            player_id: 1,
            username: "alice",
            team: 1,
            is_winner: true,
            marks_earned: 1
        },
        {
            player_id: 2,
            username: "bob",
            team: 2,
            is_winner: false,
            marks_earned: 0,
            lost_card: "S3"
        }
    ],
    responses: [
        {
            player_id: 1,
            response_type: "fun_fact",
            fun_fact_text: "Spades represent challenges!",
            card: "S3"
        },
        {
            player_id: 2,
            response_type: "question",
            question_id: 123,
            card: "S3"
        }
    ]
};

// 2. Submit complete game to backend
const response = await fetch('/api/games/submit-completed/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(gameData)
});

const result = await response.json();

// 3. Handle response and sync status
if (result.success) {
    console.log('Game submitted successfully');
    console.log('Sync Status:', result.sync_status);
    
    // Continue with answer validation if needed
    // UI can still call award-points or record-wrong-answer
} else {
    console.error('Game submission failed:', result.error);
}
```

This new workflow ensures complete data synchronization while maintaining compatibility with existing UI-driven answer validation features.
