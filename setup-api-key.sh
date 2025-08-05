#!/bin/bash

echo "🔑 OpenAI API Key Setup for Macro Tracker"
echo "=========================================="

# Function to check if API key is valid format
check_api_key() {
    local key=$1
    if [[ $key =~ ^sk-[A-Za-z0-9]{48}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Check if OPENAI_API_KEY is already set
if [ -n "$OPENAI_API_KEY" ]; then
    if check_api_key "$OPENAI_API_KEY"; then
        echo "✅ OPENAI_API_KEY is already set and appears valid"
        echo "Current key: ${OPENAI_API_KEY:0:10}..."
    else
        echo "⚠️  OPENAI_API_KEY is set but format appears invalid"
        echo "Current key: ${OPENAI_API_KEY:0:10}..."
    fi
else
    echo "❌ OPENAI_API_KEY is not set"
fi

echo ""
echo "📋 Setup Instructions:"
echo "1. Go to https://platform.openai.com/api-keys"
echo "2. Sign in or create an account"
echo "3. Click 'Create new secret key'"
echo "4. Copy the key (starts with 'sk-')"
echo "5. Choose one of the setup methods below:"
echo ""

echo "🔧 Setup Methods:"
echo ""
echo "Method 1 - Set for current session:"
echo "export OPENAI_API_KEY='sk-your-api-key-here'"
echo ""
echo "Method 2 - Add to your shell profile (recommended):"
echo "echo 'export OPENAI_API_KEY=\"sk-your-api-key-here\"' >> ~/.zshrc"
echo "source ~/.zshrc"
echo ""
echo "Method 3 - Create a .env file:"
echo "echo 'OPENAI_API_KEY=sk-your-api-key-here' > .env"
echo ""

echo "🧪 Test the API:"
echo "After setting the key, restart the backend and test with:"
echo "curl -X POST http://localhost:8080/api/meal-plan/generate \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"idealCalories\": 2000, \"favoriteFoods\": \"chicken, rice\", \"numberOfMeals\": 3}'"
echo ""

echo "🚀 Start the backend:"
echo "cd backend && mvn spring-boot:run"
echo ""

echo "🌐 Access the application:"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8080" 