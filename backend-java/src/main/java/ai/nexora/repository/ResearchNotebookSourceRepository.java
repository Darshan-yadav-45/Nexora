package ai.nexora.repository;

import ai.nexora.entity.ResearchNotebookSource;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ResearchNotebookSourceRepository extends JpaRepository<ResearchNotebookSource, UUID> {
    List<ResearchNotebookSource> findByNotebookIdOrderByCreatedAtDesc(UUID notebookId);
    List<ResearchNotebookSource> findByUserIdOrderByCreatedAtDesc(UUID userId);
    Optional<ResearchNotebookSource> findByIdAndUserId(UUID id, UUID userId);
    long countByNotebookId(UUID notebookId);
    void deleteByNotebookId(UUID notebookId);
}

