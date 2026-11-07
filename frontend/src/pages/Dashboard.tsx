import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Compass, Microscope, CheckSquare, BookMarked,
  Sparkles, CheckCircle2, Plus,
  ChevronRight, BookOpen, GraduationCap, Briefcase,
  FileText
} from 'lucide-react';
import api from '../services/api';

export default function Dashboard() {
  const [userStatus, setUserStatus] = useState<any>({ account_type: 'student', profile_completed: true });
  const [activePathProgress, setActivePathProgress] = useState<any>(null);
  const [activePath, setActivePath] = useState<any>(null);
  const [notebooks, setNotebooks] = useState<any[]>([]);
  const [plannerTasks, setPlannerTasks] = useState<any[]>([]);
  const [kbItems, setKbItems] = useState<any[]>([]);
  const [profile, setProfile] = useState<any>(null);
  const [educationRecords, setEducationRecords] = useState<any[]>([]);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [teacherProfile, setTeacherProfile] = useState<any>(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // 1. Fetch user status & account type
      try {
        const statRes = await api.get('/auth/status');
        setUserStatus(statRes.data);
      } catch (err) {}

      // 2. Fetch profile
      try {
        const profRes = await api.get('/profile/');
        setProfile(profRes.data);
      } catch (err) {}

      // 3. Fetch career paths & progress
      try {
        const pathsRes = await api.get('/career/paths');
        const allPaths = pathsRes.data;
        if (allPaths.length > 0) {
          const currentPath = allPaths[0];
          setActivePath(currentPath);
          try {
            const progRes = await api.get(`/career/progress/${currentPath.id}`);
            setActivePathProgress(progRes.data);
          } catch (err) {}
        }
      } catch (err) {}

      // 4. Fetch Research Notebooks
      try {
        const nbRes = await api.get('/notebooks');
        setNotebooks(nbRes.data);
      } catch (err) {}

      // 5. Fetch Education Records & Subjects (for students)
      try {
        const edRes = await api.get('/education/records');
        setEducationRecords(edRes.data);
      } catch (err) {}

      try {
        const subRes = await api.get('/education/subjects');
        setSubjects(subRes.data);
      } catch (err) {}

      // 6. Fetch Teacher Profile (for teachers)
      try {
        const teachRes = await api.get('/teacher/profile');
        setTeacherProfile(teachRes.data);
      } catch (err) {}

      // 7. Fetch planner tasks & knowledge base items
      try {
        const taskRes = await api.get('/integration/planner/tasks');
        setPlannerTasks(taskRes.data);
      } catch (err) {}

      try {
        const kbRes = await api.get('/integration/knowledge-base/items');
        setKbItems(kbRes.data);
      } catch (err) {}

    } catch (err) {
      console.error('Error loading dashboard data:', err);
    }
  };

  const currentEducationRecord = educationRecords.find(r => r.status === 'Currently studying') || educationRecords[educationRecords.length - 1];

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-in fade-in duration-300">
      
      {/* Top Welcome Header */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 flex flex-col sm:flex-row justify-between sm:items-center gap-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20 capitalize flex items-center gap-1.5">
              {userStatus.account_type === 'teacher' ? <BookOpen className="w-3.5 h-3.5" /> :
               userStatus.account_type === 'professional' ? <Briefcase className="w-3.5 h-3.5" /> :
               <GraduationCap className="w-3.5 h-3.5" />}
              {userStatus.account_type} Workspace
            </span>
            <span className="text-xs text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> PostgreSQL Connected
            </span>
          </div>

          <h1 className="text-3xl font-extrabold text-white">
            Welcome back, {profile?.preferred_name || profile?.name || 'Scholar'}
          </h1>
          <p className="text-gray-400 text-sm mt-1">
            {userStatus.account_type === 'teacher'
              ? 'Prepare course lecture notes, generate diagnostic exam questions, and manage academic literature.'
              : userStatus.account_type === 'professional'
              ? 'Advance your career roadmap, manage research notebooks, and track engineering tasks.'
              : 'Track your semester subjects, master career roadmaps, and grounded research papers.'}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/research"
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-primary-500/25 flex items-center gap-1.5 transition"
          >
            <Plus className="w-4 h-4" /> New Research Notebook
          </Link>
          <Link
            to="/career"
            className="px-5 py-2.5 rounded-xl border border-white/10 bg-dark-bg/60 text-gray-300 hover:text-white font-semibold text-xs flex items-center gap-1.5 transition"
          >
            <Compass className="w-4 h-4 text-primary-400" /> Career Path
          </Link>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column (2 Cols wide): Primary Role Content */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* ========================================================== */}
          {/* STUDENT WIDGET: EDUCATION & CURRENT SUBJECTS */}
          {/* ========================================================== */}
          {userStatus.account_type === 'student' && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div className="flex items-center gap-2">
                  <GraduationCap className="w-5 h-5 text-primary-400" />
                  <h2 className="text-base font-bold text-white">Education Profile & Semester Courses</h2>
                </div>
                {currentEducationRecord && (
                  <span className="text-xs px-2.5 py-0.5 rounded-full bg-primary-500/10 text-primary-300 border border-primary-500/20 font-semibold">
                    {currentEducationRecord.degree_name || currentEducationRecord.level} {currentEducationRecord.current_semester ? `• ${currentEducationRecord.current_semester}` : ''}
                  </span>
                )}
              </div>

              {/* Active Subjects Pills */}
              <div>
                <h4 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Current Subjects ({subjects.length}):</h4>
                {subjects.length === 0 ? (
                  <p className="text-xs text-gray-500 italic">No semester subjects registered yet. Complete profile onboarding to attach course syllabi.</p>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    {subjects.slice(0, 4).map((sub) => (
                      <div key={sub.id} className="p-3 rounded-xl bg-dark-bg/60 border border-white/5 flex justify-between items-center text-xs">
                        <div className="font-semibold text-white truncate pr-2">{sub.name}</div>
                        <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 shrink-0">
                          {sub.syllabi_count ? 'Syllabus Attached' : 'No Syllabus'}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* ========================================================== */}
          {/* TEACHER WIDGET: PEDAGOGICAL AI & SUBJECTS */}
          {/* ========================================================== */}
          {userStatus.account_type === 'teacher' && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div className="flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-indigo-400" />
                  <h2 className="text-base font-bold text-white">Educator Studio & Course Management</h2>
                </div>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-semibold">
                  {teacherProfile?.teaching_position || 'Faculty'}
                </span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
                <Link
                  to="/research"
                  className="p-4 rounded-2xl bg-dark-bg/60 border border-white/5 hover:border-indigo-500/40 text-left space-y-1 group transition"
                >
                  <Sparkles className="w-4 h-4 text-indigo-400 group-hover:scale-110 transition" />
                  <div className="font-bold text-white">Lesson Plan Creator</div>
                  <p className="text-gray-400 text-[11px]">Generate 60-min interactive instructional blueprints.</p>
                </Link>

                <Link
                  to="/research"
                  className="p-4 rounded-2xl bg-dark-bg/60 border border-white/5 hover:border-indigo-500/40 text-left space-y-1 group transition"
                >
                  <FileText className="w-4 h-4 text-indigo-400 group-hover:scale-110 transition" />
                  <div className="font-bold text-white">Viva Voce & Question Bank</div>
                  <p className="text-gray-400 text-[11px]">Generate diagnostic oral exams and MCQs.</p>
                </Link>

                <Link
                  to="/research"
                  className="p-4 rounded-2xl bg-dark-bg/60 border border-white/5 hover:border-indigo-500/40 text-left space-y-1 group transition"
                >
                  <BookMarked className="w-4 h-4 text-indigo-400 group-hover:scale-110 transition" />
                  <div className="font-bold text-white">Lecture Notes Generator</div>
                  <p className="text-gray-400 text-[11px]">Draft structured revision sheets and summaries.</p>
                </Link>
              </div>
            </div>
          )}

          {/* ========================================================== */}
          {/* RESEARCH NOTEBOOKS WIDGET (NotebookLM Style) */}
          {/* ========================================================== */}
          <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <div className="flex items-center gap-2">
                <Microscope className="w-5 h-5 text-primary-400" />
                <h2 className="text-base font-bold text-white">Recent AI Research Notebooks ({notebooks.length})</h2>
              </div>
              <Link to="/research" className="text-xs text-primary-400 hover:text-primary-300 font-semibold flex items-center gap-1">
                View All <ChevronRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {notebooks.length === 0 ? (
              <div className="p-6 text-center border border-dashed border-white/10 rounded-2xl space-y-2">
                <p className="text-xs text-gray-400">No research notebooks created yet.</p>
                <Link
                  to="/research"
                  className="inline-flex px-4 py-1.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white text-xs font-semibold transition"
                >
                  Create Your First Notebook
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {notebooks.slice(0, 4).map((nb) => (
                  <Link
                    key={nb.id}
                    to="/research"
                    className="p-4 rounded-2xl bg-dark-bg/60 border border-white/5 hover:border-primary-500/30 transition text-xs space-y-2 block"
                  >
                    <div className="flex justify-between items-start">
                      <span className="font-bold text-white line-clamp-1">{nb.title}</span>
                      <span className="text-[10px] text-gray-500">{new Date(nb.updated_at).toLocaleDateString()}</span>
                    </div>
                    <div className="text-[11px] text-gray-400 flex items-center gap-2">
                      <FileText className="w-3 h-3 text-primary-400" />
                      <span>{nb.source_count || 0} reference sources</span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>

          {/* ========================================================== */}
          {/* CAREER ROADMAP PROGRESS WIDGET */}
          {/* ========================================================== */}
          {activePath && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
              <div className="flex justify-between items-center border-b border-white/10 pb-3">
                <div className="flex items-center gap-2">
                  <Compass className="w-5 h-5 text-indigo-400" />
                  <h2 className="text-base font-bold text-white">Career Roadmap: {activePath.title}</h2>
                </div>
                <Link to="/career" className="text-xs text-primary-400 hover:text-primary-300 font-semibold flex items-center gap-1">
                  Continue Roadmap <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              {/* Progress Bar */}
              <div>
                <div className="flex justify-between items-center text-xs mb-1.5">
                  <span className="text-gray-400">Total Curriculum Progress</span>
                  <span className="font-bold text-primary-400">{activePathProgress?.completion_percentage || 0}%</span>
                </div>
                <div className="h-2.5 w-full bg-dark-bg rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-primary-500 to-indigo-500 transition-all duration-500"
                    style={{ width: `${activePathProgress?.completion_percentage || 0}%` }}
                  />
                </div>
              </div>

              {/* Next Recommended Topic */}
              {activePathProgress?.recommended_next_topic && (
                <div className="p-3.5 rounded-2xl bg-primary-500/10 border border-primary-500/20 flex justify-between items-center text-xs">
                  <div>
                    <span className="text-[10px] font-bold uppercase text-primary-400 tracking-wider">Next Recommended Topic:</span>
                    <p className="font-bold text-white mt-0.5">{activePathProgress.recommended_next_topic.title}</p>
                  </div>
                  <Link
                    to="/career"
                    className="px-3 py-1.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold text-[11px] transition shrink-0"
                  >
                    Start Topic &rarr;
                  </Link>
                </div>
              )}
            </div>
          )}

        </div>

        {/* Right Column: Quick Planner & Knowledge Base */}
        <div className="space-y-6">
          
          {/* Quick Planner Tasks */}
          <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <div className="flex items-center gap-2">
                <CheckSquare className="w-5 h-5 text-emerald-400" />
                <h3 className="text-sm font-bold text-white">Upcoming Tasks ({plannerTasks.length})</h3>
              </div>
              <Link to="/planner" className="text-xs text-emerald-400 hover:text-emerald-300 font-semibold">
                Open Planner
              </Link>
            </div>

            {plannerTasks.length === 0 ? (
              <p className="text-xs text-gray-500 italic p-3 text-center">No active tasks in planner.</p>
            ) : (
              <div className="space-y-2">
                {plannerTasks.slice(0, 4).map((task) => (
                  <div key={task.id} className="p-3 rounded-xl bg-dark-bg/60 border border-white/5 flex items-center justify-between text-xs">
                    <span className="text-gray-200 truncate pr-2">{task.title}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-semibold shrink-0 ${
                      task.priority === 'High' ? 'bg-red-500/10 text-red-400' : 'bg-primary-500/10 text-primary-400'
                    }`}>
                      {task.priority || 'Medium'}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Personal Knowledge Base */}
          <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <div className="flex items-center gap-2">
                <BookMarked className="w-5 h-5 text-indigo-400" />
                <h3 className="text-sm font-bold text-white">Knowledge Base ({kbItems.length})</h3>
              </div>
              <Link to="/knowledge-base" className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold">
                View Repository
              </Link>
            </div>

            <p className="text-xs text-gray-400">
              Synced research papers, methodology notes, and career cheat-sheets stored persistently.
            </p>

            <div className="space-y-2">
              {kbItems.slice(0, 3).map((item) => (
                <div key={item.id} className="p-2.5 rounded-xl bg-dark-bg/60 border border-white/5 text-xs text-gray-300 truncate">
                  &bull; {item.title}
                </div>
              ))}
            </div>
          </div>

          {/* Connected Developer Accounts Status */}
          <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-bold text-white">Connected Accounts</h3>
              <Link to="/profile" className="text-xs text-primary-400 hover:underline">
                Manage
              </Link>
            </div>
            <p className="text-xs text-gray-400">
              Link GitHub to sync public repositories into your career profile, or add your LinkedIn & X links.
            </p>
          </div>

        </div>

      </div>

    </div>
  );
}
