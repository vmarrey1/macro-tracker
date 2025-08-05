package com.macrotracker.backend.config;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;

@Configuration
public class LangGraphConfig {

    @Value("${llm.openai.api-key}")
    private String openaiApiKey;

    @Value("${llm.openai.model:gpt-4}")
    private String openaiModel;

    @Value("${llm.openai.max-tokens:2000}")
    private Integer maxTokens;

    @Value("${llm.openai.temperature:0.7}")
    private Double temperature;

    @Bean
    public ChatLanguageModel chatLanguageModel() {
        return OpenAiChatModel.builder()
                .apiKey(openaiApiKey)
                .modelName(openaiModel)
                .maxTokens(maxTokens)
                .temperature(temperature)
                .timeout(Duration.ofSeconds(60))
                .build();
    }
} 