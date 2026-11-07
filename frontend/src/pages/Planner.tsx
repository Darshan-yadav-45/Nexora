import { useState, useEffect } from 'react';
import { CheckSquare, Plus, CheckCircle2, Calendar, Trash2 } from 'lucide-react';
import api from '../services/api';

export default function Planner() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterSource, setFilterSource] = useState<string>('all');

  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDesc, setNewTaskDesc] = useState('');
  const [newTaskPriority, setNewTaskPriority] = useState('Medium');
  const [newTaskDueDate, setNewTaskDueDate] = useState('');

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const res = await api.get('/integration/planner/tasks');
      setTasks(res.data);
    } catch (err) {
      console.error('Error loading planner tasks:', err);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const res = await api.post('/integration/planner/tasks', {
        title: newTaskTitle,
        description: newTaskDesc,
        priority: newTaskPriority,
        due_date: newTaskDueDate ? new Date(newTaskDueDate).toISOString() : null,
        source_module: 'manual'
      });
      setTasks([res.data, ...tasks]);
      setNewTaskTitle('');
      setNewTaskDesc('');
      setNewTaskDueDate('');
    } catch (err) {
      console.error('Error creating task:', err);
    }
  };

  const handleToggleTask = async (task: any) => {
    const nextStatus = task.status === 'Completed' ? 'Todo' : 'Completed';
    try {
      await api.put(`/integration/planner/tasks/${task.id}`, { status: nextStatus });
      setTasks(tasks.map(t => t.id === task.id ? { ...t, status: nextStatus } : t));
    } catch (err) {
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await api.delete(`/integration/planner/tasks/${taskId}`);
      setTasks(tasks.filter(t => t.id !== taskId));
    } catch (err) {
      console.error('Error deleting task:', err);
    }
  };

  const filteredTasks = tasks.filter(t => {
    if (filterStatus === 'todo' && t.status === 'Completed') return false;
    if (filterStatus === 'completed' && t.status !== 'Completed') return false;
    if (filterSource !== 'all' && t.source_module !== filterSource) return false;
    return true;
  });

  return (
    <div className="w-full max-w-5xl mx-auto space-y-6 pb-20">
      
      {/* Header */}
      <div className="p-6 rounded-2xl bg-dark-card border border-white/10 glass-panel flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 text-amber-400 text-xs font-semibold mb-2">
            <CheckSquare className="w-3.5 h-3.5" />
            Unified Academic & Career Planner
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white">Daily Learning & Research Tasks</h1>
          <p className="text-xs text-gray-400 mt-1">
            Centrally manages study deadlines, experiment milestones, and literature review deliverables.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <span className="px-3 py-1.5 rounded-xl bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30">
            {tasks.filter(t => t.status !== 'Completed').length} Pending
          </span>
          <span className="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30">
            {tasks.filter(t => t.status === 'Completed').length} Completed
          </span>
        </div>
      </div>

      {/* New Task Form */}
      <form onSubmit={handleCreateTask} className="p-5 rounded-2xl bg-dark-card border border-white/10 glass-panel space-y-3">
        <h3 className="text-xs font-bold text-gray-300 uppercase tracking-wider">Quick Task Creation</h3>
        <div className="grid grid-cols-1 md:grid-cols-12 gap-3">
          <input
            type="text"
            required
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            placeholder="What needs to be accomplished today?"
            className="md:col-span-6 bg-dark-bg/80 border border-white/10 rounded-xl px-3.5 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-amber-500"
          />
          <select
            value={newTaskPriority}
            onChange={(e) => setNewTaskPriority(e.target.value)}
            className="md:col-span-2 bg-dark-bg/80 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Urgent">Urgent</option>
          </select>
          <input
            type="date"
            value={newTaskDueDate}
            onChange={(e) => setNewTaskDueDate(e.target.value)}
            className="md:col-span-2 bg-dark-bg/80 border border-white/10 rounded-xl px-3 py-2 text-xs text-white"
          />
          <button
            type="submit"
            className="md:col-span-2 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold transition flex items-center justify-center gap-1 shadow-md shadow-amber-600/30"
          >
            <Plus className="w-4 h-4" />
            Add Task
          </button>
        </div>
      </form>

      {/* Filter Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-gray-400 font-medium">Status:</span>
          {['all', 'todo', 'completed'].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-3 py-1 rounded-lg uppercase text-[10px] font-bold transition ${
                filterStatus === st ? 'bg-amber-600 text-white' : 'bg-dark-card text-gray-400 hover:text-white'
              }`}
            >
              {st}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2">
          <span className="text-gray-400 font-medium">Source:</span>
          {['all', 'research', 'career', 'manual'].map((src) => (
            <button
              key={src}
              onClick={() => setFilterSource(src)}
              className={`px-3 py-1 rounded-lg uppercase text-[10px] font-bold transition ${
                filterSource === src ? 'bg-purple-600 text-white' : 'bg-dark-card text-gray-400 hover:text-white'
              }`}
            >
              {src}
            </button>
          ))}
        </div>
      </div>

      {/* Tasks List */}
      <div className="space-y-2.5">
        {filteredTasks.length > 0 ? (
          filteredTasks.map((task) => {
            const isCompleted = task.status === 'Completed';
            return (
              <div
                key={task.id}
                className={`p-4 rounded-xl border transition flex items-center justify-between gap-4 glass-panel ${
                  isCompleted ? 'bg-dark-card/40 border-white/5 opacity-60' : 'bg-dark-card border-white/10'
                }`}
              >
                <div className="flex items-start gap-3.5 flex-1 min-w-0">
                  <button
                    onClick={() => handleToggleTask(task)}
                    className={`mt-0.5 w-5 h-5 rounded-lg border flex items-center justify-center transition flex-shrink-0 ${
                      isCompleted ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-gray-500 hover:border-amber-400'
                    }`}
                  >
                    {isCompleted && <CheckCircle2 className="w-4 h-4" />}
                  </button>

                  <div className="space-y-1 min-w-0">
                    <p className={`text-xs font-semibold ${isCompleted ? 'line-through text-gray-400' : 'text-white'}`}>
                      {task.title}
                    </p>
                    <div className="flex flex-wrap items-center gap-2 text-[10px]">
                      <span className={`px-2 py-0.5 rounded font-bold ${
                        task.priority === 'Urgent' || task.priority === 'High' ? 'bg-red-500/20 text-red-300' : 'bg-white/5 text-gray-400'
                      }`}>
                        {task.priority} Priority
                      </span>
                      <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 font-bold uppercase">
                        {task.source_module}
                      </span>
                      {task.due_date && (
                        <span className="text-gray-400 flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          Due: {new Date(task.due_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => handleDeleteTask(task.id)}
                  className="text-gray-500 hover:text-red-400 p-1.5 transition"
                  title="Delete Task"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            );
          })
        ) : (
          <div className="text-center py-12 rounded-xl bg-dark-card/40 border border-dashed border-white/10 text-gray-400 text-xs">
            No matching planner tasks. Create tasks or convert them from your research projects.
          </div>
        )}
      </div>

    </div>
  );
}
