package ai.nexora.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
public class HealthController {

    @GetMapping("/")
    public ResponseEntity<Map<String, Object>> root() {
        return ResponseEntity.ok(Map.of(
                "platform", "Nexora AI",
                "backend", "Java Spring Boot",
                "version", "2.0.0",
                "status", "online"
        ));
    }

    @GetMapping({"/health", "/api/health"})
    public ResponseEntity<Map<String, Object>> health() {
        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "service", "Nexora Primary Java Backend",
                "timestamp", System.currentTimeMillis()
        ));
    }
}

