#!/bin/bash

echo "🔑 Setting up OpenAI API Key for Macro Tracker"
echo "================================================"

# Check if OPENAI_API_KEY is already set
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OPENAI_API_KEY is already set"
    echo "Current key: ${OPENAI_API_KEY:0:10}..."
else
    echo "❌ OPENAI_API_KEY is not set"
    echo ""
    echo "To set up your OpenAI API key:"
    echo "1. Go to https://platform.openai.com/api-keys"
    echo "2. Create a new API key"
    echo "3. Run one of these commands:"
    echo ""
    echo "   Option 1 - Set for current session:"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "   Option 2 - Add to your shell profile (recommended):"
    echo "   echo 'export OPENAI_API_KEY=\"your-api-key-here\"' >> ~/.zshrc"
    echo "   source ~/.zshrc"
    echo ""
    echo "   Option 3 - Create a .env file:"
    echo "   echo 'OPENAI_API_KEY=your-api-key-here' > .env"
    echo ""
    echo "After setting the API key, restart the backend application."
fi

echo ""
echo "🔧 Current Configuration:"
echo "Backend URL: http://localhost:8080"
echo "Frontend URL: http://localhost:3000"
echo ""
echo "To test the API after setting the key:"
echo "curl -X POST http://localhost:8080/api/meal-plan/generate \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"idealCalories\": 2000, \"favoriteFoods\": \"chicken, rice\", \"numberOfMeals\": 3}'" 