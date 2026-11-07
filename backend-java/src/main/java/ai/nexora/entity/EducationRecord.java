package ai.nexora.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "education_records")
public class EducationRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(nullable = false)
    private String level; // SSLC, PUC, Diploma, UG, PG, PhD, Other

    @Column(nullable = false)
    private String status = "Completed"; // Completed, Currently studying, Not started

    @Column(name = "institution_name")
    private String institutionName;

    @Column(name = "board_or_university")
    private String boardOrUniversity;

    private String stream;

    @Column(name = "degree_name")
    private String degreeName;

    private String specialization;

    @Column(name = "course_duration")
    private String courseDuration;

    @Column(name = "admission_year")
    private Integer admissionYear;

    @Column(name = "passing_year")
    private Integer passingYear;

    @Column(name = "expected_completion_year")
    private Integer expectedCompletionYear;

    @Column(name = "current_class_or_year")
    private String currentClassOrYear;

    @Column(name = "current_semester")
    private String currentSemester;

    @Column(name = "result_percentage_cgpa")
    private String resultPercentageCgpa;

    @Column(name = "research_title")
    private String researchTitle;

    @Column(name = "research_guide")
    private String researchGuide;

    @Column(name = "research_status")
    private String researchStatus;

    @Column(name = "chronological_order")
    private Integer chronologicalOrder = 1;

    @Column(name = "created_at")
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "updated_at")
    private LocalDateTime updatedAt = LocalDateTime.now();

    public EducationRecord() {}

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getUserId() { return userId; }
    public void setUserId(UUID userId) { this.userId = userId; }

    public String getLevel() { return level; }
    public void setLevel(String level) { this.level = level; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public String getInstitutionName() { return institutionName; }
    public void setInstitutionName(String institutionName) { this.institutionName = institutionName; }

    public String getBoardOrUniversity() { return boardOrUniversity; }
    public void setBoardOrUniversity(String boardOrUniversity) { this.boardOrUniversity = boardOrUniversity; }

    public String getStream() { return stream; }
    public void setStream(String stream) { this.stream = stream; }

    public String getDegreeName() { return degreeName; }
    public void setDegreeName(String degreeName) { this.degreeName = degreeName; }

    public String getSpecialization() { return specialization; }
    public void setSpecialization(String specialization) { this.specialization = specialization; }

    public String getCourseDuration() { return courseDuration; }
    public void setCourseDuration(String courseDuration) { this.courseDuration = courseDuration; }

    public Integer getAdmissionYear() { return admissionYear; }
    public void setAdmissionYear(Integer admissionYear) { this.admissionYear = admissionYear; }

    public Integer getPassingYear() { return passingYear; }
    public void setPassingYear(Integer passingYear) { this.passingYear = passingYear; }

    public Integer getExpectedCompletionYear() { return expectedCompletionYear; }
    public void setExpectedCompletionYear(Integer expectedCompletionYear) { this.expectedCompletionYear = expectedCompletionYear; }

    public String getCurrentClassOrYear() { return currentClassOrYear; }
    public void setCurrentClassOrYear(String currentClassOrYear) { this.currentClassOrYear = currentClassOrYear; }

    public String getCurrentSemester() { return currentSemester; }
    public void setCurrentSemester(String currentSemester) { this.currentSemester = currentSemester; }

    public String getResultPercentageCgpa() { return resultPercentageCgpa; }
    public void setResultPercentageCgpa(String resultPercentageCgpa) { this.resultPercentageCgpa = resultPercentageCgpa; }

    public String getResearchTitle() { return researchTitle; }
    public void setResearchTitle(String researchTitle) { this.researchTitle = researchTitle; }

    public String getResearchGuide() { return researchGuide; }
    public void setResearchGuide(String researchGuide) { this.researchGuide = researchGuide; }

    public String getResearchStatus() { return researchStatus; }
    public void setResearchStatus(String researchStatus) { this.researchStatus = researchStatus; }

    public Integer getChronologicalOrder() { return chronologicalOrder; }
    public void setChronologicalOrder(Integer chronologicalOrder) { this.chronologicalOrder = chronologicalOrder; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}
