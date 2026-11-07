package ai.nexora.repository;

import ai.nexora.entity.CareerTopic;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CareerTopicRepository extends JpaRepository<CareerTopic, UUID> {
    List<CareerTopic> findByCareerModuleIdOrderByOrderIndexAsc(UUID careerModuleId);
    Optional<CareerTopic> findBySlug(String slug);
}

