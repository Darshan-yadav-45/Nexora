package ai.nexora.service;

import ai.nexora.entity.PlannerTask;
import ai.nexora.repository.PlannerTaskRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

@Service
public class PlannerService {

    private final PlannerTaskRepository taskRepository;

    public PlannerService(PlannerTaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    public List<PlannerTask> getTasks(UUID userId) {
        return taskRepository.findByUserIdOrderByDueDateAsc(userId);
    }

    @Transactional
    public PlannerTask createTask(UUID userId, PlannerTask task) {
        task.setUserId(userId);
        if (task.getStatus() == null) task.setStatus("Pending");
        if (task.getPriority() == null) task.setPriority("Medium");
        return taskRepository.save(task);
    }

    @Transactional
    public PlannerTask updateTask(UUID userId, UUID taskId, PlannerTask updated) {
        PlannerTask task = taskRepository.findByIdAndUserId(taskId, userId)
                .orElseThrow(() -> new IllegalArgumentException("Task not found"));

        if (updated.getTitle() != null) task.setTitle(updated.getTitle());
        if (updated.getDescription() != null) task.setDescription(updated.getDescription());
        if (updated.getStatus() != null) task.setStatus(updated.getStatus());
        if (updated.getPriority() != null) task.setPriority(updated.getPriority());
        if (updated.getDueDate() != null) task.setDueDate(updated.getDueDate());

        return taskRepository.save(task);
    }

    @Transactional
    public boolean deleteTask(UUID userId, UUID taskId) {
        PlannerTask task = taskRepository.findByIdAndUserId(taskId, userId)
                .orElseThrow(() -> new IllegalArgumentException("Task not found"));
        taskRepository.delete(task);
        return true;
    }
}

