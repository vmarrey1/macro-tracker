package com.macrotracker.backend.model;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "meals")
public class Meal {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "meal_plan_id", nullable = false)
    private MealPlan mealPlan;
    
    private String name;
    private String description;
    private String mealType; // breakfast, lunch, dinner, snack
    
    private Integer calories;
    private Integer protein; // in grams
    private Integer carbs; // in grams
    private Integer fat; // in grams
    private Integer fiber; // in grams
    
    private String ingredients;
    private String instructions;
    private String prepTime; // e.g., "15 minutes"
    private String cookTime; // e.g., "30 minutes"
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
} 