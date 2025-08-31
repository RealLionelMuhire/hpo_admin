#!/bin/bash
# GameContent GET API - cURL Commands

echo "🌐 GameContent GET API - cURL Commands"
echo "======================================"
echo

echo "1. Get All Game Content:"
echo "curl -X GET \"http://localhost:8000/api/game-content/\" -H \"Content-Type: application/json\""
echo

echo "2. Get Filtered Game Content (English only):"
echo "curl -X GET \"http://localhost:8000/api/game-content/?language=english\" -H \"Content-Type: application/json\""
echo

echo "3. Get Content by Age Group:"
echo "curl -X GET \"http://localhost:8000/api/game-content/?age_group=15-19\" -H \"Content-Type: application/json\""
echo

echo "4. Get Content by Topic:"
echo "curl -X GET \"http://localhost:8000/api/game-content/?topic=history\" -H \"Content-Type: application/json\""
echo

echo "5. Get Content by Subtopic:"
echo "curl -X GET \"http://localhost:8000/api/game-content/?subtopic=world%20war\" -H \"Content-Type: application/json\""
echo

echo "6. Get Content by Type:"
echo "curl -X GET \"http://localhost:8000/api/game-content/?content_type=fact\" -H \"Content-Type: application/json\""
echo

echo "7. Get Draft Content (admin):"
echo "curl -X GET \"http://localhost:8000/api/game-content/?status=draft\" -H \"Content-Type: application/json\""
echo

echo "8. Multiple Filters:"
echo "curl -X GET \"http://localhost:8000/api/game-content/?language=english&age_group=15-19&content_type=fact\" -H \"Content-Type: application/json\""
echo

echo "9. Get Specific Content by ID:"
echo "curl -X GET \"http://localhost:8000/api/game-content/1/\" -H \"Content-Type: application/json\""
echo

echo "10. Get Content by Language and Age:"
echo "curl -X GET \"http://localhost:8000/api/game-content/english/15-19/\" -H \"Content-Type: application/json\""
echo

echo "🎮 BONUS: Game Creation API (Updated Format):"
echo "============================================="
echo
echo "Create Game with Player IDs (New Format):"
echo "curl -X POST \"http://localhost:8000/api/games/create/\" \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{"
echo "    \"participant_count\": 2,"
echo "    \"players\": [1, 2]"
echo "  }'"
echo

echo "📋 Available GameContent Filter Parameters:"
echo "==========================================="
echo "• language: english, french, kinyarwanda"
echo "• age_group: 6-10, 11-14, 15-19, 20+"
echo "• topic: (partial text match)"
echo "• subtopic: (partial text match)"
echo "• content_type: question, fact, story, challenge"
echo "• status: draft, published, archived"
