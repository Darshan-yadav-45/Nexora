package ai.nexora.service;

import ai.nexora.dto.EducationDtos;
import ai.nexora.entity.*;
import ai.nexora.repository.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;

@Service
public class EducationService {

    private final UserProfileRepository userProfileRepository;
    private final EducationRecordRepository educationRecordRepository;
    private final UserSubjectRepository userSubjectRepository;
    private final SyllabusRepository syllabusRepository;
    private final UserRepository userRepository;

    public EducationService(
            UserProfileRepository userProfileRepository,
            EducationRecordRepository educationRecordRepository,
            UserSubjectRepository userSubjectRepository,
            SyllabusRepository syllabusRepository,
            UserRepository userRepository) {
        this.userProfileRepository = userProfileRepository;
        this.educationRecordRepository = educationRecordRepository;
        this.userSubjectRepository = userSubjectRepository;
        this.syllabusRepository = syllabusRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public UserProfile updatePersonalInfo(UUID userId, EducationDtos.PersonalInfoRequest req) {
        UserProfile profile = userProfileRepository.findByUserId(userId)
                .orElse(new UserProfile(userId, req.getName() != null ? req.getName() : "User"));

        if (req.getName() != null) profile.setName(req.getName());
        if (req.getPreferredName() != null) profile.setPreferredName(req.getPreferredName());
        if (req.getPhoneNumber() != null) profile.setPhoneNumber(req.getPhoneNumber());
        if (req.getDateOfBirth() != null) profile.setDateOfBirth(req.getDateOfBirth());
        if (req.getCountry() != null) profile.setCountry(req.getCountry());
        if (req.getState() != null) profile.setState(req.getState());
        if (req.getCity() != null) profile.setCity(req.getCity());
        if (req.getPreferredLanguage() != null) profile.setNativeLanguage(req.getPreferredLanguage());

        return userProfileRepository.save(profile);
    }

    public List<EducationRecord> getEducationRecords(UUID userId) {
        return educationRecordRepository.findByUserIdOrderByChronologicalOrderAsc(userId);
    }

    @Transactional
    public EducationRecord saveEducationRecord(UUID userId, EducationDtos.EducationRecordRequest req) {
        EducationRecord record;
        if (req.getId() != null) {
            record = educationRecordRepository.findByIdAndUserId(req.getId(), userId)
                    .orElse(new EducationRecord());
        } else {
            record = new EducationRecord();
            record.setUserId(userId);
        }

        record.setLevel(req.getLevel());
        record.setStatus(req.getStatus() != null ? req.getStatus() : "Completed");
        record.setInstitutionName(req.getInstitutionName());
        record.setBoardOrUniversity(req.getBoardOrUniversity());
        record.setStream(req.getStream());
        record.setDegreeName(req.getDegreeName());
        record.setSpecialization(req.getSpecialization());
        record.setCourseDuration(req.getCourseDuration());
        record.setAdmissionYear(req.getAdmissionYear());
        record.setPassingYear(req.getPassingYear());
        record.setExpectedCompletionYear(req.getExpectedCompletionYear());
        record.setCurrentClassOrYear(req.getCurrentClassOrYear());
        record.setCurrentSemester(req.getCurrentSemester());
        record.setResultPercentageCgpa(req.getResultPercentageCgpa());
        record.setResearchTitle(req.getResearchTitle());
        record.setResearchGuide(req.getResearchGuide());
        record.setResearchStatus(req.getResearchStatus());
        if (req.getChronologicalOrder() != null) {
            record.setChronologicalOrder(req.getChronologicalOrder());
        }

        return educationRecordRepository.save(record);
    }

    public List<UserSubject> getSubjects(UUID userId) {
        return userSubjectRepository.findByUserIdOrderByCreatedAtDesc(userId);
    }

    @Transactional
    public UserSubject addSubject(UUID userId, EducationDtos.SubjectRequest req) {
        UserSubject subject = new UserSubject();
        subject.setUserId(userId);
        subject.setEducationRecordId(req.getEducationRecordId());
        subject.setName(req.getName());
        subject.setCode(req.getCode());
        subject.setCredits(req.getCredits() != null ? req.getCredits() : 4);
        subject.setDescription(req.getDescription());
        subject.setIsActive(true);
        return userSubjectRepository.save(subject);
    }

    @Transactional
    public Syllabus addSyllabusText(UUID userId, EducationDtos.SyllabusTextRequest req) {
        Syllabus syllabus = new Syllabus();
        syllabus.setUserId(userId);
        syllabus.setUserSubjectId(req.getSubjectId());
        syllabus.setTitle(req.getTitle() != null ? req.getTitle() : "Syllabus Content");
        syllabus.setSourceType("pasted_text");
        syllabus.setContentText(req.getContentText());
        return syllabusRepository.save(syllabus);
    }

    @Transactional
    public Map<String, Object> completeEducationProfile(UUID userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));
        user.setProfileCompleted(true);
        userRepository.save(user);

        Map<String, Object> result = new HashMap<>();
        result.put("message", "Education journey profile completed successfully");
        result.put("profileCompleted", true);
        result.put("userId", userId);
        return result;
    }

    public Map<String, Object> getTimeline(UUID userId) {
        List<EducationRecord> records = educationRecordRepository.findByUserIdOrderByChronologicalOrderAsc(userId);
        List<UserSubject> subjects = userSubjectRepository.findByUserIdOrderByCreatedAtDesc(userId);

        Map<String, Object> timeline = new HashMap<>();
        timeline.put("records", records);
        timeline.put("subjects", subjects);
        timeline.put("totalRecords", records.size());
        timeline.put("totalSubjects", subjects.size());
        return timeline;
    }
}

