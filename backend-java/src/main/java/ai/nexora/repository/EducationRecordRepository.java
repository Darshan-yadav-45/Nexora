package ai.nexora.repository;

import ai.nexora.entity.EducationRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface EducationRecordRepository extends JpaRepository<EducationRecord, UUID> {
    List<EducationRecord> findByUserIdOrderByChronologicalOrderAsc(UUID userId);
    List<EducationRecord> findByUserIdOrderByChronologicalOrderAscCreatedAtAsc(UUID userId);
    Optional<EducationRecord> findByIdAndUserId(UUID id, UUID userId);
}
