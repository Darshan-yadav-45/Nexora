package ai.nexora.repository;

import ai.nexora.entity.PlannerTask;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface PlannerTaskRepository extends JpaRepository<PlannerTask, UUID> {
    List<PlannerTask> findByUserIdOrderByDueDateAsc(UUID userId);
    List<PlannerTask> findByUserIdAndStatusOrderByDueDateAsc(UUID userId, String status);
    Optional<PlannerTask> findByIdAndUserId(UUID id, UUID userId);
}

