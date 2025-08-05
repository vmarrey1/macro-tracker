package com.macrotracker.backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;

public class MealPlanRequest {
    
    @NotNull(message = "Ideal calories is required")
    @Min(value = 1200, message = "Calories must be at least 1200")
    @Max(value = 5000, message = "Calories must be at most 5000")
    private Integer idealCalories;
    
    @NotBlank(message = "Favorite foods are required")
    private String favoriteFoods; // comma-separated list of favorite foods
    
    @NotNull(message = "Number of meals is required")
    @Min(value = 2, message = "Number of meals must be at least 2")
    @Max(value = 6, message = "Number of meals must be at most 6")
    private Integer numberOfMeals;
    
    private String dietaryRestrictions; // vegetarian, vegan, gluten_free, dairy_free, etc.
    private String allergies; // comma-separated list of allergies
    
    // Getters and Setters
    public Integer getIdealCalories() { return idealCalories; }
    public void setIdealCalories(Integer idealCalories) { this.idealCalories = idealCalories; }
    
    public String getFavoriteFoods() { return favoriteFoods; }
    public void setFavoriteFoods(String favoriteFoods) { this.favoriteFoods = favoriteFoods; }
    
    public Integer getNumberOfMeals() { return numberOfMeals; }
    public void setNumberOfMeals(Integer numberOfMeals) { this.numberOfMeals = numberOfMeals; }
    
    public String getDietaryRestrictions() { return dietaryRestrictions; }
    public void setDietaryRestrictions(String dietaryRestrictions) { this.dietaryRestrictions = dietaryRestrictions; }
    
    public String getAllergies() { return allergies; }
    public void setAllergies(String allergies) { this.allergies = allergies; }
} 