package ai.nexora.dto;

import java.util.List;
import java.util.UUID;

public class EducationDtos {

    public static class PersonalInfoRequest {
        private String name;
        private String preferredName;
        private String email;
        private String phoneNumber;
        private String dateOfBirth;
        private String country;
        private String state;
        private String city;
        private String preferredLanguage;

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }

        public String getPreferredName() { return preferredName; }
        public void setPreferredName(String preferredName) { this.preferredName = preferredName; }

        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }

        public String getPhoneNumber() { return phoneNumber; }
        public void setPhoneNumber(String phoneNumber) { this.phoneNumber = phoneNumber; }

        public String getDateOfBirth() { return dateOfBirth; }
        public void setDateOfBirth(String dateOfBirth) { this.dateOfBirth = dateOfBirth; }

        public String getCountry() { return country; }
        public void setCountry(String country) { this.country = country; }

        public String getState() { return state; }
        public void setState(String state) { this.state = state; }

        public String getCity() { return city; }
        public void setCity(String city) { this.city = city; }

        public String getPreferredLanguage() { return preferredLanguage; }
        public void setPreferredLanguage(String preferredLanguage) { this.preferredLanguage = preferredLanguage; }
    }

    public static class EducationRecordRequest {
        private UUID id;
        private String level; // SSLC, PUC, Diploma, UG, PG, PhD, Other
        private String status; // Completed, Currently studying, Not started
        private String institutionName;
        private String boardOrUniversity;
        private String stream;
        private String degreeName;
        private String specialization;
        private String courseDuration;
        private Integer admissionYear;
        private Integer passingYear;
        private Integer expectedCompletionYear;
        private String currentClassOrYear;
        private String currentSemester;
        private String resultPercentageCgpa;
        private String researchTitle;
        private String researchGuide;
        private String researchStatus;
        private Integer chronologicalOrder;

        public UUID getId() { return id; }
        public void setId(UUID id) { this.id = id; }

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
    }

    public static class SubjectRequest {
        private UUID educationRecordId;
        private String name;
        private String code;
        private Integer credits;
        private String description;

        public UUID getEducationRecordId() { return educationRecordId; }
        public void setEducationRecordId(UUID educationRecordId) { this.educationRecordId = educationRecordId; }

        public String getName() { return name; }
        public void setName(String name) { this.name = name; }

        public String getCode() { return code; }
        public void setCode(String code) { this.code = code; }

        public Integer getCredits() { return credits; }
        public void setCredits(Integer credits) { this.credits = credits; }

        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
    }

    public static class SyllabusTextRequest {
        private UUID subjectId;
        private String title;
        private String contentText;

        public UUID getSubjectId() { return subjectId; }
        public void setSubjectId(UUID subjectId) { this.subjectId = subjectId; }

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }

        public String getContentText() { return contentText; }
        public void setContentText(String contentText) { this.contentText = contentText; }
    }

    public static class LearningPreferencesRequest {
        private String learningGoal;
        private String targetRole;
        private String weeklyTargetHours;
        private List<String> preferredSkills;

        public String getLearningGoal() { return learningGoal; }
        public void setLearningGoal(String learningGoal) { this.learningGoal = learningGoal; }

        public String getTargetRole() { return targetRole; }
        public void setTargetRole(String targetRole) { this.targetRole = targetRole; }

        public String getWeeklyTargetHours() { return weeklyTargetHours; }
        public void setWeeklyTargetHours(String weeklyTargetHours) { this.weeklyTargetHours = weeklyTargetHours; }

        public List<String> getPreferredSkills() { return preferredSkills; }
        public void setPreferredSkills(List<String> preferredSkills) { this.preferredSkills = preferredSkills; }
    }
}

