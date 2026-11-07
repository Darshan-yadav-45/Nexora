import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  Compass, Clock, AlertTriangle, BookOpen, Code, 
  HelpCircle, Sparkles, Download, Upload, Calendar, Bookmark, 
  ChevronDown, Check, Play, Edit3, X, CheckCircle2
} from 'lucide-react';
import api from '../services/api';

export default function Career() {
  const [searchParams] = useSearchParams();
  const [paths, setPaths] = useState<any[]>([]);
  const [selectedPath, setSelectedPath] = useState<any>(null);
  const [progressData, setProgressData] = useState<any>(null);
  const [, setLoading] = useState(false);

  // Selected Topic & Full Learning Content
  const [selectedTopic, setSelectedTopic] = useState<any>(null);
  const [topicContent, setTopicContent] = useState<any>(null);
  const [, setContentLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'notes' | 'code' | 'quiz' | 'exercises' | 'project' | 'interview'>('notes');
  const [topicNotes, setTopicNotes] = useState('');
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [quizAnswers, setQuizAnswers] = useState<Record<number, number>>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState<number | null>(null);

  // Modals
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showAiModal, setShowAiModal] = useState(false);
  const [showTimetableModal, setShowTimetableModal] = useState(false);
  
  // Custom Roadmap Upload States
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [extractedRoadmap, setExtractedRoadmap] = useState<any>(null);

  // AI Generator Form States
  const [aiGoal, setAiGoal] = useState('');
  const [aiLevel, setAiLevel] = useState('Beginner');
  const [aiSkills] = useState('Python, Git');
  const [aiTech, setAiTech] = useState('FastAPI, React, PostgreSQL');
  const [aiHours, setAiHours] = useState(2);
  const [aiWeeks, setAiWeeks] = useState(16);
  const [aiLoading, setAiLoading] = useState(false);

  // Timetable Form
  const [studyHours, setStudyHours] = useState(2.0);
  const [timetableResult, setTimetableResult] = useState<any>(null);

  useEffect(() => {
    loadPaths();
  }, []);

  const loadPaths = async () => {
    setLoading(true);
    try {
      const res = await api.get('/career/paths');
      setPaths(res.data);
      if (res.data.length > 0) {
        // Check URL param or default
        const pathParam = searchParams.get('path');
        const initial = pathParam ? res.data.find((p: any) => p.slug === pathParam || p.id === pathParam) || res.data[0] : res.data[0];
        selectCareerPath(initial);
      }
    } catch (err) {
      console.error('Error loading career paths:', err);
    } finally {
      setLoading(false);
    }
  };

  const selectCareerPath = async (path: any) => {
    setSelectedPath(path);
    try {
      const progRes = await api.get(`/career/progress/${path.id}`);
      setProgressData(progRes.data);

      // Check if topic was requested via URL
      const topicIdParam = searchParams.get('topic');
      if (topicIdParam) {
        const foundTopic = path.modules?.flatMap((m: any) => m.topics).find((t: any) => t.id === topicIdParam);
        if (foundTopic) {
          openTopicDetails(foundTopic);
          return;
        }
      }

      // Default to recommended or first topic
      if (path.modules?.[0]?.topics?.[0]) {
        openTopicDetails(path.modules[0].topics[0]);
      }
    } catch (err) {
      console.error('Error fetching path progress:', err);
    }
  };

  const openTopicDetails = async (topic: any) => {
    setSelectedTopic(topic);
    setContentLoading(true);
    setQuizSubmitted(false);
    setQuizAnswers({});
    setQuizScore(null);
    try {
      const contentRes = await api.get(`/career/topics/${topic.id}/content`);
      setTopicContent(contentRes.data);

      const noteRes = await api.get(`/career/topics/${topic.id}/note`);
      setTopicNotes(noteRes.data.notes || '');
      setIsBookmarked(noteRes.data.is_bookmarked || false);
    } catch (err) {
      console.error('Error loading topic content:', err);
    } finally {
      setContentLoading(false);
    }
  };

  const handleUpdateTopicStatus = async (statusVal: string, scoreVal?: number) => {
    if (!selectedTopic) return;
    try {
      await api.post(`/career/topics/${selectedTopic.id}/progress`, {
        status: statusVal,
        quiz_score: scoreVal !== undefined ? scoreVal : undefined,
        quiz_answers: quizAnswers,
        project_completed: statusVal === 'Completed'
      });
      // Refresh progress overview
      const progRes = await api.get(`/career/progress/${selectedPath.id}`);
      setProgressData(progRes.data);
    } catch (err) {
      console.error('Error updating topic progress:', err);
    }
  };

  const handleSaveNotes = async () => {
    if (!selectedTopic) return;
    try {
      await api.post(`/career/topics/${selectedTopic.id}/note`, {
        notes: topicNotes,
        is_bookmarked: isBookmarked
      });
    } catch (err) {
      console.error('Error saving note:', err);
    }
  };

  const handleToggleBookmark = async () => {
    const nextState = !isBookmarked;
    setIsBookmarked(nextState);
    if (!selectedTopic) return;
    try {
      await api.post(`/career/topics/${selectedTopic.id}/note`, {
        notes: topicNotes,
        is_bookmarked: nextState
      });
    } catch (err) {
      console.error('Error updating bookmark:', err);
    }
  };

  const handleQuizSubmit = () => {
    if (!topicContent?.mcqs) return;
    let correct = 0;
    topicContent.mcqs.forEach((mcq: any) => {
      if (quizAnswers[mcq.id] === mcq.correct_option) {
        correct++;
      }
    });
    const percentage = Math.round((correct / topicContent.mcqs.length) * 100);
    setQuizScore(percentage);
    setQuizSubmitted(true);

    // Save to backend
    const topicStatus = percentage >= 75 ? 'Completed' : 'Needs Revision';
    handleUpdateTopicStatus(topicStatus, percentage);
  };

  const handleUploadRoadmap = async () => {
    if (!uploadFile) return;
    setUploadLoading(true);
    const formData = new FormData();
    formData.append('file', uploadFile);

    try {
      const res = await api.post('/career/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setExtractedRoadmap(res.data);
    } catch (err) {
      console.error('Error uploading roadmap:', err);
      alert('Failed to extract roadmap. Please ensure file is valid.');
    } finally {
      setUploadLoading(false);
    }
  };

  const handleConfirmCustomRoadmap = async () => {
    if (!extractedRoadmap) return;
    try {
      await api.post('/career/confirm', {
        custom_roadmap_id: extractedRoadmap.custom_roadmap_id,
        title: extractedRoadmap.title,
        modules: extractedRoadmap.modules
      });
      alert('Custom roadmap confirmed and enrolled!');
      setShowUploadModal(false);
      setExtractedRoadmap(null);
      await loadPaths();
    } catch (err) {
      console.error('Error confirming custom roadmap:', err);
    }
  };

  const handleGenerateAiRoadmap = async () => {
    setAiLoading(true);
    try {
      const res = await api.post('/career/generate-ai', {
        career_goal: aiGoal,
        current_knowledge_level: aiLevel,
        existing_skills: aiSkills.split(',').map(s => s.trim()),
        preferred_technologies: aiTech.split(',').map(s => s.trim()),
        daily_study_hours: aiHours,
        target_completion_weeks: aiWeeks
      });
      setExtractedRoadmap({
        custom_roadmap_id: res.data.custom_roadmap_id,
        title: res.data.roadmap.title,
        modules: res.data.roadmap.modules,
        missing_or_unclear_topics: []
      });
      setShowAiModal(false);
      setShowUploadModal(true); // Open review modal to confirm
    } catch (err) {
      console.error('Error generating AI roadmap:', err);
    } finally {
      setAiLoading(false);
    }
  };

  const handleGenerateTimetable = async () => {
    if (!selectedPath) return;
    try {
      const res = await api.post('/career/timetable/generate', {
        career_path_id: selectedPath.id,
        daily_study_hours: studyHours,
        days_per_week: 5
      });
      setTimetableResult(res.data);
    } catch (err) {
      console.error('Error generating timetable:', err);
    }
  };

  const downloadReport = async () => {
    if (!selectedPath) return;
    window.open(`${api.defaults.baseURL}/career/report/${selectedPath.id}?format=markdown`, '_blank');
  };

  return (
    <div className="w-full max-w-7xl mx-auto space-y-6 pb-20">
      
      {/* Top Header & Track Selector */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 p-6 rounded-2xl bg-dark-card border border-white/10 glass-panel">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-500/10 text-primary-400 text-xs font-semibold mb-2">
            <Compass className="w-3.5 h-3.5" />
            Complete Career Roadmap System
          </div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-white">
            {selectedPath?.title || 'Career Paths'}
          </h1>
          <p className="text-xs md:text-sm text-gray-400 mt-1 max-w-2xl">
            {selectedPath?.description || 'Select a full stack or data career path.'}
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={() => setShowTimetableModal(true)}
            className="px-3.5 py-2 rounded-xl bg-dark-bg/80 hover:bg-white/10 text-gray-200 border border-white/10 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Calendar className="w-3.5 h-3.5 text-primary-400" />
            Timetable
          </button>
          <button
            onClick={() => setShowUploadModal(true)}
            className="px-3.5 py-2 rounded-xl bg-dark-bg/80 hover:bg-white/10 text-gray-200 border border-white/10 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Upload className="w-3.5 h-3.5 text-purple-400" />
            Upload My Roadmap
          </button>
          <button
            onClick={() => setShowAiModal(true)}
            className="px-3.5 py-2 rounded-xl bg-purple-600/30 hover:bg-purple-600/50 text-purple-200 border border-purple-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
          >
            <Sparkles className="w-3.5 h-3.5 text-purple-300" />
            AI Generator
          </button>
          <button
            onClick={downloadReport}
            className="px-3.5 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white text-xs font-semibold flex items-center gap-1.5 shadow-md shadow-primary-600/30 transition"
          >
            <Download className="w-3.5 h-3.5" />
            Report
          </button>
        </div>
      </div>

      {/* Path Selector Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
        {paths.map((p) => {
          const isSelected = selectedPath?.id === p.id;
          return (
            <button
              key={p.id}
              onClick={() => selectCareerPath(p)}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold whitespace-nowrap transition-all flex items-center gap-2 border ${
                isSelected
                  ? 'bg-primary-600 text-white border-primary-500 shadow-lg shadow-primary-600/30'
                  : 'bg-dark-card/60 text-gray-300 border-white/5 hover:border-white/20'
              }`}
            >
              <span>{p.title}</span>
              {p.is_custom && <span className="px-1.5 py-0.5 rounded bg-purple-500/30 text-[10px] text-purple-200">Custom</span>}
            </button>
          );
        })}
      </div>

      {/* Progress Bar & Summary Pill */}
      {progressData && (
        <div className="p-4 rounded-xl bg-dark-card border border-white/10 glass-panel flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-4 w-full md:w-auto">
            <div className="w-12 h-12 rounded-xl bg-primary-500/10 border border-primary-500/20 text-primary-400 flex items-center justify-center font-bold text-sm">
              {progressData.completion_percentage}%
            </div>
            <div>
              <div className="text-xs font-bold text-white">Track Progress: {progressData.completed_topics} / {progressData.total_topics} Topics Completed</div>
              <div className="text-[11px] text-gray-400">
                {progressData.weak_topics.length > 0 
                  ? `${progressData.weak_topics.length} topics flagged for revision` 
                  : 'All assessments passing on target'}
              </div>
            </div>
          </div>

          <div className="w-full md:w-1/2 h-2.5 bg-dark-bg rounded-full overflow-hidden border border-white/5">
            <div 
              className="h-full bg-gradient-to-r from-primary-500 to-purple-500 transition-all duration-500" 
              style={{ width: `${progressData.completion_percentage}%` }}
            />
          </div>
        </div>
      )}

      {/* Main Learning Workspace: Sidebar Navigation + Detailed Topic Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Column: Curriculum Modules & Topics (4 Cols) */}
        <div className="lg:col-span-4 space-y-4 max-h-[85vh] overflow-y-auto pr-1">
          {selectedPath?.modules?.map((mod: any, mIdx: number) => (
            <div key={mod.id} className="rounded-xl bg-dark-card border border-white/10 overflow-hidden glass-panel">
              <div className="p-3.5 bg-white/5 border-b border-white/5 flex items-center justify-between">
                <div>
                  <span className="text-[10px] font-bold text-primary-400 uppercase tracking-wider">Module {mIdx + 1}</span>
                  <h3 className="text-xs font-bold text-white">{mod.title}</h3>
                </div>
                <span className="text-[10px] px-2 py-0.5 rounded bg-white/10 text-gray-300 font-medium">
                  {mod.difficulty_level}
                </span>
              </div>

              <div className="p-2 space-y-1">
                {mod.topics?.map((top: any) => {
                  const isSelected = selectedTopic?.id === top.id;
                  const topicStat = progressData?.topics?.find((t: any) => t.topic_id === top.id);
                  const status = topicStat?.status || 'Not Started';

                  return (
                    <button
                      key={top.id}
                      onClick={() => openTopicDetails(top)}
                      className={`w-full text-left p-2.5 rounded-lg text-xs transition flex items-center justify-between gap-2 ${
                        isSelected 
                          ? 'bg-primary-600/30 border border-primary-500/50 text-white font-bold' 
                          : 'hover:bg-white/5 text-gray-300'
                      }`}
                    >
                      <div className="flex items-center gap-2 truncate">
                        <span className={`w-2 h-2 rounded-full ${
                          status === 'Completed' ? 'bg-emerald-400' : (status === 'In Progress' ? 'bg-primary-400' : (status === 'Needs Revision' ? 'bg-amber-400' : 'bg-gray-600'))
                        }`} />
                        <span className="truncate">{top.title}</span>
                      </div>

                      <div className="flex items-center gap-1.5 flex-shrink-0">
                        {topicStat?.quiz_score > 0 && (
                          <span className="text-[10px] px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300">
                            {topicStat.quiz_score}%
                          </span>
                        )}
                        {topicStat?.is_bookmarked && (
                          <Bookmark className="w-3 h-3 text-amber-400 fill-amber-400" />
                        )}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Right Column: Complete Topic Deep Learning Viewer (8 Cols) */}
        <div className="lg:col-span-8 bg-dark-card border border-white/10 rounded-2xl p-6 glass-panel space-y-6">
          {selectedTopic ? (
            <>
              {/* Topic Header with Status, Bookmark & Estimated Time */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-white/10">
                <div className="space-y-1">
                  <div className="flex items-center gap-2 text-xs">
                    <span className="px-2 py-0.5 rounded bg-primary-500/20 text-primary-300 font-bold uppercase">{selectedTopic.level}</span>
                    <span className="text-gray-400 flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" />
                      {topicContent?.estimated_learning_time_minutes || selectedTopic.estimated_minutes} Mins
                    </span>
                  </div>
                  <h2 className="text-xl md:text-2xl font-bold text-white">{selectedTopic.title}</h2>
                </div>

                {/* Progress State Changer & Bookmark */}
                <div className="flex items-center gap-2">
                  <button
                    onClick={handleToggleBookmark}
                    className={`p-2 rounded-xl border transition ${
                      isBookmarked ? 'bg-amber-500/20 text-amber-400 border-amber-500/40' : 'bg-white/5 text-gray-400 border-white/10 hover:text-white'
                    }`}
                    title="Bookmark topic"
                  >
                    <Bookmark className={`w-4 h-4 ${isBookmarked ? 'fill-amber-400' : ''}`} />
                  </button>

                  <select
                    value={progressData?.topics?.find((t: any) => t.topic_id === selectedTopic.id)?.status || 'Not Started'}
                    onChange={(e) => handleUpdateTopicStatus(e.target.value)}
                    className="bg-dark-bg border border-white/10 rounded-xl px-3 py-1.5 text-xs font-semibold text-gray-200 focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="Not Started">Not Started</option>
                    <option value="In Progress">In Progress</option>
                    <option value="Completed">Completed</option>
                    <option value="Needs Revision">Needs Revision</option>
                  </select>
                </div>
              </div>

              {/* Subtopics Breadcrumb */}
              {selectedTopic.subtopics && selectedTopic.subtopics.length > 0 && (
                <div className="flex flex-wrap gap-1.5 text-xs">
                  <span className="text-gray-500 font-medium self-center mr-1">Subtopics:</span>
                  {selectedTopic.subtopics.map((sub: any) => (
                    <span key={sub.id} className="px-2.5 py-1 rounded-md bg-white/5 text-gray-300 border border-white/5">
                      {sub.title}
                    </span>
                  ))}
                </div>
              )}

              {/* Learning Content Navigation Tabs */}
              <div className="flex items-center gap-1 border-b border-white/10 overflow-x-auto pb-1 scrollbar-none text-xs font-semibold">
                {[
                  { id: 'notes', label: '1. Technical Notes', icon: BookOpen },
                  { id: 'code', label: '2. Code & Architecture', icon: Code },
                  { id: 'quiz', label: '3. Interactive Quiz', icon: HelpCircle },
                  { id: 'exercises', label: '4. Coding Task', icon: Play },
                  { id: 'project', label: '5. Mini-Project', icon: Compass },
                  { id: 'interview', label: '6. Interview Q&A', icon: CheckCircle2 }
                ].map((tab) => {
                  const Icon = tab.icon;
                  const isActive = activeTab === tab.id;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={`flex items-center gap-1.5 px-3 py-2 rounded-lg whitespace-nowrap transition ${
                        isActive 
                          ? 'bg-primary-600 text-white font-bold' 
                          : 'text-gray-400 hover:text-white hover:bg-white/5'
                      }`}
                    >
                      <Icon className="w-3.5 h-3.5" />
                      {tab.label}
                    </button>
                  );
                })}
              </div>

              {/* Tab 1: Technical Notes & Theory */}
              {activeTab === 'notes' && topicContent && (
                <div className="space-y-6 text-sm text-gray-300">
                  {/* Learning Objectives */}
                  <div className="p-4 rounded-xl bg-primary-950/30 border border-primary-500/20 space-y-2">
                    <h4 className="text-xs font-bold text-primary-400 uppercase tracking-wider">Learning Objectives</h4>
                    <ul className="list-disc list-inside space-y-1 text-xs text-gray-200">
                      {topicContent.learning_objectives?.map((obj: string, i: number) => (
                        <li key={i}>{obj}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Beginner-Friendly Explanation */}
                  <div className="space-y-2">
                    <h3 className="text-base font-bold text-white flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-primary-400" />
                      Intuitive Breakdown
                    </h3>
                    <p className="leading-relaxed text-gray-300 text-xs sm:text-sm bg-dark-bg/40 p-4 rounded-xl border border-white/5">
                      {topicContent.beginner_explanation}
                    </p>
                  </div>

                  {/* Detailed Technical Notes */}
                  <div className="space-y-2">
                    <h3 className="text-base font-bold text-white">Detailed Technical Architecture</h3>
                    <div className="prose prose-invert max-w-none text-xs sm:text-sm leading-relaxed whitespace-pre-wrap bg-dark-bg/60 p-4 rounded-xl border border-white/5 font-mono text-gray-300">
                      {topicContent.detailed_technical_notes}
                    </div>
                  </div>

                  {/* Definitions & Concepts */}
                  {topicContent.important_definitions && topicContent.important_definitions.length > 0 && (
                    <div className="space-y-3">
                      <h3 className="text-base font-bold text-white">Important Definitions & Core Concepts</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {topicContent.important_definitions.map((def: any, i: number) => (
                          <div key={i} className="p-3.5 rounded-xl bg-dark-bg/50 border border-white/5 space-y-1">
                            <span className="text-xs font-bold text-primary-300">{def.term}</span>
                            <p className="text-xs text-gray-300">{def.definition}</p>
                            <span className="text-[10px] text-gray-400 italic block pt-1">Principle: {def.key_concept}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Revision Notes & Key Takeaways */}
                  <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-500/20 space-y-3">
                    <h4 className="text-xs font-bold text-purple-400 uppercase tracking-wider">Key Takeaways & Revision Notes</h4>
                    <p className="text-xs text-gray-300 whitespace-pre-wrap">{topicContent.revision_notes}</p>
                    <div className="flex flex-wrap gap-2 pt-2">
                      {topicContent.key_takeaways?.map((takeaway: string, idx: number) => (
                        <span key={idx} className="px-2.5 py-1 rounded bg-purple-500/10 text-[11px] text-purple-200 border border-purple-500/20">
                          ✓ {takeaway}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Tab 2: Code & Architecture */}
              {activeTab === 'code' && topicContent && (
                <div className="space-y-6 text-sm">
                  {/* Practical Coding Example */}
                  {topicContent.practical_coding_examples?.map((ex: any, idx: number) => (
                    <div key={idx} className="space-y-2">
                      <div className="flex items-center justify-between">
                        <h4 className="text-sm font-bold text-white">{ex.title}</h4>
                        <span className="text-xs text-primary-400 font-mono uppercase">{ex.language}</span>
                      </div>
                      <div className="rounded-xl overflow-hidden border border-white/10 bg-dark-bg">
                        <div className="bg-white/5 px-4 py-1.5 text-xs text-gray-400 font-mono flex items-center justify-between">
                          <span>Production Implementation</span>
                          <button 
                            onClick={() => navigator.clipboard.writeText(ex.code)}
                            className="text-[10px] text-primary-400 hover:text-primary-300 font-sans"
                          >
                            Copy Code
                          </button>
                        </div>
                        <pre className="p-4 text-xs font-mono text-gray-200 overflow-x-auto leading-relaxed whitespace-pre-wrap">
                          {ex.code}
                        </pre>
                      </div>
                      {ex.output && (
                        <div className="p-3 rounded-lg bg-emerald-950/30 border border-emerald-500/20 text-xs text-emerald-300 font-mono">
                          <span className="font-bold text-emerald-400 block mb-1">Expected Output:</span>
                          {ex.output}
                        </div>
                      )}
                      <p className="text-xs text-gray-400">{ex.explanation}</p>
                    </div>
                  ))}

                  {/* Common Mistakes */}
                  {topicContent.common_mistakes && topicContent.common_mistakes.length > 0 && (
                    <div className="space-y-3 pt-4 border-t border-white/10">
                      <h4 className="text-sm font-bold text-amber-400 flex items-center gap-2">
                        <AlertTriangle className="w-4 h-4" />
                        Common Mistakes & How to Avoid Them
                      </h4>
                      <div className="space-y-3">
                        {topicContent.common_mistakes.map((m: any, idx: number) => (
                          <div key={idx} className="p-4 rounded-xl bg-amber-500/5 border border-amber-500/20 space-y-2">
                            <span className="text-xs font-bold text-red-400 block">❌ Pitfall: {m.mistake}</span>
                            <p className="text-xs text-gray-300"><strong className="text-gray-200">Why it's wrong:</strong> {m.why_wrong}</p>
                            <p className="text-xs text-emerald-400"><strong className="text-emerald-300">How to fix:</strong> {m.how_to_fix}</p>
                            {m.corrected_code && (
                              <pre className="p-2.5 rounded bg-dark-bg text-xs font-mono text-gray-300 overflow-x-auto">
                                {m.corrected_code}
                              </pre>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Real World Applications */}
                  {topicContent.real_world_applications && (
                    <div className="space-y-3 pt-4 border-t border-white/10">
                      <h4 className="text-sm font-bold text-white">Real-World Industrial Applications</h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        {topicContent.real_world_applications.map((app: any, idx: number) => (
                          <div key={idx} className="p-3.5 rounded-xl bg-dark-bg/60 border border-white/5 space-y-1">
                            <span className="text-xs font-bold text-primary-300">{app.domain}</span>
                            <h5 className="text-xs font-semibold text-white">{app.use_case}</h5>
                            <p className="text-[11px] text-gray-400">{app.real_example}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Tab 3: Interactive Quiz & Assessment */}
              {activeTab === 'quiz' && topicContent && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-base font-bold text-white">Topic Assessment MCQs</h3>
                      <p className="text-xs text-gray-400">Test your mastery with instant scoring and explanations</p>
                    </div>
                    {quizScore !== null && (
                      <span className={`px-3 py-1.5 rounded-xl text-xs font-bold border ${
                        quizScore >= 75 ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                      }`}>
                        Score: {quizScore}% {quizScore >= 75 ? '(Passed)' : '(Needs Revision)'}
                      </span>
                    )}
                  </div>

                  <div className="space-y-4">
                    {topicContent.mcqs?.map((mcq: any, idx: number) => {
                      const selectedOpt = quizAnswers[mcq.id];
                      const isCorrect = selectedOpt === mcq.correct_option;

                      return (
                        <div key={mcq.id} className="p-4 rounded-xl bg-dark-bg/50 border border-white/5 space-y-3">
                          <p className="text-xs font-bold text-white">
                            {idx + 1}. {mcq.question}
                          </p>

                          <div className="space-y-2">
                            {mcq.options.map((opt: string, optIdx: number) => {
                              const isChecked = selectedOpt === optIdx;
                              let btnClass = "border-white/10 bg-dark-card/60 text-gray-300 hover:border-white/20";

                              if (quizSubmitted) {
                                if (optIdx === mcq.correct_option) {
                                  btnClass = "border-emerald-500 bg-emerald-500/20 text-emerald-200 font-bold";
                                } else if (isChecked && !isCorrect) {
                                  btnClass = "border-red-500 bg-red-500/20 text-red-200";
                                }
                              } else if (isChecked) {
                                btnClass = "border-primary-500 bg-primary-500/20 text-white font-bold";
                              }

                              return (
                                <button
                                  key={optIdx}
                                  disabled={quizSubmitted}
                                  onClick={() => setQuizAnswers({ ...quizAnswers, [mcq.id]: optIdx })}
                                  className={`w-full p-2.5 rounded-lg text-left text-xs border transition flex items-center justify-between ${btnClass}`}
                                >
                                  <span>{opt}</span>
                                  {quizSubmitted && optIdx === mcq.correct_option && (
                                    <Check className="w-4 h-4 text-emerald-400" />
                                  )}
                                </button>
                              );
                            })}
                          </div>

                          {quizSubmitted && (
                            <div className="p-3 rounded-lg bg-white/5 text-[11px] text-gray-300 border border-white/5">
                              <strong className="text-primary-400">Explanation: </strong>
                              {mcq.explanation}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>

                  <div className="flex items-center gap-3">
                    {!quizSubmitted ? (
                      <button
                        onClick={handleQuizSubmit}
                        disabled={Object.keys(quizAnswers).length < (topicContent.mcqs?.length || 0)}
                        className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 disabled:opacity-50 text-white text-xs font-bold transition shadow-lg shadow-primary-600/30"
                      >
                        Submit Answers
                      </button>
                    ) : (
                      <button
                        onClick={() => {
                          setQuizSubmitted(false);
                          setQuizAnswers({});
                          setQuizScore(null);
                        }}
                        className="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-medium transition"
                      >
                        Retake Assessment
                      </button>
                    )}
                  </div>
                </div>
              )}

              {/* Tab 4: Coding Tasks & Practical Exercises */}
              {activeTab === 'exercises' && topicContent && (
                <div className="space-y-6">
                  {topicContent.coding_exercises?.map((ex: any) => (
                    <div key={ex.id} className="space-y-4 p-5 rounded-xl bg-dark-bg/60 border border-white/10">
                      <div>
                        <h4 className="text-sm font-bold text-white">{ex.title}</h4>
                        <p className="text-xs text-gray-400 mt-1">{ex.description}</p>
                      </div>

                      <div className="rounded-xl overflow-hidden border border-white/10 bg-dark-bg">
                        <div className="bg-white/5 px-4 py-1.5 text-xs text-gray-400 font-mono">
                          Starter Code
                        </div>
                        <pre className="p-4 text-xs font-mono text-gray-300 overflow-x-auto whitespace-pre-wrap">
                          {ex.starter_code}
                        </pre>
                      </div>

                      {/* Solution Accordion */}
                      <details className="group rounded-xl border border-white/10 bg-dark-card p-3">
                        <summary className="cursor-pointer text-xs font-bold text-primary-400 flex items-center justify-between">
                          <span>View Reference Solution & Logic</span>
                          <ChevronDown className="w-4 h-4 group-open:rotate-180 transition" />
                        </summary>
                        <pre className="mt-3 p-3 rounded-lg bg-dark-bg text-xs font-mono text-emerald-300 overflow-x-auto whitespace-pre-wrap">
                          {ex.solution_code}
                        </pre>
                      </details>
                    </div>
                  ))}
                </div>
              )}

              {/* Tab 5: Mini-Projects */}
              {activeTab === 'project' && topicContent && (
                <div className="space-y-6">
                  {topicContent.mini_projects?.map((proj: any, idx: number) => (
                    <div key={idx} className="p-5 rounded-xl bg-dark-bg/60 border border-white/10 space-y-4">
                      <div className="flex items-center justify-between">
                        <h4 className="text-sm font-bold text-white">{proj.title}</h4>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-primary-500/20 text-primary-300 font-bold uppercase">Capstone Assignment</span>
                      </div>
                      <p className="text-xs text-gray-300">{proj.description}</p>

                      <div className="space-y-2">
                        <span className="text-xs font-bold text-gray-200">Requirements & Deliverables:</span>
                        <ul className="list-disc list-inside space-y-1 text-xs text-gray-400">
                          {proj.requirements?.map((req: string, rIdx: number) => (
                            <li key={rIdx}>{req}</li>
                          ))}
                        </ul>
                      </div>

                      <div className="p-3 rounded-lg bg-white/5 text-xs text-gray-300">
                        <strong className="text-primary-400">Deliverable Spec: </strong>
                        {proj.deliverables}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Tab 6: Interview Questions & Answers */}
              {activeTab === 'interview' && topicContent && (
                <div className="space-y-4">
                  {topicContent.interview_questions?.map((iq: any, idx: number) => (
                    <div key={idx} className="p-4 rounded-xl bg-dark-bg/50 border border-white/5 space-y-2">
                      <div className="flex items-center justify-between">
                        <h4 className="text-xs font-bold text-white">Q{idx + 1}: {iq.question}</h4>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-white/10 text-gray-300">{iq.difficulty}</span>
                      </div>
                      <p className="text-xs text-gray-300 leading-relaxed"><strong className="text-emerald-400">Answer:</strong> {iq.answer}</p>
                      <span className="text-[10px] text-amber-300 block italic">💡 Interview Tip: {iq.tip}</span>
                    </div>
                  ))}
                </div>
              )}

              {/* Personal Topic Notes & Action Bar */}
              <div className="pt-6 border-t border-white/10 space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-gray-300 flex items-center gap-1.5">
                    <Edit3 className="w-3.5 h-3.5 text-primary-400" />
                    Personal Topic Notes
                  </h4>
                  <button
                    onClick={handleSaveNotes}
                    className="text-xs text-primary-400 hover:text-primary-300 font-semibold"
                  >
                    Save Notes
                  </button>
                </div>
                <textarea
                  value={topicNotes}
                  onChange={(e) => setTopicNotes(e.target.value)}
                  placeholder="Record your personal observations, edge cases, or code snippets for this topic..."
                  rows={3}
                  className="w-full p-3 rounded-xl bg-dark-bg/70 border border-white/10 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </>
          ) : (
            <div className="text-center py-20 text-gray-500">
              Select any topic from the curriculum sidebar to load its complete notes, code examples, interactive quizzes, and projects.
            </div>
          )}
        </div>

      </div>

      {/* Upload My Roadmap Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="relative w-full max-w-2xl bg-dark-card border border-white/10 rounded-2xl p-6 shadow-2xl glass-panel max-h-[90vh] overflow-y-auto space-y-6">
            <div className="flex items-center justify-between pb-3 border-b border-white/10">
              <div className="flex items-center gap-2">
                <Upload className="w-5 h-5 text-purple-400" />
                <h3 className="text-lg font-bold text-white">Upload & Review My Roadmap</h3>
              </div>
              <button onClick={() => setShowUploadModal(false)} className="text-gray-400 hover:text-white p-1">
                <X className="w-5 h-5" />
              </button>
            </div>

            {!extractedRoadmap ? (
              <div className="space-y-4">
                <p className="text-xs text-gray-400">
                  Upload your syllabus or study guide in PDF, DOCX, TXT, or Image format. 
                  Nexora AI will extract the structure, verify missing engineering prerequisites, and generate interactive topic notes.
                </p>

                <div className="border-2 border-dashed border-white/15 rounded-xl p-8 text-center space-y-3 bg-dark-bg/40">
                  <Upload className="w-8 h-8 text-gray-400 mx-auto" />
                  <div>
                    <label className="cursor-pointer text-xs font-bold text-primary-400 hover:text-primary-300">
                      Choose document file
                      <input
                        type="file"
                        className="hidden"
                        accept=".pdf,.docx,.doc,.txt,.png,.jpg,.jpeg"
                        onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                      />
                    </label>
                    <p className="text-[11px] text-gray-500 mt-1">Supports PDF, DOCX, TXT, PNG, JPG</p>
                  </div>
                  {uploadFile && (
                    <span className="text-xs text-emerald-400 font-mono block">
                      Selected: {uploadFile.name} ({(uploadFile.size / 1024).toFixed(1)} KB)
                    </span>
                  )}
                </div>

                <button
                  onClick={handleUploadRoadmap}
                  disabled={!uploadFile || uploadLoading}
                  className="w-full py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white text-xs font-bold transition flex items-center justify-center gap-2 shadow-lg shadow-purple-600/30"
                >
                  {uploadLoading ? 'Extracting Structure with AI...' : 'Extract & Review Roadmap'}
                </button>
              </div>
            ) : (
              <div className="space-y-6">
                <div>
                  <span className="text-[10px] uppercase font-bold text-purple-400">Extracted Preview</span>
                  <h4 className="text-base font-bold text-white">{extractedRoadmap.title}</h4>
                </div>

                {/* Missing Topics Flags */}
                {extractedRoadmap.missing_or_unclear_topics && extractedRoadmap.missing_or_unclear_topics.length > 0 && (
                  <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-1.5">
                    <span className="text-xs font-bold text-amber-300 flex items-center gap-1.5">
                      <AlertTriangle className="w-3.5 h-3.5" />
                      Recommended Additional Engineering Topics:
                    </span>
                    <ul className="text-xs text-amber-200 list-disc list-inside space-y-0.5">
                      {extractedRoadmap.missing_or_unclear_topics.map((t: any, idx: number) => (
                        <li key={idx}><strong>{t.suggested_topic}</strong>: {t.reason}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Modules Preview Table */}
                <div className="space-y-3">
                  <span className="text-xs font-bold text-gray-300">Extracted Curriculum ({extractedRoadmap.modules?.length} Modules):</span>
                  <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
                    {extractedRoadmap.modules?.map((m: any, idx: number) => (
                      <div key={idx} className="p-3 rounded-lg bg-dark-bg/60 border border-white/5 space-y-1">
                        <span className="text-xs font-bold text-white">{m.title}</span>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {m.topics?.map((top: any, tIdx: number) => (
                            <span key={tIdx} className="text-[10px] px-2 py-0.5 rounded bg-white/5 text-gray-300">
                              {top.title}
                            </span>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="flex items-center gap-3 pt-3 border-t border-white/10">
                  <button
                    onClick={handleConfirmCustomRoadmap}
                    className="flex-1 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition shadow-lg shadow-emerald-600/30"
                  >
                    Confirm & Save to My Roadmaps
                  </button>
                  <button
                    onClick={() => setExtractedRoadmap(null)}
                    className="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white text-xs font-medium transition"
                  >
                    Upload Different File
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* AI Roadmap Generator Modal */}
      {showAiModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="relative w-full max-w-lg bg-dark-card border border-white/10 rounded-2xl p-6 shadow-2xl glass-panel space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-white/10">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary-400" />
                <h3 className="text-lg font-bold text-white">Generate Personalized AI Roadmap</h3>
              </div>
              <button onClick={() => setShowAiModal(false)} className="text-gray-400 hover:text-white p-1">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3.5 text-xs">
              <div>
                <label className="block font-semibold text-gray-300 mb-1">Target Career Goal / Role</label>
                <input
                  type="text"
                  value={aiGoal}
                  onChange={(e) => setAiGoal(e.target.value)}
                  placeholder="e.g. Distributed Cloud Systems Architect"
                  className="w-full bg-dark-bg/70 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-gray-300 mb-1">Current Level</label>
                  <select
                    value={aiLevel}
                    onChange={(e) => setAiLevel(e.target.value)}
                    className="w-full bg-dark-bg/70 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-gray-300 mb-1">Daily Study Hours</label>
                  <input
                    type="number"
                    value={aiHours}
                    onChange={(e) => setAiHours(Number(e.target.value))}
                    className="w-full bg-dark-bg/70 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-gray-300 mb-1">Preferred Technologies</label>
                <input
                  type="text"
                  value={aiTech}
                  onChange={(e) => setAiTech(e.target.value)}
                  placeholder="e.g. Python, FastAPI, Docker, PostgreSQL"
                  className="w-full bg-dark-bg/70 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label className="block font-semibold text-gray-300 mb-1">Target Duration (Weeks)</label>
                <input
                  type="number"
                  value={aiWeeks}
                  onChange={(e) => setAiWeeks(Number(e.target.value))}
                  className="w-full bg-dark-bg/70 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>

            <button
              onClick={handleGenerateAiRoadmap}
              disabled={!aiGoal || aiLoading}
              className="w-full py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 disabled:opacity-50 text-white text-xs font-bold transition shadow-lg shadow-primary-600/30 flex items-center justify-center gap-2"
            >
              {aiLoading ? 'Synthesizing Curriculum...' : 'Generate AI Roadmap'}
            </button>
          </div>
        </div>
      )}

      {/* Timetable Modal */}
      {showTimetableModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
          <div className="relative w-full max-w-xl bg-dark-card border border-white/10 rounded-2xl p-6 shadow-2xl glass-panel space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-white/10">
              <div className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-primary-400" />
                <h3 className="text-lg font-bold text-white">Study Timetable Generator</h3>
              </div>
              <button onClick={() => setShowTimetableModal(false)} className="text-gray-400 hover:text-white p-1">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block font-semibold text-gray-300 mb-1">Available Daily Study Hours</label>
                <input
                  type="number"
                  step="0.5"
                  value={studyHours}
                  onChange={(e) => setStudyHours(Number(e.target.value))}
                  className="w-full bg-dark-bg/70 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>
              <button
                onClick={handleGenerateTimetable}
                className="w-full py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white text-xs font-bold transition shadow-lg shadow-primary-600/30"
              >
                Calculate Study Schedule
              </button>

              {timetableResult && (
                <div className="space-y-2 pt-3">
                  <span className="font-bold text-gray-200">Generated Schedule ({timetableResult.total_days_scheduled} Study Days):</span>
                  <div className="space-y-1.5 max-h-56 overflow-y-auto pr-1">
                    {timetableResult.schedule?.map((item: any, idx: number) => (
                      <div key={idx} className="p-2 rounded-lg bg-dark-bg/60 border border-white/5 flex items-center justify-between">
                        <div>
                          <span className="text-[10px] font-bold text-primary-400">{item.date} ({item.day_name})</span>
                          <p className="text-xs text-white">{item.topic_title}</p>
                        </div>
                        <span className="text-[10px] text-gray-400">{item.estimated_minutes}m</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
