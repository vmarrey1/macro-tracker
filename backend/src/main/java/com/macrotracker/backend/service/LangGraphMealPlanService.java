package com.macrotracker.backend.service;

import com.macrotracker.backend.dto.MealPlanRequest;
import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.SystemMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.output.Response;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class LangGraphMealPlanService {

    private static final Logger log = LoggerFactory.getLogger(LangGraphMealPlanService.class);

    @Autowired
    private ChatLanguageModel chatModel;

    public Mono<String> generateMealPlan(MealPlanRequest request) {
        return Mono.fromCallable(() -> {
            try {
                log.info("Generating meal plan with LangGraph for {} calories, {} meals", 
                    request.getIdealCalories(), request.getNumberOfMeals());

                // Step 1: Analyze user preferences and requirements
                String analysisPrompt = buildAnalysisPrompt(request);
                String analysis = executeAnalysisStep(analysisPrompt);

                // Step 2: Generate meal structure
                String structurePrompt = buildStructurePrompt(request, analysis);
                String structure = executeStructureStep(structurePrompt);

                // Step 3: Generate detailed meal plan
                String detailedPrompt = buildDetailedPrompt(request, analysis, structure);
                String detailedPlan = executeDetailedStep(detailedPrompt);

                // Step 4: Generate shopping list and tips
                String finalPrompt = buildFinalPrompt(request, detailedPlan);
                String finalResult = executeFinalStep(finalPrompt);

                log.info("Successfully generated meal plan with LangGraph");
                return finalResult;

            } catch (Exception e) {
                log.error("Error in LangGraph meal plan generation: {}", e.getMessage(), e);
                throw new RuntimeException("Failed to generate meal plan with LangGraph", e);
            }
        });
    }

    private String buildAnalysisPrompt(MealPlanRequest request) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("You are a professional nutritionist analyzing user preferences for meal planning.\n\n");
        prompt.append("User Requirements:\n");
        prompt.append("- Daily calorie target: ").append(request.getIdealCalories()).append(" calories\n");
        prompt.append("- Number of meals per day: ").append(request.getNumberOfMeals()).append("\n");
        prompt.append("- Favorite foods: ").append(request.getFavoriteFoods()).append("\n");
        
        if (request.getDietaryRestrictions() != null && !request.getDietaryRestrictions().isEmpty()) {
            prompt.append("- Dietary restrictions: ").append(request.getDietaryRestrictions()).append("\n");
        }
        
        if (request.getAllergies() != null && !request.getAllergies().isEmpty()) {
            prompt.append("- Allergies: ").append(request.getAllergies()).append("\n");
        }
        
        prompt.append("\nAnalyze these requirements and provide:\n");
        prompt.append("1. Calorie distribution per meal\n");
        prompt.append("2. Macro breakdown (protein, carbs, fat)\n");
        prompt.append("3. Key nutritional considerations\n");
        prompt.append("4. Recommended food categories\n");
        prompt.append("5. Potential challenges and solutions\n\n");
        prompt.append("Format as JSON with keys: calorieDistribution, macroBreakdown, considerations, foodCategories, challenges");
        
        return prompt.toString();
    }

    private String executeAnalysisStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a professional nutritionist. Provide detailed, accurate analysis."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in analysis step: {}", e.getMessage());
            return "{\"error\": \"Analysis failed\"}";
        }
    }

    private String buildStructurePrompt(MealPlanRequest request, String analysis) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("Based on the analysis: ").append(analysis).append("\n\n");
        prompt.append("Create a 7-day meal structure with ").append(request.getNumberOfMeals()).append(" meals per day.\n");
        prompt.append("Daily calorie target: ").append(request.getIdealCalories()).append(" calories\n\n");
        prompt.append("Provide:\n");
        prompt.append("1. Daily meal themes (e.g., 'Protein Focus Monday', 'Vegetarian Tuesday')\n");
        prompt.append("2. Meal timing suggestions\n");
        prompt.append("3. Calorie distribution per meal\n");
        prompt.append("4. Key ingredients to include\n\n");
        prompt.append("Format as JSON with structure: {\"weeklyStructure\": [{\"day\": \"Monday\", \"theme\": \"...\", \"meals\": [...]}]}");
        
        return prompt.toString();
    }

    private String executeStructureStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a meal planning expert. Create structured, balanced meal plans."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in structure step: {}", e.getMessage());
            return "{\"error\": \"Structure generation failed\"}";
        }
    }

    private String buildDetailedPrompt(MealPlanRequest request, String analysis, String structure) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("Analysis: ").append(analysis).append("\n");
        prompt.append("Structure: ").append(structure).append("\n\n");
        prompt.append("Create detailed meal recipes for a 7-day plan with ").append(request.getNumberOfMeals()).append(" meals per day.\n");
        prompt.append("Daily calories: ").append(request.getIdealCalories()).append("\n");
        prompt.append("Include favorite foods: ").append(request.getFavoriteFoods()).append("\n\n");
        prompt.append("For each meal provide:\n");
        prompt.append("- Recipe name\n");
        prompt.append("- Ingredients with quantities\n");
        prompt.append("- Step-by-step instructions\n");
        prompt.append("- Nutritional info (calories, protein, carbs, fat)\n");
        prompt.append("- Prep time\n");
        prompt.append("- Cooking time\n\n");
        prompt.append("Format as JSON with structure: {\"weeklyPlan\": [{\"day\": \"Monday\", \"meals\": [{\"name\": \"...\", \"ingredients\": \"...\", \"instructions\": \"...\", \"nutrition\": {...}, \"prepTime\": \"...\", \"cookTime\": \"...\"}]}]}");
        
        return prompt.toString();
    }

    private String executeDetailedStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a professional chef and nutritionist. Create detailed, practical recipes."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in detailed step: {}", e.getMessage());
            return "{\"error\": \"Detailed plan generation failed\"}";
        }
    }

    private String buildFinalPrompt(MealPlanRequest request, String detailedPlan) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("Detailed Plan: ").append(detailedPlan).append("\n\n");
        prompt.append("Generate the final meal plan package including:\n");
        prompt.append("1. Complete 7-day meal plan with all recipes\n");
        prompt.append("2. Comprehensive shopping list organized by category\n");
        prompt.append("3. Meal prep tips and storage instructions\n");
        prompt.append("4. Nutritional summary for each day\n");
        prompt.append("5. Substitution suggestions for dietary restrictions\n\n");
        prompt.append("Format as JSON with structure: {\"dailyCalories\": ").append(request.getIdealCalories()).append(", \"weeklyPlan\": [...], \"shoppingList\": [...], \"mealPrepTips\": [...], \"nutritionalSummary\": {...}}");
        
        return prompt.toString();
    }

    private String executeFinalStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a meal planning expert. Create comprehensive, user-friendly meal plans."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in final step: {}", e.getMessage());
            return "{\"error\": \"Final plan generation failed\"}";
        }
    }
} 