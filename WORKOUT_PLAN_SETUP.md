# 🏋️‍♂️ Workout Plan Generation with LangGraph

## 🚀 Overview

The Macro Tracker now includes a sophisticated workout plan generation system using LangGraph (via LangChain4j). The workout plan generation uses a 4-step workflow that provides detailed, personalized workout routines based on user preferences and fitness goals.

## 🔧 Setup Instructions

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Compile the project
mvn clean compile

# Start the Spring Boot application
mvn spring-boot:run
```

### 2. Frontend Setup

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

The workout plan generation uses a 4-step LangGraph workflow:

1. **Analysis Step**: Analyzes user fitness profile and requirements
2. **Structure Step**: Creates workout structure and split
3. **Detailed Step**: Generates detailed workout routines
4. **Final Step**: Compiles progression plan and tips

### Key Components

- **`LangGraphWorkoutPlanService`**: Main service implementing the workflow
- **`WorkoutPlanRequest`**: DTO for workout plan requests
- **`WorkoutController`**: REST API endpoint
- **Frontend Form**: Comprehensive workout planning interface

## 📊 API Usage

### Generate Workout Plan

```bash
curl -X POST http://localhost:8080/api/workout/generate \
  -H "Content-Type: application/json" \
  -d '{
    "fitnessGoal": "strength",
    "experienceLevel": "beginner",
    "workoutsPerWeek": 3,
    "workoutDuration": 45,
    "availableEquipment": "minimal",
    "injuries": "",
    "preferences": ""
  }'
```

### Request Format

```json
{
  "fitnessGoal": "strength",           // strength, cardio, flexibility, weight_loss, muscle_gain, endurance
  "experienceLevel": "beginner",       // beginner, intermediate, advanced
  "workoutsPerWeek": 3,               // Number of workouts per week (2-6)
  "workoutDuration": 45,              // Workout duration in minutes (30-120)
  "availableEquipment": "minimal",     // none, minimal, home_equipment, full_gym
  "injuries": "",                     // Optional: comma-separated injuries/limitations
  "preferences": ""                   // Optional: workout preferences or dislikes
}
```

### Response Format

```json
{
  "goal": "strength",
  "experienceLevel": "beginner",
  "workoutsPerWeek": 3,
  "workoutDuration": 45,
  "weeklyWorkouts": [
    {
      "day": "Monday",
      "warmup": ["Dynamic stretching", "Light cardio"],
      "mainExercises": [
        {
          "name": "Squats",
          "sets": 3,
          "reps": 10,
          "restTime": 90,
          "instructions": "Stand with feet shoulder-width apart..."
        }
      ],
      "cooldown": ["Static stretching", "Foam rolling"],
      "progressionNotes": "Increase weight by 5-10% when 3 sets of 10 reps become easy",
      "formCues": ["Keep chest up", "Knees in line with toes"]
    }
  ],
  "progressionSchedule": [
    {
      "week": 1,
      "focus": "Form and technique",
      "notes": "Focus on proper form before increasing weight"
    }
  ],
  "exerciseLibrary": [
    {
      "name": "Squats",
      "category": "strength",
      "muscleGroup": "legs",
      "equipment": "barbell",
      "instructions": "Detailed form instructions..."
    }
  ],
  "nutritionRecommendations": {
    "protein": "1.6-2.2g per kg body weight",
    "carbs": "3-7g per kg body weight",
    "fats": "0.8-1.2g per kg body weight"
  },
  "recoveryGuidelines": [
    "Get 7-9 hours of sleep per night",
    "Stay hydrated throughout the day"
  ],
  "equipmentAlternatives": [
    {
      "original": "barbell squats",
      "alternatives": ["dumbbell squats", "goblet squats", "bodyweight squats"]
    }
  ],
  "progressTracking": [
    "Track weight lifted for each exercise",
    "Record number of reps completed",
    "Note how you feel after each workout"
  ]
}
```

## 🔄 Workflow Steps

### Step 1: Analysis
- Analyzes user fitness profile
- Determines appropriate workout split
- Identifies exercise selection criteria
- Recommends intensity and volume
- Plans progression strategy
- Considers safety and recovery

### Step 2: Structure
- Creates weekly workout schedule
- Plans focus areas for each day
- Determines exercise categories
- Schedules rest days
- Allocates time per exercise type

### Step 3: Detailed Routines
- Generates warm-up routines
- Creates main exercise programs
- Provides exercise alternatives
- Includes cool-down routines
- Adds progression notes
- Includes form cues and safety tips

### Step 4: Final Compilation
- Compiles complete workout plan
- Creates progression schedule
- Builds exercise library
- Provides nutrition recommendations
- Includes recovery guidelines
- Offers equipment alternatives
- Suggests progress tracking methods

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
# Test workout plan generation
curl -X POST http://localhost:8080/api/workout/generate \
  -H "Content-Type: application/json" \
  -d '{
    "fitnessGoal": "strength",
    "experienceLevel": "beginner",
    "workoutsPerWeek": 3,
    "workoutDuration": 45,
    "availableEquipment": "minimal",
    "injuries": "knee injury",
    "preferences": "prefer compound movements"
  }'
```

### Test Frontend

1. Open http://localhost:3000
2. Navigate to "Workouts" tab
3. Fill out the workout plan form:
   - Select fitness goal (strength, cardio, etc.)
   - Choose experience level
   - Set workouts per week
   - Specify workout duration
   - Select available equipment
   - Add any injuries/limitations
   - Include preferences
4. Click "Generate Personalized Workout Plan"

## 🎯 Fitness Goals

### Available Goals

- **Strength Training**: Build muscle and increase strength
- **Cardio & Endurance**: Improve cardiovascular fitness
- **Flexibility & Mobility**: Enhance range of motion
- **Weight Loss**: Create calorie deficit through exercise
- **Muscle Gain**: Focus on hypertrophy and progressive overload
- **Endurance**: Improve stamina and aerobic capacity

### Experience Levels

- **Beginner**: 0-6 months of consistent training
- **Intermediate**: 6 months - 2 years of training
- **Advanced**: 2+ years of structured training

### Equipment Options

- **No equipment**: Bodyweight exercises only
- **Minimal**: Dumbbells, resistance bands, basic equipment
- **Home gym**: More comprehensive home equipment
- **Full gym**: Access to commercial gym equipment

## 📈 Benefits of LangGraph Workout Planning

1. **Personalized Routines**: Tailored to individual goals and experience
2. **Progressive Programming**: Structured progression over time
3. **Safety First**: Considers injuries and limitations
4. **Equipment Flexibility**: Adapts to available equipment
5. **Comprehensive Guidance**: Includes nutrition, recovery, and tracking
6. **Scalable Workouts**: Can adjust difficulty and volume
7. **Educational**: Provides form cues and exercise explanations

## 🔮 Future Enhancements

- Add video demonstrations for exercises
- Implement workout tracking and progress monitoring
- Add social features (share workouts, compete with friends)
- Integrate with wearable devices
- Add AI-powered form analysis
- Create workout plan templates
- Add seasonal programming (bulk/cut cycles)

## 📝 Notes

- The LangGraph workflow uses LangChain4j for Java
- Each step is independent and can be modified separately
- The workflow is designed to be fault-tolerant
- Responses are cached to improve performance
- All API calls are logged for monitoring
- The system adapts to different fitness levels and goals
- Safety considerations are built into every step

## 🆘 Troubleshooting

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

4. **Workout Plan Too Complex/Simple**
   - Adjust the experience level
   - Modify the fitness goal
   - Change the number of workouts per week

### Logs

Check backend logs for detailed error information:
```bash
cd backend
mvn spring-boot:run
```

---

**Ready to get fit!** 🏋️‍♂️💪 