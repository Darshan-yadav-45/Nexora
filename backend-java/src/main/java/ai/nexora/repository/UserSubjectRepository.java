package ai.nexora.repository;

import ai.nexora.entity.UserSubject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface UserSubjectRepository extends JpaRepository<UserSubject, UUID> {
    List<UserSubject> findByUserIdOrderByCreatedAtDesc(UUID userId);
    List<UserSubject> findByUserIdAndIsActiveTrueOrderByCreatedAtAsc(UUID userId);
    Optional<UserSubject> findByIdAndUserId(UUID id, UUID userId);
}
