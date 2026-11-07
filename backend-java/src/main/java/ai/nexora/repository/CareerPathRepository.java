package ai.nexora.repository;

import ai.nexora.entity.CareerPath;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CareerPathRepository extends JpaRepository<CareerPath, UUID> {
    Optional<CareerPath> findBySlug(String slug);
    List<CareerPath> findByIsCustomFalseOrderByTitleAsc();
    List<CareerPath> findByUserId(UUID userId);
}

