package ai.nexora.controller;

import ai.nexora.entity.CareerPath;
import ai.nexora.service.CareerService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/career")
public class CareerController {

    private final CareerService careerService;

    public CareerController(CareerService careerService) {
        this.careerService = careerService;
    }

    @GetMapping("/paths")
    public ResponseEntity<List<CareerPath>> getPaths() {
        return ResponseEntity.ok(careerService.getAllPaths());
    }

    @GetMapping("/paths/{slug}")
    public ResponseEntity<Map<String, Object>> getPathDetails(@PathVariable String slug) {
        return ResponseEntity.ok(careerService.getPathDetails(slug));
    }
}

