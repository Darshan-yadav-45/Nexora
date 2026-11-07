package ai.nexora.dto;

import java.time.LocalDateTime;
import java.util.UUID;

public class SocialDtos {

    public static class ConnectGithubRequest {
        private String username;
        private String token;
        private String profileUrl;

        public String getUsername() { return username; }
        public void setUsername(String username) { this.username = username; }

        public String getToken() { return token; }
        public void setToken(String token) { this.token = token; }

        public String getProfileUrl() { return profileUrl; }
        public void setProfileUrl(String profileUrl) { this.profileUrl = profileUrl; }
    }

    public static class AddProfileLinkRequest {
        private String platform;
        private String profileUrl;
        private String username;
        private String displayName;

        public String getPlatform() { return platform; }
        public void setPlatform(String platform) { this.platform = platform; }

        public String getProfileUrl() { return profileUrl; }
        public void setProfileUrl(String profileUrl) { this.profileUrl = profileUrl; }

        public String getUsername() { return username; }
        public void setUsername(String username) { this.username = username; }

        public String getDisplayName() { return displayName; }
        public void setDisplayName(String displayName) { this.displayName = displayName; }
    }

    public static class SocialAccountDto {
        private UUID id;
        private String platform;
        private String username;
        private String profileUrl;
        private String displayName;
        private String avatarUrl;
        private String connectionType;
        private Boolean isConnected;
        private Boolean showOnPublicProfile;
        private LocalDateTime createdAt;

        public UUID getId() { return id; }
        public void setId(UUID id) { this.id = id; }

        public String getPlatform() { return platform; }
        public void setPlatform(String platform) { this.platform = platform; }

        public String getUsername() { return username; }
        public void setUsername(String username) { this.username = username; }

        public String getProfileUrl() { return profileUrl; }
        public void setProfileUrl(String profileUrl) { this.profileUrl = profileUrl; }

        public String getDisplayName() { return displayName; }
        public void setDisplayName(String displayName) { this.displayName = displayName; }

        public String getAvatarUrl() { return avatarUrl; }
        public void setAvatarUrl(String avatarUrl) { this.avatarUrl = avatarUrl; }

        public String getConnectionType() { return connectionType; }
        public void setConnectionType(String connectionType) { this.connectionType = connectionType; }

        public Boolean getIsConnected() { return isConnected; }
        public void setIsConnected(Boolean isConnected) { this.isConnected = isConnected; }

        public Boolean getShowOnPublicProfile() { return showOnPublicProfile; }
        public void setShowOnPublicProfile(Boolean showOnPublicProfile) { this.showOnPublicProfile = showOnPublicProfile; }

        public LocalDateTime getCreatedAt() { return createdAt; }
        public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    }
}

