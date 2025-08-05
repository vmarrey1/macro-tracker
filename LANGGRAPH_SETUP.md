# LangGraph Integration for Macro Tracker

## 🚀 Overview

This project now includes LangGraph (via LangChain4j) for sophisticated LLM workflow management. The meal plan generation uses a multi-step workflow that provides more detailed and structured meal plans.

## 🔧 Setup Instructions

### 1. OpenAI API Key Setup

First, set up your OpenAI API key:

```bash
# Run the setup script
./setup-api-key.sh

# Or manually set the API key
export OPENAI_API_KEY='sk-your-api-key-here'
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Compile the project
mvn clean compile

# Start the Spring Boot application
mvn spring-boot:run
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the React application
npm start
```

## 🏗️ Architecture

### LangGraph Workflow

The meal plan generation now uses a 4-step LangGraph workflow:

1. **Analysis Step**: Analyzes user preferences and requirements
2. **Structure Step**: Creates a 7-day meal structure
3. **Detailed Step**: Generates detailed recipes for each meal
4. **Final Step**: Compiles shopping list and meal prep tips

### Key Components

- **`LangGraphMealPlanService`**: Main service implementing the workflow
- **`LangGraphConfig`**: Configuration for LangChain4j
- **`MealPlanController`**: REST API endpoint
- **`MealPlanRequest`**: DTO for meal plan requests

## 📊 API Usage

### Generate Meal Plan

```bash
curl -X POST http://localhost:8080/api/meal-plan/generate \
  -H "Content-Type: application/json" \
  -d '{
    "idealCalories": 2000,
    "favoriteFoods": "chicken, rice, vegetables, eggs, yogurt",
    "numberOfMeals": 3,
    "dietaryRestrictions": "",
    "allergies": ""
  }'
```

### Request Format

```json
{
  "idealCalories": 2000,           // Daily calorie target (1200-5000)
  "favoriteFoods": "chicken, rice", // Comma-separated favorite foods
  "numberOfMeals": 3,              // Number of meals per day (2-6)
  "dietaryRestrictions": "",        // Optional dietary restrictions
  "allergies": ""                   // Optional allergies
}
```

### Response Format

```json
{
  "dailyCalories": 2000,
  "weeklyPlan": [
    {
      "day": "Monday",
      "meals": [
        {
          "name": "Protein Bowl",
          "type": "breakfast",
          "calories": 450,
          "protein": 35,
          "carbs": 45,
          "fat": 15,
          "ingredients": "chicken, quinoa, vegetables...",
          "instructions": "1. Cook quinoa...",
          "prepTime": "10 minutes",
          "cookTime": "20 minutes"
        }
      ]
    }
  ],
  "shoppingList": ["chicken breast", "quinoa", "vegetables"],
  "mealPrepTips": ["Cook quinoa in bulk...", "Pre-chop vegetables..."]
}
```

## 🔄 Workflow Steps

### Step 1: Analysis
- Analyzes user requirements
- Determines calorie distribution
- Identifies nutritional considerations
- Suggests food categories

### Step 2: Structure
- Creates 7-day meal themes
- Plans meal timing
- Distributes calories per meal
- Identifies key ingredients

### Step 3: Detailed Recipes
- Generates complete recipes
- Includes ingredients and quantities
- Provides step-by-step instructions
- Calculates nutritional information

### Step 4: Final Compilation
- Compiles complete meal plan
- Creates shopping list
- Provides meal prep tips
- Includes nutritional summary

## 🛠️ Configuration

### Application Properties

```yaml
# LLM Configuration
llm:
  openai:
    api-key: ${OPENAI_API_KEY:your-openai-api-key}
    model: gpt-4
    max-tokens: 2000
    temperature: 0.7
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
LLM_OPENAI_MODEL=gpt-4
LLM_OPENAI_MAX_TOKENS=2000
LLM_OPENAI_TEMPERATURE=0.7
```

## 🧪 Testing

### Test the API

```bash
# Test meal plan generation
curl -X POST http://localhost:8080/api/meal-plan/generate \
  -H "Content-Type: application/json" \
  -d '{
    "idealCalories": 2000,
    "favoriteFoods": "chicken, rice, vegetables, eggs, yogurt",
    "numberOfMeals": 3,
    "dietaryRestrictions": "vegetarian",
    "allergies": "nuts"
  }'
```

### Test Frontend

1. Open http://localhost:3000
2. Navigate to "Meal Plans" tab
3. Fill out the form
4. Click "Generate 7-Day Meal Plan"

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```bash
   export OPENAI_API_KEY='sk-your-api-key-here'
   ```

2. **Backend Won't Start**
   ```bash
   cd backend
   mvn clean compile
   mvn spring-boot:run
   ```

3. **Frontend Won't Start**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **CORS Issues**
   - Backend is configured to allow requests from http://localhost:3000
   - Check that both frontend and backend are running

### Logs

Check backend logs for detailed error information:
```bash
cd backend
mvn spring-boot:run
```

## 📈 Benefits of LangGraph

1. **Structured Workflow**: Multi-step process ensures comprehensive meal plans
2. **Better Quality**: Each step builds upon the previous for better results
3. **Error Handling**: Graceful handling of failures at each step
4. **Scalability**: Easy to add new steps or modify existing ones
5. **Debugging**: Clear separation of concerns for easier troubleshooting

## 🔮 Future Enhancements

- Add workout plan generation workflow
- Implement user preference learning
- Add meal plan customization options
- Integrate with nutrition databases
- Add meal plan sharing features

## 📝 Notes

- The LangGraph workflow uses LangChain4j for Java
- Each step is independent and can be modified separately
- The workflow is designed to be fault-tolerant
- Responses are cached to improve performance
- All API calls are logged for monitoring 