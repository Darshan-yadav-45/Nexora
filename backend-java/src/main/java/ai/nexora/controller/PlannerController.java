package ai.nexora.controller;

import ai.nexora.entity.PlannerTask;
import ai.nexora.entity.User;
import ai.nexora.service.PlannerService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/planner")
public class PlannerController {

    private final PlannerService plannerService;

    public PlannerController(PlannerService plannerService) {
        this.plannerService = plannerService;
    }

    @GetMapping("/tasks")
    public ResponseEntity<List<PlannerTask>> getTasks(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(plannerService.getTasks(user.getId()));
    }

    @PostMapping("/tasks")
    public ResponseEntity<PlannerTask> createTask(
            @AuthenticationPrincipal User user,
            @RequestBody PlannerTask task) {
        return ResponseEntity.ok(plannerService.createTask(user.getId(), task));
    }

    @PutMapping("/tasks/{id}")
    public ResponseEntity<PlannerTask> updateTask(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id,
            @RequestBody PlannerTask task) {
        return ResponseEntity.ok(plannerService.updateTask(user.getId(), id, task));
    }

    @DeleteMapping("/tasks/{id}")
    public ResponseEntity<Map<String, Object>> deleteTask(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id) {
        boolean deleted = plannerService.deleteTask(user.getId(), id);
        return ResponseEntity.ok(Map.of("success", deleted));
    }
}

