package com.macrotracker.backend.service;

import com.macrotracker.backend.dto.MealPlanRequest;
import com.macrotracker.backend.dto.WorkoutPlanRequest;
import com.macrotracker.backend.model.MealPlan;
import com.macrotracker.backend.model.WorkoutPlan;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

@Service
public class LlmService {
    
    private static final Logger log = LoggerFactory.getLogger(LlmService.class);
    
    @Value("${llm.openai.api-key}")
    private String openaiApiKey;
    
    @Value("${llm.openai.model}")
    private String openaiModel;
    
    @Value("${llm.openai.max-tokens}")
    private Integer maxTokens;
    
    @Value("${llm.openai.temperature}")
    private Double temperature;
    
    private final WebClient webClient;
    
    public LlmService() {
        this.webClient = WebClient.builder()
                .baseUrl("https://api.openai.com/v1")
                .build();
    }
    
    public Mono<String> generateMealPlan(MealPlanRequest request) {
        String prompt = buildMealPlanPrompt(request);
        return callOpenAI(prompt);
    }
    
    public Mono<String> generateWorkoutPlan(WorkoutPlanRequest request) {
        String prompt = buildWorkoutPlanPrompt(request);
        return callOpenAI(prompt);
    }
    
    private String buildMealPlanPrompt(MealPlanRequest request) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("You are a professional nutritionist and meal planner. ");
        prompt.append("Create a 7-day meal plan with the following requirements:\n\n");
        prompt.append("- Daily calorie target: ").append(request.getIdealCalories()).append(" calories\n");
        prompt.append("- Number of meals per day: ").append(request.getNumberOfMeals()).append("\n");
        prompt.append("- Favorite foods to include: ").append(request.getFavoriteFoods()).append("\n");
        
        if (request.getDietaryRestrictions() != null && !request.getDietaryRestrictions().isEmpty()) {
            prompt.append("- Dietary Restrictions: ").append(request.getDietaryRestrictions()).append("\n");
        }
        
        if (request.getAllergies() != null && !request.getAllergies().isEmpty()) {
            prompt.append("- Allergies: ").append(request.getAllergies()).append("\n");
        }
        
        prompt.append("\nPlease provide:\n");
        prompt.append("1. A 7-day meal plan with ").append(request.getNumberOfMeals()).append(" meals per day\n");
        prompt.append("2. For each meal, include: name, calories, protein, carbs, fat, ingredients, and simple instructions\n");
        prompt.append("3. Ensure the daily total calories is close to ").append(request.getIdealCalories()).append("\n");
        prompt.append("4. Include favorite foods when possible\n");
        prompt.append("5. Shopping list for the week\n");
        prompt.append("6. Meal prep tips\n\n");
        prompt.append("Format the response as JSON with the following structure:\n");
        prompt.append("{\n");
        prompt.append("  \"dailyCalories\": ").append(request.getIdealCalories()).append(",\n");
        prompt.append("  \"weeklyPlan\": [{\n");
        prompt.append("    \"day\": \"Monday\",\n");
        prompt.append("    \"meals\": [{\n");
        prompt.append("      \"name\": \"string\",\n");
        prompt.append("      \"type\": \"breakfast|lunch|dinner|snack\",\n");
        prompt.append("      \"calories\": number,\n");
        prompt.append("      \"protein\": number,\n");
        prompt.append("      \"carbs\": number,\n");
        prompt.append("      \"fat\": number,\n");
        prompt.append("      \"ingredients\": \"string\",\n");
        prompt.append("      \"instructions\": \"string\"\n");
        prompt.append("    }]\n");
        prompt.append("  }],\n");
        prompt.append("  \"shoppingList\": [\"item1\", \"item2\"],\n");
        prompt.append("  \"mealPrepTips\": [\"tip1\", \"tip2\"]\n");
        prompt.append("}");
        
        return prompt.toString();
    }
    
    private String buildWorkoutPlanPrompt(WorkoutPlanRequest request) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("You are a professional fitness trainer and workout planner. ");
        prompt.append("Create a detailed ").append(request.getDurationWeeks()).append("-week workout plan for a person with the following characteristics:\n\n");
        prompt.append("- Age: ").append(request.getAge()).append(" years\n");
        prompt.append("- Gender: ").append(request.getGender()).append("\n");
        prompt.append("- Weight: ").append(request.getWeight()).append(" kg\n");
        prompt.append("- Height: ").append(request.getHeight()).append(" cm\n");
        prompt.append("- Activity Level: ").append(request.getActivityLevel()).append("\n");
        prompt.append("- Goal: ").append(request.getGoal()).append("\n");
        prompt.append("- Difficulty: ").append(request.getDifficulty()).append("\n");
        prompt.append("- Workouts per week: ").append(request.getWorkoutsPerWeek()).append("\n");
        
        if (request.getFitnessExperience() != null && !request.getFitnessExperience().isEmpty()) {
            prompt.append("- Fitness Experience: ").append(request.getFitnessExperience()).append("\n");
        }
        
        if (request.getAvailableEquipment() != null && !request.getAvailableEquipment().isEmpty()) {
            prompt.append("- Available Equipment: ").append(request.getAvailableEquipment()).append("\n");
        }
        
        if (request.getTimeAvailability() != null && !request.getTimeAvailability().isEmpty()) {
            prompt.append("- Time Availability: ").append(request.getTimeAvailability()).append("\n");
        }
        
        if (request.getInjuries() != null && !request.getInjuries().isEmpty()) {
            prompt.append("- Injuries/Limitations: ").append(request.getInjuries()).append("\n");
        }
        
        if (request.getPreferences() != null && !request.getPreferences().isEmpty()) {
            prompt.append("- Preferences: ").append(request.getPreferences()).append("\n");
        }
        
        prompt.append("\nPlease provide:\n");
        prompt.append("1. Weekly workout schedule\n");
        prompt.append("2. For each workout, include: name, type, duration, difficulty, and exercises\n");
        prompt.append("3. For each exercise, include: name, sets, reps, rest time, and instructions\n");
        prompt.append("4. Progressive overload recommendations\n");
        prompt.append("5. Recovery and rest day guidelines\n\n");
        prompt.append("Format the response as JSON with the following structure:\n");
        prompt.append("{\n");
        prompt.append("  \"weeklySchedule\": [{\n");
        prompt.append("    \"day\": \"Monday\",\n");
        prompt.append("    \"workout\": {\n");
        prompt.append("      \"name\": \"string\",\n");
        prompt.append("      \"type\": \"strength|cardio|flexibility|hiit|yoga\",\n");
        prompt.append("      \"duration\": \"string\",\n");
        prompt.append("      \"difficulty\": \"beginner|intermediate|advanced\",\n");
        prompt.append("      \"exercises\": [{\n");
        prompt.append("        \"name\": \"string\",\n");
        prompt.append("        \"category\": \"strength|cardio|flexibility|bodyweight\",\n");
        prompt.append("        \"muscleGroup\": \"string\",\n");
        prompt.append("        \"equipment\": \"string\",\n");
        prompt.append("        \"sets\": number,\n");
        prompt.append("        \"reps\": number,\n");
        prompt.append("        \"duration\": number,\n");
        prompt.append("        \"restTime\": number,\n");
        prompt.append("        \"weight\": \"string\",\n");
        prompt.append("        \"instructions\": \"string\"\n");
        prompt.append("      }]\n");
        prompt.append("    }\n");
        prompt.append("  }],\n");
        prompt.append("  \"progressiveOverload\": [\"tip1\", \"tip2\"],\n");
        prompt.append("  \"recoveryGuidelines\": [\"guideline1\", \"guideline2\"]\n");
        prompt.append("}");
        
        return prompt.toString();
    }
    
    private Mono<String> callOpenAI(String prompt) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("model", openaiModel);
        requestBody.put("messages", new Object[]{
                Map.of("role", "user", "content", prompt)
        });
        requestBody.put("max_tokens", maxTokens);
        requestBody.put("temperature", temperature);
        
        return webClient.post()
                .uri("/chat/completions")
                .header("Authorization", "Bearer " + openaiApiKey)
                .header("Content-Type", "application/json")
                .bodyValue(requestBody)
                .retrieve()
                .bodyToMono(Map.class)
                .map(response -> {
                    if (response.containsKey("choices") && !((java.util.List<?>) response.get("choices")).isEmpty()) {
                        Map<String, Object> choice = (Map<String, Object>) ((java.util.List<?>) response.get("choices")).get(0);
                        Map<String, Object> message = (Map<String, Object>) choice.get("message");
                        return (String) message.get("content");
                    }
                    throw new RuntimeException("Failed to get response from OpenAI");
                })
                .doOnError(error -> log.error("Error calling OpenAI API: {}", error.getMessage()))
                .onErrorReturn("{\"error\": \"Failed to generate plan. Please try again.\"}");
    }
} 