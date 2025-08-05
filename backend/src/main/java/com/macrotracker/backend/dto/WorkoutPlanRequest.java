package com.macrotracker.backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

public class WorkoutPlanRequest {
    
    // Getters and Setters
    public String getGoal() { return goal; }
    public void setGoal(String goal) { this.goal = goal; }
    
    public String getDifficulty() { return difficulty; }
    public void setDifficulty(String difficulty) { this.difficulty = difficulty; }
    
    public Integer getAge() { return age; }
    public void setAge(Integer age) { this.age = age; }
    
    public String getGender() { return gender; }
    public void setGender(String gender) { this.gender = gender; }
    
    public Double getWeight() { return weight; }
    public void setWeight(Double weight) { this.weight = weight; }
    
    public Double getHeight() { return height; }
    public void setHeight(Double height) { this.height = height; }
    
    public String getActivityLevel() { return activityLevel; }
    public void setActivityLevel(String activityLevel) { this.activityLevel = activityLevel; }
    
    public String getFitnessExperience() { return fitnessExperience; }
    public void setFitnessExperience(String fitnessExperience) { this.fitnessExperience = fitnessExperience; }
    
    public String getAvailableEquipment() { return availableEquipment; }
    public void setAvailableEquipment(String availableEquipment) { this.availableEquipment = availableEquipment; }
    
    public String getTimeAvailability() { return timeAvailability; }
    public void setTimeAvailability(String timeAvailability) { this.timeAvailability = timeAvailability; }
    
    public Integer getDurationWeeks() { return durationWeeks; }
    public void setDurationWeeks(Integer durationWeeks) { this.durationWeeks = durationWeeks; }
    
    public Integer getWorkoutsPerWeek() { return workoutsPerWeek; }
    public void setWorkoutsPerWeek(Integer workoutsPerWeek) { this.workoutsPerWeek = workoutsPerWeek; }
    
    public String getInjuries() { return injuries; }
    public void setInjuries(String injuries) { this.injuries = injuries; }
    
    public String getPreferences() { return preferences; }
    public void setPreferences(String preferences) { this.preferences = preferences; }
    
    @NotBlank(message = "Goal is required")
    private String goal; // strength, cardio, flexibility, weight_loss, muscle_gain
    
    @NotBlank(message = "Difficulty level is required")
    private String difficulty; // beginner, intermediate, advanced
    
    @NotNull(message = "Age is required")
    @Min(value = 13, message = "Age must be at least 13")
    @Max(value = 100, message = "Age must be at most 100")
    private Integer age;
    
    @NotBlank(message = "Gender is required")
    private String gender; // male, female, other
    
    @NotNull(message = "Weight is required")
    @Min(value = 30, message = "Weight must be at least 30 kg")
    @Max(value = 300, message = "Weight must be at most 300 kg")
    private Double weight; // in kg
    
    @NotNull(message = "Height is required")
    @Min(value = 100, message = "Height must be at least 100 cm")
    @Max(value = 250, message = "Height must be at most 250 cm")
    private Double height; // in cm
    
    @NotBlank(message = "Activity level is required")
    private String activityLevel; // sedentary, lightly_active, moderately_active, very_active, extremely_active
    
    private String fitnessExperience; // none, beginner, intermediate, advanced
    private String availableEquipment; // none, minimal, full_gym, home_equipment
    private String timeAvailability; // 30_min, 45_min, 60_min, 90_min
    
    @NotNull(message = "Duration in weeks is required")
    @Min(value = 1, message = "Duration must be at least 1 week")
    @Max(value = 12, message = "Duration must be at most 12 weeks")
    private Integer durationWeeks;
    
    @NotNull(message = "Workouts per week is required")
    @Min(value = 1, message = "Workouts per week must be at least 1")
    @Max(value = 7, message = "Workouts per week must be at most 7")
    private Integer workoutsPerWeek;
    
    private String injuries; // comma-separated list of injuries or limitations
    private String preferences; // workout preferences or dislikes
} 