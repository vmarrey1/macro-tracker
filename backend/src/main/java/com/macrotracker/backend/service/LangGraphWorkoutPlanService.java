package com.macrotracker.backend.service;

import com.macrotracker.backend.dto.WorkoutPlanRequest;
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
public class LangGraphWorkoutPlanService {

    private static final Logger log = LoggerFactory.getLogger(LangGraphWorkoutPlanService.class);

    @Autowired
    private ChatLanguageModel chatModel;

    public Mono<String> generateWorkoutPlan(WorkoutPlanRequest request) {
        return Mono.fromCallable(() -> {
            try {
                log.info("Generating workout plan with LangGraph for {} goal, {} level, {} workouts/week", 
                    request.getFitnessGoal(), request.getExperienceLevel(), request.getWorkoutsPerWeek());

                // Step 1: Analyze user fitness profile and requirements
                String analysisPrompt = buildAnalysisPrompt(request);
                String analysis = executeAnalysisStep(analysisPrompt);

                // Step 2: Generate workout structure and split
                String structurePrompt = buildStructurePrompt(request, analysis);
                String structure = executeStructureStep(structurePrompt);

                // Step 3: Generate detailed workout routines
                String detailedPrompt = buildDetailedPrompt(request, analysis, structure);
                String detailedRoutines = executeDetailedStep(detailedPrompt);

                // Step 4: Generate progression plan and tips
                String finalPrompt = buildFinalPrompt(request, detailedRoutines);
                String finalResult = executeFinalStep(finalPrompt);

                log.info("Successfully generated workout plan with LangGraph");
                return finalResult;

            } catch (Exception e) {
                log.error("Error in LangGraph workout plan generation: {}", e.getMessage(), e);
                throw new RuntimeException("Failed to generate workout plan with LangGraph", e);
            }
        });
    }

    private String buildAnalysisPrompt(WorkoutPlanRequest request) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("You are a professional fitness trainer and exercise physiologist analyzing user requirements for workout planning.\n\n");
        prompt.append("User Requirements:\n");
        prompt.append("- Fitness Goal: ").append(request.getFitnessGoal()).append("\n");
        prompt.append("- Experience Level: ").append(request.getExperienceLevel()).append("\n");
        prompt.append("- Workouts per Week: ").append(request.getWorkoutsPerWeek()).append("\n");
        prompt.append("- Workout Duration: ").append(request.getWorkoutDuration()).append(" minutes\n");
        
        if (request.getAvailableEquipment() != null && !request.getAvailableEquipment().isEmpty()) {
            prompt.append("- Available Equipment: ").append(request.getAvailableEquipment()).append("\n");
        }
        
        if (request.getInjuries() != null && !request.getInjuries().isEmpty()) {
            prompt.append("- Injuries/Limitations: ").append(request.getInjuries()).append("\n");
        }
        
        if (request.getPreferences() != null && !request.getPreferences().isEmpty()) {
            prompt.append("- Preferences: ").append(request.getPreferences()).append("\n");
        }
        
        prompt.append("\nAnalyze these requirements and provide:\n");
        prompt.append("1. Recommended workout split (e.g., Push/Pull/Legs, Upper/Lower, Full Body)\n");
        prompt.append("2. Exercise selection criteria\n");
        prompt.append("3. Intensity and volume recommendations\n");
        prompt.append("4. Progression strategy\n");
        prompt.append("5. Safety considerations\n");
        prompt.append("6. Recovery recommendations\n\n");
        prompt.append("Format as JSON with keys: workoutSplit, exerciseCriteria, intensityVolume, progressionStrategy, safetyConsiderations, recoveryRecommendations");
        
        return prompt.toString();
    }

    private String executeAnalysisStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a professional fitness trainer and exercise physiologist. Provide detailed, accurate analysis."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in analysis step: {}", e.getMessage());
            return "{\"error\": \"Analysis failed\"}";
        }
    }

    private String buildStructurePrompt(WorkoutPlanRequest request, String analysis) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("Based on the analysis: ").append(analysis).append("\n\n");
        prompt.append("Create a ").append(request.getWorkoutsPerWeek()).append("-day workout structure for ").append(request.getFitnessGoal()).append(".\n");
        prompt.append("Workout duration: ").append(request.getWorkoutDuration()).append(" minutes\n");
        prompt.append("Experience level: ").append(request.getExperienceLevel()).append("\n\n");
        prompt.append("Provide:\n");
        prompt.append("1. Weekly workout schedule\n");
        prompt.append("2. Focus areas for each day\n");
        prompt.append("3. Exercise categories per day\n");
        prompt.append("4. Rest day recommendations\n");
        prompt.append("5. Time allocation per exercise type\n\n");
        prompt.append("Format as JSON with structure: {\"weeklySchedule\": [{\"day\": \"Monday\", \"focus\": \"...\", \"exercises\": [...], \"restDay\": false}]}");
        
        return prompt.toString();
    }

    private String executeStructureStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a workout programming expert. Create structured, balanced workout plans."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in structure step: {}", e.getMessage());
            return "{\"error\": \"Structure generation failed\"}";
        }
    }

    private String buildDetailedPrompt(WorkoutPlanRequest request, String analysis, String structure) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("Analysis: ").append(analysis).append("\n");
        prompt.append("Structure: ").append(structure).append("\n\n");
        prompt.append("Create detailed workout routines for ").append(request.getWorkoutsPerWeek()).append(" days per week.\n");
        prompt.append("Goal: ").append(request.getFitnessGoal()).append("\n");
        prompt.append("Duration: ").append(request.getWorkoutDuration()).append(" minutes per session\n");
        prompt.append("Level: ").append(request.getExperienceLevel()).append("\n\n");
        
        if (request.getAvailableEquipment() != null && !request.getAvailableEquipment().isEmpty()) {
            prompt.append("Equipment: ").append(request.getAvailableEquipment()).append("\n\n");
        }
        
        prompt.append("For each workout provide:\n");
        prompt.append("- Warm-up routine (5-10 minutes)\n");
        prompt.append("- Main exercises with sets, reps, and rest periods\n");
        prompt.append("- Exercise alternatives for different equipment levels\n");
        prompt.append("- Cool-down routine (5 minutes)\n");
        prompt.append("- Progression notes\n");
        prompt.append("- Form cues and safety tips\n\n");
        prompt.append("Format as JSON with structure: {\"weeklyWorkouts\": [{\"day\": \"Monday\", \"warmup\": [...], \"mainExercises\": [...], \"cooldown\": [...], \"progressionNotes\": \"...\", \"formCues\": [...]}]}");
        
        return prompt.toString();
    }

    private String executeDetailedStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a professional personal trainer and exercise specialist. Create detailed, practical workout routines."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in detailed step: {}", e.getMessage());
            return "{\"error\": \"Detailed routine generation failed\"}";
        }
    }

    private String buildFinalPrompt(WorkoutPlanRequest request, String detailedRoutines) {
        StringBuilder prompt = new StringBuilder();
        prompt.append("Detailed Routines: ").append(detailedRoutines).append("\n\n");
        prompt.append("Generate the final workout plan package including:\n");
        prompt.append("1. Complete ").append(request.getWorkoutsPerWeek()).append("-day workout plan with all routines\n");
        prompt.append("2. Weekly progression schedule (4-8 weeks)\n");
        prompt.append("3. Exercise library with descriptions and form cues\n");
        prompt.append("4. Nutrition recommendations for ").append(request.getFitnessGoal()).append("\n");
        prompt.append("5. Recovery and rest day guidelines\n");
        prompt.append("6. Equipment alternatives and modifications\n");
        prompt.append("7. Progress tracking methods\n\n");
        prompt.append("Format as JSON with structure: {\"goal\": \"").append(request.getFitnessGoal()).append("\", \"experienceLevel\": \"").append(request.getExperienceLevel()).append("\", \"workoutsPerWeek\": ").append(request.getWorkoutsPerWeek()).append(", \"workoutDuration\": ").append(request.getWorkoutDuration()).append(", \"weeklyWorkouts\": [...], \"progressionSchedule\": [...], \"exerciseLibrary\": [...], \"nutritionRecommendations\": {...}, \"recoveryGuidelines\": [...], \"equipmentAlternatives\": [...], \"progressTracking\": [...]}");
        
        return prompt.toString();
    }

    private String executeFinalStep(String prompt) {
        try {
            Response<AiMessage> response = chatModel.generate(
                new SystemMessage("You are a comprehensive fitness coach. Create complete, user-friendly workout plans."),
                new UserMessage(prompt)
            );
            return response.content().text();
        } catch (Exception e) {
            log.error("Error in final step: {}", e.getMessage());
            return "{\"error\": \"Final plan generation failed\"}";
        }
    }
} 