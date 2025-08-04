# Development Guide

## Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Git

### Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd Macro-Tracker

# Install frontend dependencies
npm run install-deps

# Start the development server
npm start
```

The application will be available at `http://localhost:3000`

## Project Structure

```
Macro-Tracker/
├── frontend/          # React.js application
│   ├── src/          # Source code
│   ├── public/       # Static assets
│   └── package.json  # Frontend dependencies
├── backend/          # Spring Boot backend (coming soon)
├── ml-models/        # Computer vision models
├── docs/            # Documentation
└── README.md        # Project overview
```

## Development Workflow

### Frontend Development
1. Navigate to the frontend directory: `cd frontend`
2. Start the development server: `npm start`
3. Make changes to the code
4. The app will automatically reload with changes

### Backend Development (Future)
1. Navigate to the backend directory: `cd backend`
2. Set up Spring Boot project
3. Run with: `mvn spring-boot:run`

### ML Model Development (Future)
1. Navigate to the ml-models directory
2. Set up Python environment
3. Develop and test models

## Features Implemented

### ✅ Completed
- [x] Project structure and Git repository
- [x] React frontend with modern UI
- [x] Food image upload functionality
- [x] Mock macro analysis results
- [x] Responsive design
- [x] Navigation between different sections
- [x] Beautiful gradient design with glassmorphism effects

### 🚧 In Progress
- [ ] Backend API development
- [ ] Computer vision integration
- [ ] LLM integration for meal planning
- [ ] User authentication

### 📋 Planned
- [ ] Database integration
- [ ] Real-time macro calculation
- [ ] Progress tracking
- [ ] Mobile app development

## Tech Stack

### Frontend
- **React.js** - UI framework
- **Lucide React** - Icon library
- **CSS3** - Styling with modern features
- **HTML5** - Semantic markup

### Backend (Planned)
- **Spring Boot** - Java framework
- **Spring Security** - Authentication
- **Spring Data JPA** - Database access
- **PostgreSQL/MySQL** - Database

### ML/AI (Planned)
- **TensorFlow/PyTorch** - Deep learning
- **OpenCV** - Computer vision
- **OpenAI/Anthropic** - LLM integration

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Commit your changes: `git commit -m 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## Code Style

### Frontend
- Use functional components with hooks
- Follow React best practices
- Use meaningful component and variable names
- Add comments for complex logic

### Backend (Future)
- Follow Spring Boot conventions
- Use proper Java naming conventions
- Add comprehensive unit tests
- Document API endpoints

## Testing

### Frontend Testing
```bash
cd frontend
npm test
```

### Backend Testing (Future)
```bash
cd backend
mvn test
```

## Deployment

### Frontend
```bash
cd frontend
npm run build
```

### Backend (Future)
```bash
cd backend
mvn clean package
```

## Troubleshooting

### Common Issues

1. **Port 3000 already in use**
   - Kill the process: `lsof -ti:3000 | xargs kill -9`
   - Or use a different port: `PORT=3001 npm start`

2. **Node modules issues**
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

3. **Git issues**
   - Check git status: `git status`
   - Reset if needed: `git reset --hard HEAD`

## Support

For questions or issues, please create an issue in the GitHub repository. 