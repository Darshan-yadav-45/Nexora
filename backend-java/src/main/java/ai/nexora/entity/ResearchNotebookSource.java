package ai.nexora.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "research_notebook_sources")
public class ResearchNotebookSource {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private UUID id;

    @Column(name = "notebook_id", nullable = false)
    private UUID notebookId;

    @Column(name = "user_id", nullable = false)
    private UUID userId;

    @Column(nullable = false, length = 500)
    private String title;

    @Column(name = "file_name")
    private String fileName;

    @Column(name = "source_type", length = 50)
    private String sourceType = "file"; // file, text, url

    @Column(name = "file_path", length = 1000)
    private String filePath;

    @Column(name = "source_url", length = 1000)
    private String sourceUrl;

    @Column(name = "processing_status", length = 50)
    private String processingStatus = "completed"; // pending, processing, completed, failed

    @Column(name = "processing_progress")
    private Integer processingProgress = 100;

    @Column(columnDefinition = "TEXT")
    private String overview;

    @Column(name = "extracted_text", columnDefinition = "TEXT")
    private String extractedText;

    @Column(name = "page_count")
    private Integer pageCount = 1;

    @Column(name = "created_at")
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "updated_at")
    private LocalDateTime updatedAt = LocalDateTime.now();

    public ResearchNotebookSource() {}

    public ResearchNotebookSource(UUID notebookId, UUID userId, String title, String sourceType) {
        this.notebookId = notebookId;
        this.userId = userId;
        this.title = title;
        this.sourceType = sourceType;
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }

    public UUID getNotebookId() { return notebookId; }
    public void setNotebookId(UUID notebookId) { this.notebookId = notebookId; }

    public UUID getUserId() { return userId; }
    public void setUserId(UUID userId) { this.userId = userId; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getFileName() { return fileName; }
    public void setFileName(String fileName) { this.fileName = fileName; }

    public String getSourceType() { return sourceType; }
    public void setSourceType(String sourceType) { this.sourceType = sourceType; }

    public String getFilePath() { return filePath; }
    public void setFilePath(String filePath) { this.filePath = filePath; }

    public String getSourceUrl() { return sourceUrl; }
    public void setSourceUrl(String sourceUrl) { this.sourceUrl = sourceUrl; }

    public String getProcessingStatus() { return processingStatus; }
    public void setProcessingStatus(String processingStatus) { this.processingStatus = processingStatus; }

    public Integer getProcessingProgress() { return processingProgress; }
    public void setProcessingProgress(Integer processingProgress) { this.processingProgress = processingProgress; }

    public String getOverview() { return overview; }
    public void setOverview(String overview) { this.overview = overview; }

    public String getExtractedText() { return extractedText; }
    public void setExtractedText(String extractedText) { this.extractedText = extractedText; }

    public Integer getPageCount() { return pageCount; }
    public void setPageCount(Integer pageCount) { this.pageCount = pageCount; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
}

