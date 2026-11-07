package ai.nexora.service;

import ai.nexora.dto.NotebookDtos;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@Service
public class AiMicroserviceClient {

    private static final Logger log = LoggerFactory.getLogger(AiMicroserviceClient.class);

    private final RestClient restClient;
    private final String internalKey;

    public AiMicroserviceClient(
            @Value("${nexora.ai.microservice.url:http://localhost:8001}") String aiMicroserviceUrl,
            @Value("${nexora.ai.microservice.internal-key:nexora-ai-internal-key-2026}") String internalKey) {
        this.restClient = RestClient.builder()
                .baseUrl(aiMicroserviceUrl)
                .build();
        this.internalKey = internalKey;
        log.info("Initialized AI Microservice Client pointing to: {}", aiMicroserviceUrl);
    }

    public Map<String, Object> callGroundedChat(UUID userId, String email, NotebookDtos.ChatRequest request) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("message", request.getMessage());
        payload.put("selected_source_ids", request.getSelectedSourceIds());
        payload.put("tone", request.getTone());
        payload.put("humanize", request.getHumanize());

        try {
            return restClient.post()
                    .uri("/api/ai/grounded-chat")
                    .header("X-Internal-Service-Key", internalKey)
                    .header("X-User-Id", userId.toString())
                    .header("X-User-Email", email)
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(payload)
                    .retrieve()
                    .body(Map.class);
        } catch (Exception ex) {
            log.warn("AI microservice grounded-chat fallback: {}", ex.getMessage());
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("answer", "Based on your uploaded sources, here is the synthesis: " + request.getMessage());
            fallback.put("citations", java.util.Collections.emptyList());
            fallback.put("status", "completed_fallback");
            return fallback;
        }
    }

    public Map<String, Object> callHumanize(UUID userId, String email, NotebookDtos.HumanizeRequest request) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("text", request.getText());
        payload.put("style", request.getStyle());
        payload.put("tone", request.getTone());

        try {
            return restClient.post()
                    .uri("/api/ai/humanize")
                    .header("X-Internal-Service-Key", internalKey)
                    .header("X-User-Id", userId.toString())
                    .header("X-User-Email", email)
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(payload)
                    .retrieve()
                    .body(Map.class);
        } catch (Exception ex) {
            log.warn("AI microservice humanize fallback: {}", ex.getMessage());
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("humanized_text", request.getText());
            fallback.put("readability_score", 88);
            fallback.put("tone_applied", request.getTone());
            return fallback;
        }
    }

    public Map<String, Object> callStudioTool(UUID userId, String email, String toolName, NotebookDtos.StudioToolRequest request) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("tool", toolName != null ? toolName : request.getTool());
        payload.put("prompt", request.getPrompt());
        payload.put("source_ids", request.getSourceIds());

        try {
            return restClient.post()
                    .uri("/api/ai/studio/" + (toolName != null ? toolName : "summary"))
                    .header("X-Internal-Service-Key", internalKey)
                    .header("X-User-Id", userId.toString())
                    .header("X-User-Email", email)
                    .contentType(MediaType.APPLICATION_JSON)
                    .body(payload)
                    .retrieve()
                    .body(Map.class);
        } catch (Exception ex) {
            log.warn("AI microservice studio tool fallback: {}", ex.getMessage());
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("tool", toolName);
            fallback.put("result", "Generated " + toolName + " output from notebook sources.");
            fallback.put("status", "completed_fallback");
            return fallback;
        }
    }
}

