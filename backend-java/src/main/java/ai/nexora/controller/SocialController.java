package ai.nexora.controller;

import ai.nexora.dto.SocialDtos;
import ai.nexora.entity.SocialAccount;
import ai.nexora.entity.User;
import ai.nexora.service.SocialService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/social")
public class SocialController {

    private final SocialService socialService;

    public SocialController(SocialService socialService) {
        this.socialService = socialService;
    }

    @GetMapping("/accounts")
    public ResponseEntity<List<SocialAccount>> getAccounts(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(socialService.getAccounts(user.getId()));
    }

    @PostMapping("/add-profile-link")
    public ResponseEntity<SocialAccount> addProfileLink(
            @AuthenticationPrincipal User user,
            @RequestBody SocialDtos.AddProfileLinkRequest req) {
        return ResponseEntity.ok(socialService.addProfileLink(user.getId(), req));
    }

    @PostMapping("/connect-github")
    public ResponseEntity<SocialAccount> connectGithub(
            @AuthenticationPrincipal User user,
            @RequestBody SocialDtos.ConnectGithubRequest req) {
        return ResponseEntity.ok(socialService.connectGithub(user.getId(), req));
    }

    @PatchMapping("/visibility/{id}")
    public ResponseEntity<Map<String, Object>> updateVisibility(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id,
            @RequestBody Map<String, Boolean> body) {
        boolean showOnProfile = body.getOrDefault("showOnPublicProfile", true);
        boolean updated = socialService.updateVisibility(user.getId(), id, showOnProfile);
        return ResponseEntity.ok(Map.of("success", updated, "showOnPublicProfile", showOnProfile));
    }

    @DeleteMapping("/disconnect/{id}")
    public ResponseEntity<Map<String, Object>> disconnect(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id) {
        boolean disconnected = socialService.disconnect(user.getId(), id);
        return ResponseEntity.ok(Map.of("success", disconnected));
    }
}

