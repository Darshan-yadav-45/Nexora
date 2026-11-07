package ai.nexora.controller;

import ai.nexora.dto.AuthDtos;
import ai.nexora.entity.User;
import ai.nexora.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<AuthDtos.AuthResponse> register(@Valid @RequestBody AuthDtos.RegisterRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping(value = "/login", consumes = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<AuthDtos.AuthResponse> loginJson(@Valid @RequestBody AuthDtos.LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @PostMapping(value = "/login", consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
    public ResponseEntity<AuthDtos.AuthResponse> loginForm(
            @RequestParam(required = false) String username,
            @RequestParam(required = false) String email,
            @RequestParam String password) {
        String loginIdentifier = username != null ? username : email;
        AuthDtos.LoginRequest request = new AuthDtos.LoginRequest(loginIdentifier, password);
        return ResponseEntity.ok(authService.login(request));
    }

    @GetMapping("/me")
    public ResponseEntity<AuthDtos.UserDto> getCurrentUser(@AuthenticationPrincipal User user) {
        if (user == null) {
            return ResponseEntity.status(401).build();
        }
        return ResponseEntity.ok(authService.getCurrentUser(user));
    }

    @PostMapping("/select-account-type")
    public ResponseEntity<AuthDtos.UserDto> selectAccountType(
            @AuthenticationPrincipal User user,
            @Valid @RequestBody AuthDtos.SelectRoleRequest request) {
        if (user == null) {
            return ResponseEntity.status(401).build();
        }
        return ResponseEntity.ok(authService.selectAccountType(user, request.getAccountType()));
    }

    @PostMapping("/forgot-password")
    public ResponseEntity<Map<String, String>> forgotPassword(@Valid @RequestBody AuthDtos.ForgotPasswordRequest request) {
        String token = authService.requestForgotPassword(request.getEmail());
        Map<String, String> response = new HashMap<>();
        response.put("message", "If an account exists, a password reset link has been dispatched.");
        response.put("resetToken", token);
        response.put("reset_token_preview", token);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/reset-password")
    public ResponseEntity<Map<String, String>> resetPassword(@Valid @RequestBody AuthDtos.ResetPasswordRequest request) {
        authService.resetPassword(request);
        Map<String, String> response = new HashMap<>();
        response.put("message", "Password has been successfully reset. Please log in with your new credentials.");
        return ResponseEntity.ok(response);
    }

    @GetMapping("/status")
    public ResponseEntity<Map<String, Object>> authStatus(@AuthenticationPrincipal User user) {
        Map<String, Object> status = new HashMap<>();
        if (user != null) {
            status.put("authenticated", true);
            status.put("user", authService.getCurrentUser(user));
        } else {
            status.put("authenticated", false);
            status.put("user", null);
        }
        return ResponseEntity.ok(status);
    }
}
