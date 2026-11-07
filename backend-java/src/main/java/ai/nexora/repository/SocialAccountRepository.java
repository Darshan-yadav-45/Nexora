package ai.nexora.repository;

import ai.nexora.entity.SocialAccount;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface SocialAccountRepository extends JpaRepository<SocialAccount, UUID> {
    List<SocialAccount> findByUserIdOrderByCreatedAtDesc(UUID userId);
    List<SocialAccount> findByUserIdOrderByCreatedAtAsc(UUID userId);
    Optional<SocialAccount> findByUserIdAndPlatform(UUID userId, String platform);
    Optional<SocialAccount> findByIdAndUserId(UUID id, UUID userId);
}
