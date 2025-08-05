package com.macrotracker.backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

public class WorkoutPlanRequest {
    
    @NotBlank(message = "Fitness goal is required")
    private String fitnessGoal; // strength, cardio, flexibility, weight_loss, muscle_gain, endurance
    
    @NotBlank(message = "Experience level is required")
    private String experienceLevel; // beginner, intermediate, advanced
    
    @NotNull(message = "Workouts per week is required")
    @Min(value = 2, message = "Workouts per week must be at least 2")
    @Max(value = 6, message = "Workouts per week must be at most 6")
    private Integer workoutsPerWeek;
    
    @NotNull(message = "Workout duration is required")
    @Min(value = 30, message = "Workout duration must be at least 30 minutes")
    @Max(value = 120, message = "Workout duration must be at most 120 minutes")
    private Integer workoutDuration; // in minutes
    
    private String availableEquipment; // none, minimal, full_gym, home_equipment
    private String injuries; // comma-separated list of injuries or limitations
    private String preferences; // workout preferences or dislikes
    
    // Constructors
    public WorkoutPlanRequest() {}
    
    public WorkoutPlanRequest(String fitnessGoal, String experienceLevel, Integer workoutsPerWeek, 
                             Integer workoutDuration, String availableEquipment, String injuries, String preferences) {
        this.fitnessGoal = fitnessGoal;
        this.experienceLevel = experienceLevel;
        this.workoutsPerWeek = workoutsPerWeek;
        this.workoutDuration = workoutDuration;
        this.availableEquipment = availableEquipment;
        this.injuries = injuries;
        this.preferences = preferences;
    }
    
    // Getters and Setters
    public String getFitnessGoal() { return fitnessGoal; }
    public void setFitnessGoal(String fitnessGoal) { this.fitnessGoal = fitnessGoal; }
    
    public String getExperienceLevel() { return experienceLevel; }
    public void setExperienceLevel(String experienceLevel) { this.experienceLevel = experienceLevel; }
    
    public Integer getWorkoutsPerWeek() { return workoutsPerWeek; }
    public void setWorkoutsPerWeek(Integer workoutsPerWeek) { this.workoutsPerWeek = workoutsPerWeek; }
    
    public Integer getWorkoutDuration() { return workoutDuration; }
    public void setWorkoutDuration(Integer workoutDuration) { this.workoutDuration = workoutDuration; }
    
    public String getAvailableEquipment() { return availableEquipment; }
    public void setAvailableEquipment(String availableEquipment) { this.availableEquipment = availableEquipment; }
    
    public String getInjuries() { return injuries; }
    public void setInjuries(String injuries) { this.injuries = injuries; }
    
    public String getPreferences() { return preferences; }
    public void setPreferences(String preferences) { this.preferences = preferences; }
} 