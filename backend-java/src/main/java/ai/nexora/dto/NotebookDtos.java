package ai.nexora.dto;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

public class NotebookDtos {

    public static class CreateNotebookRequest {
        private String title;
        private String description;
        private String domainArea;
        private String category;

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }

        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }

        public String getDomainArea() { return domainArea; }
        public void setDomainArea(String domainArea) { this.domainArea = domainArea; }

        public String getCategory() { return category; }
        public void setCategory(String category) { this.category = category; }
    }

    public static class NotebookDto {
        private UUID id;
        private UUID userId;
        private String title;
        private String description;
        private String domainArea;
        private String category;
        private Boolean isPinned;
        private Long sourceCount;
        private Long noteCount;
        private LocalDateTime createdAt;
        private LocalDateTime updatedAt;

        public UUID getId() { return id; }
        public void setId(UUID id) { this.id = id; }

        public UUID getUserId() { return userId; }
        public void setUserId(UUID userId) { this.userId = userId; }

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }

        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }

        public String getDomainArea() { return domainArea; }
        public void setDomainArea(String domainArea) { this.domainArea = domainArea; }

        public String getCategory() { return category; }
        public void setCategory(String category) { this.category = category; }

        public Boolean getIsPinned() { return isPinned; }
        public void setIsPinned(Boolean isPinned) { this.isPinned = isPinned; }

        public Long getSourceCount() { return sourceCount; }
        public void setSourceCount(Long sourceCount) { this.sourceCount = sourceCount; }

        public Long getNoteCount() { return noteCount; }
        public void setNoteCount(Long noteCount) { this.noteCount = noteCount; }

        public LocalDateTime getCreatedAt() { return createdAt; }
        public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

        public LocalDateTime getUpdatedAt() { return updatedAt; }
        public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }
    }

    public static class ChatRequest {
        private String message;
        private List<UUID> selectedSourceIds;
        private String tone = "academic"; // academic, simple, balanced, executive
        private Boolean humanize = false;

        public String getMessage() { return message; }
        public void setMessage(String message) { this.message = message; }

        public List<UUID> getSelectedSourceIds() { return selectedSourceIds; }
        public void setSelectedSourceIds(List<UUID> selectedSourceIds) { this.selectedSourceIds = selectedSourceIds; }

        public String getTone() { return tone; }
        public void setTone(String tone) { this.tone = tone; }

        public Boolean getHumanize() { return humanize; }
        public void setHumanize(Boolean humanize) { this.humanize = humanize; }
    }

    public static class HumanizeRequest {
        private String text;
        private String style = "student"; // student, researcher, professional
        private String tone = "clear"; // clear, conversational, academic

        public String getText() { return text; }
        public void setText(String text) { this.text = text; }

        public String getStyle() { return style; }
        public void setStyle(String style) { this.style = style; }

        public String getTone() { return tone; }
        public void setTone(String tone) { this.tone = tone; }
    }

    public static class StudioToolRequest {
        private String tool;
        private String prompt;
        private List<UUID> sourceIds;

        public String getTool() { return tool; }
        public void setTool(String tool) { this.tool = tool; }

        public String getPrompt() { return prompt; }
        public void setPrompt(String prompt) { this.prompt = prompt; }

        public List<UUID> getSourceIds() { return sourceIds; }
        public void setSourceIds(List<UUID> sourceIds) { this.sourceIds = sourceIds; }
    }

    public static class CreateNoteRequest {
        private String title;
        private String content;
        private String category = "General";
        private Boolean isPinned = false;

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }

        public String getContent() { return content; }
        public void setContent(String content) { this.content = content; }

        public String getCategory() { return category; }
        public void setCategory(String category) { this.category = category; }

        public Boolean getIsPinned() { return isPinned; }
        public void setIsPinned(Boolean isPinned) { this.isPinned = isPinned; }
    }

    public static class AddSourceTextRequest {
        private String title;
        private String contentText;

        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }

        public String getContentText() { return contentText; }
        public void setContentText(String contentText) { this.contentText = contentText; }
    }
}

