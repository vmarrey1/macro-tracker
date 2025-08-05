import React, { useState } from 'react';
import './App.css';
import { Camera, Upload, Target, Activity, Utensils, TrendingUp, Zap } from 'lucide-react';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [activeTab, setActiveTab] = useState('analyze');

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setSelectedImage(e.target.result);
        setAnalysisResult(null);
      };
      reader.readAsDataURL(file);
    }
  };

  const analyzeImage = async () => {
    if (!selectedImage) return;
    
    setIsAnalyzing(true);
    // Simulate API call - replace with actual backend call
    setTimeout(() => {
      setAnalysisResult({
        food: "Grilled Chicken Breast with Vegetables",
        calories: 320,
        protein: 35,
        carbs: 12,
        fat: 8,
        fiber: 6
      });
      setIsAnalyzing(false);
    }, 2000);
  };

  const generateMealPlan = async () => {
    try {
      const calories = document.getElementById('calories').value;
      const favoriteFoods = document.getElementById('favoriteFoods').value;
      const numberOfMeals = document.getElementById('numberOfMeals').value;
      const dietaryRestrictions = document.getElementById('dietaryRestrictions').value;
      const allergies = document.getElementById('allergies').value;

      const response = await fetch('http://localhost:8080/api/meal-plan/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          idealCalories: parseInt(calories),
          favoriteFoods: favoriteFoods,
          numberOfMeals: parseInt(numberOfMeals),
          dietaryRestrictions: dietaryRestrictions,
          allergies: allergies
        })
      });
      
      const data = await response.json();
      console.log("Generated meal plan:", data);
      
      // Display the meal plan in a modal or new section
      alert("Meal plan generated! Check the console for details.");
    } catch (error) {
      console.error("Error generating meal plan:", error);
      alert("Error generating meal plan. Please try again.");
    }
  };

  const generateWorkout = () => {
    // Simulate workout generation
    console.log("Generating workout plan...");
  };

  return (
    <div className="App">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <Target className="logo-icon" />
            <h1>Macro Tracker</h1>
          </div>
          <nav className="nav">
            <button 
              className={`nav-btn ${activeTab === 'analyze' ? 'active' : ''}`}
              onClick={() => setActiveTab('analyze')}
            >
              <Camera size={20} />
              Analyze Food
            </button>
            <button 
              className={`nav-btn ${activeTab === 'meal-plan' ? 'active' : ''}`}
              onClick={() => setActiveTab('meal-plan')}
            >
              <Utensils size={20} />
              Meal Plans
            </button>
            <button 
              className={`nav-btn ${activeTab === 'workout' ? 'active' : ''}`}
              onClick={() => setActiveTab('workout')}
            >
              <Activity size={20} />
              Workouts
            </button>
            <button 
              className={`nav-btn ${activeTab === 'progress' ? 'active' : ''}`}
              onClick={() => setActiveTab('progress')}
            >
              <TrendingUp size={20} />
              Progress
            </button>
          </nav>
        </div>
      </header>

      <main className="main-content">
        {activeTab === 'analyze' && (
          <div className="analyze-section">
            <div className="upload-area">
              <div className="upload-card">
                <div className="upload-icon">
                  <Upload size={48} />
                </div>
                <h2>Upload Food Image</h2>
                <p>Take a photo or upload an image of your food to get instant macro analysis</p>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  id="image-upload"
                  className="file-input"
                />
                <label htmlFor="image-upload" className="upload-button">
                  Choose Image
                </label>
              </div>
            </div>

            {selectedImage && (
              <div className="image-preview">
                <img src={selectedImage} alt="Selected food" className="preview-image" />
                <button 
                  className="analyze-button"
                  onClick={analyzeImage}
                  disabled={isAnalyzing}
                >
                  {isAnalyzing ? (
                    <>
                      <div className="spinner"></div>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Zap size={20} />
                      Analyze Macros
                    </>
                  )}
                </button>
              </div>
            )}

            {analysisResult && (
              <div className="results-section">
                <h3>Analysis Results</h3>
                <div className="food-info">
                  <h4>{analysisResult.food}</h4>
                </div>
                <div className="macros-grid">
                  <div className="macro-card calories">
                    <div className="macro-icon">🔥</div>
                    <div className="macro-content">
                      <h5>Calories</h5>
                      <p>{analysisResult.calories} kcal</p>
                    </div>
                  </div>
                  <div className="macro-card protein">
                    <div className="macro-icon">💪</div>
                    <div className="macro-content">
                      <h5>Protein</h5>
                      <p>{analysisResult.protein}g</p>
                    </div>
                  </div>
                  <div className="macro-card carbs">
                    <div className="macro-icon">🌾</div>
                    <div className="macro-content">
                      <h5>Carbs</h5>
                      <p>{analysisResult.carbs}g</p>
                    </div>
                  </div>
                  <div className="macro-card fat">
                    <div className="macro-icon">🥑</div>
                    <div className="macro-content">
                      <h5>Fat</h5>
                      <p>{analysisResult.fat}g</p>
                    </div>
                  </div>
                  <div className="macro-card fiber">
                    <div className="macro-icon">🌿</div>
                    <div className="macro-content">
                      <h5>Fiber</h5>
                      <p>{analysisResult.fiber}g</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'meal-plan' && (
          <div className="meal-plan-section">
            <div className="section-header">
              <h2>AI-Powered Meal Planning</h2>
              <p>Create personalized 7-day meal plans based on your preferences</p>
            </div>
            <div className="meal-plan-form">
              <div className="form-group">
                <label htmlFor="calories">Daily Calorie Target</label>
                <input 
                  type="number" 
                  id="calories" 
                  placeholder="e.g., 2000" 
                  min="1200" 
                  max="5000"
                  defaultValue="2000"
                />
              </div>
              <div className="form-group">
                <label htmlFor="favoriteFoods">Favorite Foods</label>
                <input 
                  type="text" 
                  id="favoriteFoods" 
                  placeholder="e.g., chicken, rice, vegetables, eggs, yogurt"
                  defaultValue="chicken, rice, vegetables, eggs, yogurt"
                />
              </div>
              <div className="form-group">
                <label htmlFor="numberOfMeals">Number of Meals per Day</label>
                <select id="numberOfMeals" defaultValue="3">
                  <option value="2">2 meals</option>
                  <option value="3">3 meals</option>
                  <option value="4">4 meals</option>
                  <option value="5">5 meals</option>
                  <option value="6">6 meals</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="dietaryRestrictions">Dietary Restrictions (optional)</label>
                <input 
                  type="text" 
                  id="dietaryRestrictions" 
                  placeholder="e.g., vegetarian, gluten-free"
                />
              </div>
              <div className="form-group">
                <label htmlFor="allergies">Allergies (optional)</label>
                <input 
                  type="text" 
                  id="allergies" 
                  placeholder="e.g., nuts, dairy"
                />
              </div>
              <button className="generate-plan-button" onClick={generateMealPlan}>
                Generate 7-Day Meal Plan
              </button>
            </div>
          </div>
        )}

        {activeTab === 'workout' && (
          <div className="workout-section">
            <div className="section-header">
              <h2>Personalized Workout Plans</h2>
              <p>Get custom workout routines tailored to your fitness level and goals</p>
            </div>
            <div className="workout-cards">
              <div className="workout-card">
                <div className="workout-icon">🏃‍♂️</div>
                <h3>Cardio</h3>
                <p>Improve endurance and burn calories</p>
                <button className="workout-button" onClick={generateWorkout}>
                  Generate Workout
                </button>
              </div>
              <div className="workout-card">
                <div className="workout-icon">🏋️‍♂️</div>
                <h3>Strength</h3>
                <p>Build muscle and increase strength</p>
                <button className="workout-button" onClick={generateWorkout}>
                  Generate Workout
                </button>
              </div>
              <div className="workout-card">
                <div className="workout-icon">🧘‍♀️</div>
                <h3>Flexibility</h3>
                <p>Improve mobility and reduce injury risk</p>
                <button className="workout-button" onClick={generateWorkout}>
                  Generate Workout
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'progress' && (
          <div className="progress-section">
            <div className="section-header">
              <h2>Your Progress</h2>
              <p>Track your nutrition and fitness journey</p>
            </div>
            <div className="progress-cards">
              <div className="progress-card">
                <div className="progress-icon">📊</div>
                <h3>Weekly Overview</h3>
                <p>Coming soon - detailed progress tracking</p>
              </div>
              <div className="progress-card">
                <div className="progress-icon">📈</div>
                <h3>Trends</h3>
                <p>Coming soon - visualize your progress</p>
              </div>
              <div className="progress-card">
                <div className="progress-icon">🏆</div>
                <h3>Achievements</h3>
                <p>Coming soon - celebrate your milestones</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
