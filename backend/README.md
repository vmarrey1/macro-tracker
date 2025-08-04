# Macro Tracker Backend

Spring Boot backend for the Macro Tracker application.

## Features (Planned)

- RESTful API for food image analysis
- Integration with computer vision services
- LLM integration for meal and workout planning
- User authentication and data persistence
- Real-time macro calculation

## Tech Stack

- Spring Boot 3.x
- Spring Security
- Spring Data JPA
- PostgreSQL/MySQL
- OpenCV/TensorFlow for image processing
- OpenAI/Anthropic API for LLM integration

## Getting Started

### Prerequisites
- Java 17 or higher
- Maven 3.6+
- Database (PostgreSQL/MySQL)

### Setup
```bash
# Clone the repository
git clone <repository-url>

# Navigate to backend
cd backend

# Build the project
mvn clean install

# Run the application
mvn spring-boot:run
```

The API will be available at `http://localhost:8080`

## API Endpoints (Planned)

### Food Analysis
- `POST /api/food/analyze` - Analyze food image and return macros
- `GET /api/food/history` - Get user's food analysis history

### Meal Planning
- `POST /api/meal-plan/generate` - Generate personalized meal plan
- `GET /api/meal-plan/current` - Get current meal plan

### Workout Planning
- `POST /api/workout/generate` - Generate personalized workout plan
- `GET /api/workout/current` - Get current workout plan

### User Management
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/user/profile` - Get user profile

## Development Status

🚧 **Under Development** 🚧

This backend is currently in the planning phase. The frontend is ready and can be connected once the backend APIs are implemented. 