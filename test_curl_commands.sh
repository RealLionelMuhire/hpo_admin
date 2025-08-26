#!/bin/bash

# GameContent API cURL Test Script
# Make sure your Django server is running on localhost:8000

echo "🚀 Testing GameContent GET API Endpoints"
echo "========================================="

BASE_URL="http://localhost:8000"

echo ""
echo "1️⃣ Testing: Get All Content"
curl -s -X GET "$BASE_URL/api/game-content/" \
  -H "Content-Type: application/json" | jq '.success, .count'

echo ""
echo "2️⃣ Testing: Get English Content"
curl -s -X GET "$BASE_URL/api/game-content/?language=english" \
  -H "Content-Type: application/json" | jq '.success, .count, .filters_applied'

echo ""
echo "3️⃣ Testing: Get Content by ID (ID=1)"
curl -s -X GET "$BASE_URL/api/game-content/1/" \
  -H "Content-Type: application/json" | jq '.success, .content.title // "Not found"'

echo ""
echo "4️⃣ Testing: Get Content by Language/Age"
curl -s -X GET "$BASE_URL/api/game-content/english/15-19/" \
  -H "Content-Type: application/json" | jq '.success, .count'

echo ""
echo "5️⃣ Testing: Multiple Filters"
curl -s -X GET "$BASE_URL/api/game-content/?language=english&content_type=fact&status=published" \
  -H "Content-Type: application/json" | jq '.success, .count, .filters_applied'

echo ""
echo "✅ Test completed! Check the responses above."
echo ""
echo "💡 Available endpoints:"
echo "   GET $BASE_URL/api/game-content/"
echo "   GET $BASE_URL/api/game-content/{id}/"
echo "   GET $BASE_URL/api/game-content/{language}/{age_group}/"
