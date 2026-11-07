package ai.nexora.service;

import ai.nexora.dto.AuthDtos;
import ai.nexora.entity.User;
import ai.nexora.entity.UserProfile;
import ai.nexora.repository.UserProfileRepository;
import ai.nexora.repository.UserRepository;
import ai.nexora.security.JwtTokenProvider;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final UserProfileRepository userProfileRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtTokenProvider jwtTokenProvider;

    public AuthService(
            UserRepository userRepository,
            UserProfileRepository userProfileRepository,
            PasswordEncoder passwordEncoder,
            JwtTokenProvider jwtTokenProvider) {
        this.userRepository = userRepository;
        this.userProfileRepository = userProfileRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @Transactional
    public AuthDtos.AuthResponse register(AuthDtos.RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new IllegalArgumentException("User with this email already exists");
        }

        if (request.getConfirmPassword() != null && !request.getPassword().equals(request.getConfirmPassword())) {
            throw new IllegalArgumentException("Passwords do not match");
        }

        User user = new User();
        user.setEmail(request.getEmail().toLowerCase().trim());
        user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
        user.setIsVerified(true);
        user.setProfileCompleted(false);
        user.setFirstTimeLogin(true);
        user = userRepository.save(user);

        UserProfile profile = new UserProfile(user.getId(), request.getName());
        userProfileRepository.save(profile);

        String token = jwtTokenProvider.generateToken(user.getEmail(), user.getId());
        AuthDtos.UserDto userDto = mapToUserDto(user, profile.getName());

        return new AuthDtos.AuthResponse(token, userDto, "Registration successful");
    }

    public AuthDtos.AuthResponse login(AuthDtos.LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail().toLowerCase().trim())
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
            throw new IllegalArgumentException("Invalid email or password");
        }

        String name = userProfileRepository.findByUserId(user.getId())
                .map(UserProfile::getName)
                .orElse("Nexora User");

        String token = jwtTokenProvider.generateToken(user.getEmail(), user.getId());
        AuthDtos.UserDto userDto = mapToUserDto(user, name);

        return new AuthDtos.AuthResponse(token, userDto, "Login successful");
    }

    public AuthDtos.UserDto getCurrentUser(User user) {
        String name = userProfileRepository.findByUserId(user.getId())
                .map(UserProfile::getName)
                .orElse("Nexora User");
        return mapToUserDto(user, name);
    }

    @Transactional
    public AuthDtos.UserDto selectAccountType(User user, String accountType) {
        user.setAccountType(accountType.toLowerCase().trim());
        user.setFirstTimeLogin(false);
        user = userRepository.save(user);

        String name = userProfileRepository.findByUserId(user.getId())
                .map(UserProfile::getName)
                .orElse("Nexora User");

        return mapToUserDto(user, name);
    }

    @Transactional
    public String requestForgotPassword(String email) {
        Optional<User> userOpt = userRepository.findByEmail(email.toLowerCase().trim());
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            String token = UUID.randomUUID().toString();
            user.setResetPasswordToken(token);
            user.setResetTokenExpiry(LocalDateTime.now().plusHours(24));
            userRepository.save(user);
            return token;
        }
        return UUID.randomUUID().toString(); // Return token without leaking user existence
    }

    @Transactional
    public boolean resetPassword(AuthDtos.ResetPasswordRequest request) {
        if (request.getConfirmPassword() != null && !request.getNewPassword().equals(request.getConfirmPassword())) {
            throw new IllegalArgumentException("Passwords do not match");
        }

        User user = userRepository.findAll().stream()
                .filter(u -> request.getToken().equals(u.getResetPasswordToken()))
                .filter(u -> u.getResetTokenExpiry() != null && u.getResetTokenExpiry().isAfter(LocalDateTime.now()))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Invalid or expired password reset token"));

        user.setPasswordHash(passwordEncoder.encode(request.getNewPassword()));
        user.setResetPasswordToken(null);
        user.setResetTokenExpiry(null);
        userRepository.save(user);
        return true;
    }

    private AuthDtos.UserDto mapToUserDto(User user, String name) {
        AuthDtos.UserDto dto = new AuthDtos.UserDto();
        dto.setId(user.getId());
        dto.setEmail(user.getEmail());
        dto.setName(name);
        dto.setAccountType(user.getAccountType());
        dto.setIsVerified(user.getIsVerified());
        dto.setProfileCompleted(user.getProfileCompleted());
        dto.setFirstTimeLogin(user.getFirstTimeLogin());
        return dto;
    }
}

