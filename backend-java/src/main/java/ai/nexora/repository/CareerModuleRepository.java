package ai.nexora.repository;

import ai.nexora.entity.CareerModule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface CareerModuleRepository extends JpaRepository<CareerModule, UUID> {
    List<CareerModule> findByCareerPathIdOrderByOrderIndexAsc(UUID careerPathId);
}

