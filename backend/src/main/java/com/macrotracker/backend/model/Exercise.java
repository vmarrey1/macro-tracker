package com.macrotracker.backend.model;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "exercises")
public class Exercise {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne
    @JoinColumn(name = "workout_id", nullable = false)
    private Workout workout;
    
    private String name;
    private String description;
    private String category; // strength, cardio, flexibility, bodyweight
    
    private String muscleGroup; // chest, back, legs, shoulders, arms, core, full_body
    private String equipment; // barbell, dumbbell, bodyweight, machine, cable, etc.
    
    private Integer sets;
    private Integer reps;
    private Integer duration; // in seconds, for timed exercises
    private Integer restTime; // in seconds
    
    private String weight; // e.g., "10kg", "bodyweight"
    private String notes; // additional instructions or modifications
    
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