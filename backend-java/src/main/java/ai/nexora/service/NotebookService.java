package ai.nexora.service;

import ai.nexora.dto.NotebookDtos;
import ai.nexora.entity.ResearchNote;
import ai.nexora.entity.ResearchNotebook;
import ai.nexora.entity.ResearchNotebookSource;
import ai.nexora.repository.ResearchNoteRepository;
import ai.nexora.repository.ResearchNotebookRepository;
import ai.nexora.repository.ResearchNotebookSourceRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
import java.util.stream.Collectors;

@Service
public class NotebookService {

    private final ResearchNotebookRepository notebookRepository;
    private final ResearchNotebookSourceRepository sourceRepository;
    private final ResearchNoteRepository noteRepository;
    private final AiMicroserviceClient aiClient;

    public NotebookService(
            ResearchNotebookRepository notebookRepository,
            ResearchNotebookSourceRepository sourceRepository,
            ResearchNoteRepository noteRepository,
            AiMicroserviceClient aiClient) {
        this.notebookRepository = notebookRepository;
        this.sourceRepository = sourceRepository;
        this.noteRepository = noteRepository;
        this.aiClient = aiClient;
    }

    public List<NotebookDtos.NotebookDto> getNotebooks(UUID userId) {
        List<ResearchNotebook> notebooks = notebookRepository.findByUserIdOrderByUpdatedAtDesc(userId);
        return notebooks.stream().map(nb -> {
            NotebookDtos.NotebookDto dto = new NotebookDtos.NotebookDto();
            dto.setId(nb.getId());
            dto.setUserId(nb.getUserId());
            dto.setTitle(nb.getTitle());
            dto.setDescription(nb.getDescription());
            dto.setDomainArea(nb.getDomainArea());
            dto.setCategory(nb.getCategory());
            dto.setIsPinned(nb.getIsPinned());
            dto.setSourceCount(sourceRepository.countByNotebookId(nb.getId()));
            dto.setNoteCount(noteRepository.countByNotebookId(nb.getId()));
            dto.setCreatedAt(nb.getCreatedAt());
            dto.setUpdatedAt(nb.getUpdatedAt());
            return dto;
        }).collect(Collectors.toList());
    }

    public ResearchNotebook getNotebook(UUID id, UUID userId) {
        return notebookRepository.findByIdAndUserId(id, userId)
                .orElseThrow(() -> new IllegalArgumentException("Notebook not found"));
    }

    @Transactional
    public ResearchNotebook createNotebook(UUID userId, NotebookDtos.CreateNotebookRequest req) {
        ResearchNotebook nb = new ResearchNotebook(userId, req.getTitle());
        nb.setDescription(req.getDescription());
        nb.setDomainArea(req.getDomainArea());
        if (req.getCategory() != null) {
            nb.setCategory(req.getCategory());
        }
        return notebookRepository.save(nb);
    }

    public List<ResearchNotebookSource> getSources(UUID notebookId) {
        return sourceRepository.findByNotebookIdOrderByCreatedAtDesc(notebookId);
    }

    @Transactional
    public ResearchNotebookSource addTextSource(UUID userId, UUID notebookId, NotebookDtos.AddSourceTextRequest req) {
        ResearchNotebookSource src = new ResearchNotebookSource(notebookId, userId, req.getTitle(), "text");
        src.setExtractedText(req.getContentText());
        src.setProcessingStatus("completed");
        src.setProcessingProgress(100);
        src.setOverview(req.getContentText().length() > 200 ? req.getContentText().substring(0, 200) + "..." : req.getContentText());
        return sourceRepository.save(src);
    }

    public List<ResearchNote> getNotes(UUID notebookId) {
        return noteRepository.findByNotebookIdOrderByCreatedAtDesc(notebookId);
    }

    @Transactional
    public ResearchNote createNote(UUID userId, UUID notebookId, NotebookDtos.CreateNoteRequest req) {
        ResearchNote note = new ResearchNote(userId, notebookId, req.getTitle(), req.getContent());
        if (req.getCategory() != null) note.setCategory(req.getCategory());
        if (req.getIsPinned() != null) note.setIsPinned(req.getIsPinned());
        return noteRepository.save(note);
    }

    public Map<String, Object> executeGroundedChat(UUID userId, String email, NotebookDtos.ChatRequest req) {
        return aiClient.callGroundedChat(userId, email, req);
    }

    public Map<String, Object> executeHumanize(UUID userId, String email, NotebookDtos.HumanizeRequest req) {
        return aiClient.callHumanize(userId, email, req);
    }

    public Map<String, Object> executeStudioTool(UUID userId, String email, String toolName, NotebookDtos.StudioToolRequest req) {
        return aiClient.callStudioTool(userId, email, toolName, req);
    }
}

