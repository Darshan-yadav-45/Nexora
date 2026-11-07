package ai.nexora.repository;

import ai.nexora.entity.ResearchNotebook;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ResearchNotebookRepository extends JpaRepository<ResearchNotebook, UUID> {
    List<ResearchNotebook> findByUserIdOrderByUpdatedAtDesc(UUID userId);
    List<ResearchNotebook> findByUserIdOrderByIsPinnedDescUpdatedAtDesc(UUID userId);
    Optional<ResearchNotebook> findByIdAndUserId(UUID id, UUID userId);
}
