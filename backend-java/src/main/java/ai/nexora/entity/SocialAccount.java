package ai.nexora.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "social_accounts")
public class SocialAccount {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(nullable = false, length = 50)
    private String platform; // github, linkedin, twitter, instagram, youtube, other

    @Column(name = "platform_user_id")
    private String platformUserId;

    private String username;

    @Column(name = "profile_url", nullable = false, length = 1000)
    private String profileUrl;

    @Column(name = "display_name")
    private String displayName;

    @Column(name = "avatar_url", length = 1000)
    private String avatarUrl;

    @Column(name = "connection_type")
    private String connectionType = "profile_link"; // oauth, profile_link

    @Column(name = "is_connected")
    private Boolean isConnected = false;

    @Column(name = "show_on_public_profile")
    private Boolean showOnPublicProfile = true;

    @Column(name = "encrypted_token", columnDefinition = "TEXT")
    private String encryptedToken;

    @Column(name = "created_at")
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "updated_at")
    private LocalDateTime updatedAt = LocalDateTime.now();

    public SocialAccount() {}

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getUserId() { return userId; }
    public void setUserId(UUID userId) { this.userId = userId; }

    public String getPlatform() { return platform; }
    public void setPlatform(String platform) { this.platform = platform; }

    public String getPlatformUserId() { return platformUserId; }
    public void setPlatformUserId(String platformUserId) { this.platformUserId = platformUserId; }

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

    public String getEncryptedToken() { return encryptedToken; }
    public void setEncryptedToken(String encryptedToken) { this.encryptedToken = encryptedToken; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
