package ai.nexora.controller;

import ai.nexora.dto.EducationDtos;
import ai.nexora.entity.*;
import ai.nexora.service.EducationService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/education")
public class EducationController {

    private final EducationService educationService;

    public EducationController(EducationService educationService) {
        this.educationService = educationService;
    }

    @PutMapping("/personal-info")
    public ResponseEntity<UserProfile> updatePersonalInfo(
            @AuthenticationPrincipal User user,
            @RequestBody EducationDtos.PersonalInfoRequest req) {
        return ResponseEntity.ok(educationService.updatePersonalInfo(user.getId(), req));
    }

    @GetMapping("/records")
    public ResponseEntity<List<EducationRecord>> getRecords(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(educationService.getEducationRecords(user.getId()));
    }

    @PostMapping("/records")
    public ResponseEntity<EducationRecord> saveRecord(
            @AuthenticationPrincipal User user,
            @RequestBody EducationDtos.EducationRecordRequest req) {
        return ResponseEntity.ok(educationService.saveEducationRecord(user.getId(), req));
    }

    @GetMapping("/subjects")
    public ResponseEntity<List<UserSubject>> getSubjects(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(educationService.getSubjects(user.getId()));
    }

    @PostMapping("/subjects")
    public ResponseEntity<UserSubject> addSubject(
            @AuthenticationPrincipal User user,
            @RequestBody EducationDtos.SubjectRequest req) {
        return ResponseEntity.ok(educationService.addSubject(user.getId(), req));
    }

    @PostMapping("/syllabus/text")
    public ResponseEntity<Syllabus> addSyllabusText(
            @AuthenticationPrincipal User user,
            @RequestBody EducationDtos.SyllabusTextRequest req) {
        return ResponseEntity.ok(educationService.addSyllabusText(user.getId(), req));
    }

    @GetMapping("/timeline")
    public ResponseEntity<Map<String, Object>> getTimeline(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(educationService.getTimeline(user.getId()));
    }

    @PostMapping("/complete")
    public ResponseEntity<Map<String, Object>> completeEducation(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(educationService.completeEducationProfile(user.getId()));
    }
}

