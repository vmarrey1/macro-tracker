package com.macrotracker.backend.controller;

import com.macrotracker.backend.dto.MealPlanRequest;
import com.macrotracker.backend.service.LangGraphMealPlanService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/meal-plan")
@CrossOrigin(origins = "http://localhost:3000")
public class MealPlanController {

    private static final Logger log = LoggerFactory.getLogger(MealPlanController.class);

    @Autowired
    private LangGraphMealPlanService langGraphMealPlanService;
    
    @PostMapping("/generate")
    public Mono<ResponseEntity<String>> generateMealPlan(@Valid @RequestBody MealPlanRequest request) {
        log.info("Generating meal plan with LangGraph for {} calories, {} meals per day", request.getIdealCalories(), request.getNumberOfMeals());
        
        return langGraphMealPlanService.generateMealPlan(request)
                .map(response -> {
                    log.info("Successfully generated meal plan with LangGraph");
                    return ResponseEntity.ok(response);
                })
                .onErrorReturn(ResponseEntity.internalServerError()
                        .body("{\"error\": \"Failed to generate meal plan. Please try again.\"}"));
    }
    
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Meal Plan Service is running!");
    }
} 