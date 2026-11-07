package ai.nexora.repository;

import ai.nexora.entity.ResearchNote;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ResearchNoteRepository extends JpaRepository<ResearchNote, UUID> {
    List<ResearchNote> findByNotebookIdOrderByCreatedAtDesc(UUID notebookId);
    List<ResearchNote> findByUserIdOrderByCreatedAtDesc(UUID userId);
    Optional<ResearchNote> findByIdAndUserId(UUID id, UUID userId);
    long countByNotebookId(UUID notebookId);
}

