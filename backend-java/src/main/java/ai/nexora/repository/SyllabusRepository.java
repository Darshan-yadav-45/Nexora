package ai.nexora.repository;

import ai.nexora.entity.Syllabus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface SyllabusRepository extends JpaRepository<Syllabus, UUID> {
    List<Syllabus> findByUserSubjectId(UUID userSubjectId);
    List<Syllabus> findByUserId(UUID userId);
}
