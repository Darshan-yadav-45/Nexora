package ai.nexora.controller;

import ai.nexora.dto.NotebookDtos;
import ai.nexora.entity.ResearchNote;
import ai.nexora.entity.ResearchNotebook;
import ai.nexora.entity.ResearchNotebookSource;
import ai.nexora.entity.User;
import ai.nexora.service.NotebookService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/notebooks")
public class NotebookController {

    private final NotebookService notebookService;

    public NotebookController(NotebookService notebookService) {
        this.notebookService = notebookService;
    }

    @GetMapping
    public ResponseEntity<List<NotebookDtos.NotebookDto>> getNotebooks(@AuthenticationPrincipal User user) {
        return ResponseEntity.ok(notebookService.getNotebooks(user.getId()));
    }

    @PostMapping
    public ResponseEntity<ResearchNotebook> createNotebook(
            @AuthenticationPrincipal User user,
            @RequestBody NotebookDtos.CreateNotebookRequest req) {
        return ResponseEntity.ok(notebookService.createNotebook(user.getId(), req));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ResearchNotebook> getNotebook(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id) {
        return ResponseEntity.ok(notebookService.getNotebook(id, user.getId()));
    }

    @GetMapping("/{id}/sources")
    public ResponseEntity<List<ResearchNotebookSource>> getSources(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id) {
        // verify ownership
        notebookService.getNotebook(id, user.getId());
        return ResponseEntity.ok(notebookService.getSources(id));
    }

    @PostMapping("/{id}/sources/text")
    public ResponseEntity<ResearchNotebookSource> addTextSource(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id,
            @RequestBody NotebookDtos.AddSourceTextRequest req) {
        // verify ownership
        notebookService.getNotebook(id, user.getId());
        return ResponseEntity.ok(notebookService.addTextSource(user.getId(), id, req));
    }

    @GetMapping("/{id}/notes")
    public ResponseEntity<List<ResearchNote>> getNotes(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id) {
        // verify ownership
        notebookService.getNotebook(id, user.getId());
        return ResponseEntity.ok(notebookService.getNotes(id));
    }

    @PostMapping("/{id}/notes")
    public ResponseEntity<ResearchNote> createNote(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id,
            @RequestBody NotebookDtos.CreateNoteRequest req) {
        // verify ownership
        notebookService.getNotebook(id, user.getId());
        return ResponseEntity.ok(notebookService.createNote(user.getId(), id, req));
    }

    @PostMapping("/{id}/chat")
    public ResponseEntity<Map<String, Object>> chat(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id,
            @RequestBody NotebookDtos.ChatRequest req) {
        // verify ownership
        notebookService.getNotebook(id, user.getId());
        return ResponseEntity.ok(notebookService.executeGroundedChat(user.getId(), user.getEmail(), req));
    }

    @PostMapping("/{id}/humanize")
    public ResponseEntity<Map<String, Object>> humanize(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id,
            @RequestBody NotebookDtos.HumanizeRequest req) {
        notebookService.getNotebook(id, user.getId());
        return ResponseEntity.ok(notebookService.executeHumanize(user.getId(), user.getEmail(), req));
    }

    @PostMapping("/{id}/studio/{toolName}")
    public ResponseEntity<Map<String, Object>> studioTool(
            @AuthenticationPrincipal User user,
            @PathVariable UUID id,
            @PathVariable String toolName,
            @RequestBody NotebookDtos.StudioToolRequest req) {
        notebookService.getNotebook(id, user.getId());
        return ResponseEntity.ok(notebookService.executeStudioTool(user.getId(), user.getEmail(), toolName, req));
    }
}

