package ai.nexora.service;

import ai.nexora.entity.CareerModule;
import ai.nexora.entity.CareerPath;
import ai.nexora.entity.CareerTopic;
import ai.nexora.repository.CareerModuleRepository;
import ai.nexora.repository.CareerPathRepository;
import ai.nexora.repository.CareerTopicRepository;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class CareerService {

    private final CareerPathRepository pathRepository;
    private final CareerModuleRepository moduleRepository;
    private final CareerTopicRepository topicRepository;

    public CareerService(
            CareerPathRepository pathRepository,
            CareerModuleRepository moduleRepository,
            CareerTopicRepository topicRepository) {
        this.pathRepository = pathRepository;
        this.moduleRepository = moduleRepository;
        this.topicRepository = topicRepository;
    }

    public List<CareerPath> getAllPaths() {
        return pathRepository.findAll();
    }

    public Map<String, Object> getPathDetails(String slug) {
        CareerPath path = pathRepository.findBySlug(slug)
                .orElseThrow(() -> new IllegalArgumentException("Career path not found: " + slug));

        List<CareerModule> modules = moduleRepository.findByCareerPathIdOrderByOrderIndexAsc(path.getId());
        List<Map<String, Object>> moduleList = new ArrayList<>();

        for (CareerModule m : modules) {
            List<CareerTopic> topics = topicRepository.findByCareerModuleIdOrderByOrderIndexAsc(m.getId());
            Map<String, Object> mMap = new HashMap<>();
            mMap.put("id", m.getId());
            mMap.put("title", m.getTitle());
            mMap.put("description", m.getDescription());
            mMap.put("difficultyLevel", m.getDifficultyLevel());
            mMap.put("estimatedHours", m.getEstimatedHours());
            mMap.put("topics", topics);
            moduleList.add(mMap);
        }

        Map<String, Object> response = new HashMap<>();
        response.put("path", path);
        response.put("modules", moduleList);
        return response;
    }
}

