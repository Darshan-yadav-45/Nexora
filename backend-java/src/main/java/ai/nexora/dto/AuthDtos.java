package ai.nexora.dto;

import com.fasterxml.jackson.annotation.JsonAlias;
import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.util.UUID;

public class AuthDtos {

    public static class RegisterRequest {
        @NotBlank(message = "Name is required")
        private String name;

        @NotBlank(message = "Email is required")
        @Email(message = "Valid email is required")
        private String email;

        @NotBlank(message = "Password is required")
        @Size(min = 6, message = "Password must be at least 6 characters")
        private String password;

        @JsonAlias({"confirm_password", "confirmPassword"})
        private String confirmPassword;

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }

        public String getConfirmPassword() { return confirmPassword; }
        public void setConfirmPassword(String confirmPassword) { this.confirmPassword = confirmPassword; }

        @JsonProperty("confirm_password")
        public void setConfirm_password(String confirm_password) { this.confirmPassword = confirm_password; }
    }

    public static class LoginRequest {
        @JsonAlias({"email", "username"})
        private String email;

        @NotBlank(message = "Password is required")
        private String password;

        public LoginRequest() {}

        public LoginRequest(String email, String password) {
            this.email = email;
            this.password = password;
        }

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        @JsonProperty("username")
        public void setUsername(String username) { this.email = username; }

        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
    }

    public static class AuthResponse {
        private String token;
        private UserDto user;
        private String message;

        public AuthResponse() {}

        public AuthResponse(String token, UserDto user, String message) {
            this.token = token;
            this.user = user;
            this.message = message;
        }

        public String getToken() { return token; }
        public void setToken(String token) { this.token = token; }

        @JsonProperty("access_token")
        public String getAccess_token() { return token; }

        @JsonProperty("token_type")
        public String getToken_type() { return "bearer"; }

        public UserDto getUser() { return user; }
        public void setUser(UserDto user) { this.user = user; }

        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }
    }

    public static class UserDto {
        private UUID id;
        private String email;
        private String name;
        private String accountType;
        private Boolean isVerified;
        private Boolean profileCompleted;
        private Boolean firstTimeLogin;

        public UserDto() {}

        public UUID getId() { return id; }
        public void setId(UUID id) { this.id = id; }

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }

        public String getAccountType() { return accountType; }
        public void setAccountType(String accountType) { this.accountType = accountType; }

        @JsonProperty("account_type")
        public String getAccount_type() { return accountType; }

        public Boolean getIsVerified() { return isVerified; }
        public void setIsVerified(Boolean isVerified) { this.isVerified = isVerified; }

        @JsonProperty("is_verified")
        public Boolean getIs_verified() { return isVerified; }

        public Boolean getProfileCompleted() { return profileCompleted; }
        public void setProfileCompleted(Boolean profileCompleted) { this.profileCompleted = profileCompleted; }

        @JsonProperty("profile_completed")
        public Boolean getProfile_completed() { return profileCompleted; }

        public Boolean getFirstTimeLogin() { return firstTimeLogin; }
        public void setFirstTimeLogin(Boolean firstTimeLogin) { this.firstTimeLogin = firstTimeLogin; }

        @JsonProperty("first_time_login")
        public Boolean getFirst_time_login() { return firstTimeLogin; }
    }

    public static class SelectRoleRequest {
        @NotBlank(message = "Account type is required")
        @JsonAlias({"accountType", "account_type"})
        private String accountType; // student, teacher, professional

        public String getAccountType() { return accountType; }
        public void setAccountType(String accountType) { this.accountType = accountType; }

        @JsonProperty("account_type")
        public void setAccount_type(String account_type) { this.accountType = account_type; }
    }

    public static class ForgotPasswordRequest {
        @NotBlank(message = "Email is required")
        @Email(message = "Valid email is required")
        private String email;

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
    }

    public static class ResetPasswordRequest {
        @NotBlank(message = "Token is required")
        private String token;

        @NotBlank(message = "New password is required")
        @Size(min = 6, message = "Password must be at least 6 characters")
        @JsonAlias({"newPassword", "new_password"})
        private String newPassword;

        @JsonAlias({"confirmPassword", "confirm_password"})
        private String confirmPassword;

        public String getToken() { return token; }
        public void setToken(String token) { this.token = token; }

        public String getNewPassword() { return newPassword; }
        public void setNewPassword(String newPassword) { this.newPassword = newPassword; }

        @JsonProperty("new_password")
        public void setNew_password(String new_password) { this.newPassword = new_password; }

        public String getConfirmPassword() { return confirmPassword; }
        public void setConfirmPassword(String confirmPassword) { this.confirmPassword = confirmPassword; }

        @JsonProperty("confirm_password")
        public void setConfirm_password(String confirm_password) { this.confirmPassword = confirm_password; }
    }
}
