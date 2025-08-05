package com.macrotracker.backend.controller;

import com.macrotracker.backend.dto.WorkoutPlanRequest;
import com.macrotracker.backend.service.LangGraphWorkoutPlanService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/workout")
@CrossOrigin(origins = "http://localhost:3000")
public class WorkoutController {
    
    private static final Logger log = LoggerFactory.getLogger(WorkoutController.class);
    
    @Autowired
    private LangGraphWorkoutPlanService langGraphWorkoutPlanService;
    
    @PostMapping("/generate")
    public Mono<ResponseEntity<String>> generateWorkoutPlan(@Valid @RequestBody WorkoutPlanRequest request) {
        log.info("Generating workout plan with LangGraph for {} goal, {} level, {} workouts/week", 
            request.getFitnessGoal(), request.getExperienceLevel(), request.getWorkoutsPerWeek());
        
        return langGraphWorkoutPlanService.generateWorkoutPlan(request)
                .map(response -> {
                    log.info("Successfully generated workout plan with LangGraph");
                    return ResponseEntity.ok(response);
                })
                .onErrorReturn(ResponseEntity.internalServerError()
                        .body("{\"error\": \"Failed to generate workout plan. Please try again.\"}"));
    }
    
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Workout Service is running!");
    }
} 