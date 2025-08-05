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
    
    // Workout plan generation moved to LangGraphWorkoutPlanService
    // This method is kept for backward compatibility but delegates to the new service
    public Mono<String> generateWorkoutPlan(WorkoutPlanRequest request) {
        log.warn("Using deprecated LlmService.generateWorkoutPlan - use LangGraphWorkoutPlanService instead");
        throw new UnsupportedOperationException("Use LangGraphWorkoutPlanService for workout plan generation");
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