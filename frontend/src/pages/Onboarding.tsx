import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  GraduationCap, BookOpen, Briefcase, User, CheckCircle2, ChevronRight,
  ChevronLeft, Sparkles, Plus, Trash2, Upload, FileText, Check, AlertCircle,
  Award, Globe, FileCheck
} from 'lucide-react';
import api from '../services/api';

export default function Onboarding() {
  const navigate = useNavigate();

  // Primary Account Type: None until selected, then 'student' | 'teacher' | 'professional'
  const [accountType, setAccountType] = useState<string | null>(null);

  // Student Step Index: 1 to 7
  const [studentStep, setStudentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // --- Step 1: Personal Info State ---
  const [personalInfo, setPersonalInfo] = useState({
    name: '',
    preferredName: '',
    email: localStorage.getItem('userEmail') || '',
    phoneNumber: '',
    dateOfBirth: '',
    country: 'India',
    state: '',
    city: '',
    preferredLanguage: 'English'
  });

  // --- Step 2: Education Records State ---
  const [activeLevel, setActiveLevel] = useState<'SSLC' | 'PUC' | 'Diploma' | 'UG' | 'PG' | 'PhD' | 'Other'>('UG');
  const [educationRecords, setEducationRecords] = useState<any[]>([]);
  const [currentRecord, setCurrentRecord] = useState({
    level: 'Undergraduate (UG)',
    status: 'Currently studying', // Completed, Currently studying, Not started
    institutionName: '',
    boardOrUniversity: '',
    stream: 'Science',
    degreeName: 'BE / B.Tech',
    specialization: 'Computer Science & Engineering',
    courseDuration: '4 Years',
    admissionYear: 2021,
    passingYear: 2025,
    expectedCompletionYear: 2025,
    currentClassOrYear: '4th Year',
    currentSemester: '7th Semester',
    resultPercentageCgpa: '',
    researchTitle: '',
    researchGuide: '',
    researchStatus: 'Ongoing'
  });

  // --- Step 3: Subjects & Syllabi State ---
  const [subjects, setSubjects] = useState<any[]>([]);
  const [newSubject, setNewSubject] = useState({ name: '', code: '', credits: 4, description: '' });
  const [syllabusModalSubject, setSyllabusModalSubject] = useState<any | null>(null);
  const [syllabusText, setSyllabusText] = useState('');
  const [syllabusUploadSuccess, setSyllabusUploadSuccess] = useState<string | null>(null);

  // --- Step 4: Learning Preferences State ---
  const [learningPrefs, setLearningPrefs] = useState({
    explanationLanguage: 'English',
    difficultyLevel: 'Intermediate',
    explanationDepth: 'detailed',
    codeExamplesRequired: true,
    visualExplanationsRequired: true,
    practiceQuestionsRequired: true,
    mcqsRequired: true,
    vivaPrepRequired: true,
    examPrepRequired: true
  });

  // --- Step 5: Career Info State ---
  const [careerInfo, setCareerInfo] = useState({
    careerGoal: 'Full Stack AI Platform Engineer',
    preferredPath: 'Python Full Stack Development',
    skills: 'Python, React, PostgreSQL, Docker',
    technologies: 'FastAPI, LangChain, Kubernetes, PyTorch',
    dailyHours: 2,
    targetWeeks: 12
  });

  // --- Step 6: Resume Upload State ---
  const [resumeParsedData, setResumeParsedData] = useState<any | null>(null);
  const [resumeId, setResumeId] = useState<string | null>(null);
  const [resumeConfirmed, setResumeConfirmed] = useState(false);

  // --- Step 7: Timeline State ---
  const [timeline, setTimeline] = useState<any[]>([]);

  // --- Teacher Form State ---
  const [teacherForm, setTeacherForm] = useState({
    institution: '',
    teachingPosition: 'Assistant Professor',
    department: 'Computer Science & Engineering',
    qualification: 'M.Tech / Ph.D',
    specialization: 'Artificial Intelligence & Systems',
    experienceYears: 5,
    subjectsTaught: 'Algorithms, Database Management, Operating Systems',
    currentClasses: 'B.Tech 3rd Year, M.Tech 1st Year'
  });

  // --- Professional Form State ---
  const [professionalForm, setProfessionalForm] = useState({
    name: '',
    profession: 'Software Engineer',
    organization: 'Technology Enterprise',
    skills: 'System Design, Cloud Infrastructure, Python',
    careerGoals: 'Build high-scale distributed intelligence systems',
    preferredLanguage: 'English',
    enabledModules: ['study', 'career', 'research', 'creator', 'planner', 'knowledge_base']
  });

  useEffect(() => {
    // Check if user already chose an account type
    const savedType = localStorage.getItem('accountType');
    if (savedType) {
      setAccountType(savedType);
    }
  }, []);

  // --- Handlers: Account Type Selection ---
  const handleSelectAccountType = async (type: string) => {
    setLoading(true);
    setError(null);
    try {
      await api.post('/auth/select-account-type', { account_type: type });
      setAccountType(type);
      localStorage.setItem('accountType', type);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to set account type');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Student Step 1 Save ---
  const handleSaveStep1 = async () => {
    setLoading(true);
    setError(null);
    try {
      await api.post('/education/personal-info', {
        name: personalInfo.name || personalInfo.email.split('@')[0],
        preferred_name: personalInfo.preferredName || personalInfo.name,
        email: personalInfo.email,
        phone_number: personalInfo.phoneNumber,
        date_of_birth: personalInfo.dateOfBirth,
        country: personalInfo.country,
        state: personalInfo.state,
        city: personalInfo.city,
        preferred_language: personalInfo.preferredLanguage
      });
      setStudentStep(2);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save personal info');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Student Step 2 Add Education Record ---
  const handleAddEducationRecord = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.post('/education/records', {
        level: currentRecord.level,
        status: currentRecord.status,
        institution_name: currentRecord.institutionName,
        board_or_university: currentRecord.boardOrUniversity,
        stream: currentRecord.stream,
        degree_name: currentRecord.degreeName,
        specialization: currentRecord.specialization,
        course_duration: currentRecord.courseDuration,
        admission_year: Number(currentRecord.admissionYear) || 2021,
        passing_year: Number(currentRecord.passingYear) || 2025,
        expected_completion_year: Number(currentRecord.expectedCompletionYear) || 2025,
        current_class_or_year: currentRecord.currentClassOrYear,
        current_semester: currentRecord.currentSemester,
        result_percentage_cgpa: currentRecord.resultPercentageCgpa,
        research_title: currentRecord.researchTitle,
        research_guide: currentRecord.researchGuide,
        research_status: currentRecord.researchStatus,
        chronological_order: educationRecords.length + 1
      });
      setEducationRecords([...educationRecords, res.data]);
      alert(`Saved qualification: ${currentRecord.level} (${currentRecord.status})`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save education record');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Student Step 3 Add Subject ---
  const handleAddSubject = async () => {
    if (!newSubject.name.trim()) return;
    setLoading(true);
    try {
      const res = await api.post('/education/subjects', newSubject);
      setSubjects([...subjects, res.data]);
      setNewSubject({ name: '', code: '', credits: 4, description: '' });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to add subject');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSyllabusFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0] || !syllabusModalSubject) return;
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      await api.post(`/education/subjects/${syllabusModalSubject.id}/syllabus-file`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setSyllabusUploadSuccess(`Uploaded & extracted syllabus for ${syllabusModalSubject.name}`);
      setTimeout(() => {
        setSyllabusModalSubject(null);
        setSyllabusUploadSuccess(null);
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload syllabus');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveSyllabusText = async () => {
    if (!syllabusText.trim() || !syllabusModalSubject) return;
    setLoading(true);
    try {
      await api.post(`/education/subjects/${syllabusModalSubject.id}/syllabus-text`, {
        title: `Syllabus for ${syllabusModalSubject.name}`,
        content_text: syllabusText
      });
      setSyllabusUploadSuccess(`Saved syllabus text for ${syllabusModalSubject.name}`);
      setTimeout(() => {
        setSyllabusModalSubject(null);
        setSyllabusUploadSuccess(null);
        setSyllabusText('');
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save syllabus text');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Student Step 4 Preferences ---
  const handleSaveStep4 = async () => {
    setLoading(true);
    try {
      await api.post('/education/learning-preferences', {
        explanation_language: learningPrefs.explanationLanguage,
        difficulty_level: learningPrefs.difficultyLevel,
        explanation_depth: learningPrefs.explanationDepth,
        code_examples_required: learningPrefs.codeExamplesRequired,
        visual_explanations_required: learningPrefs.visualExplanationsRequired,
        practice_questions_required: learningPrefs.practiceQuestionsRequired,
        mcqs_required: learningPrefs.mcqsRequired,
        viva_prep_required: learningPrefs.vivaPrepRequired,
        exam_prep_required: learningPrefs.examPrepRequired
      });
      setStudentStep(5);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save preferences');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Student Step 5 Career Info ---
  const handleSaveStep5 = async () => {
    setLoading(true);
    try {
      await api.post('/education/career-info', {
        career_goal: careerInfo.careerGoal,
        preferred_career_path: careerInfo.preferredPath,
        current_skills: careerInfo.skills.split(',').map(s => s.trim()).filter(Boolean),
        technologies_interested: careerInfo.technologies.split(',').map(s => s.trim()).filter(Boolean),
        daily_learning_time_minutes: Number(careerInfo.dailyHours) * 60,
        target_completion_weeks: Number(careerInfo.targetWeeks)
      });
      setStudentStep(6);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save career info');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Student Step 6 Resume Upload & Confirmation ---
  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0]) return;
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError(null);
    try {
      const res = await api.post('/education/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResumeParsedData(res.data.parsed_sections);
      setResumeId(res.data.resume_id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Resume parsing failed');
    } finally {
      setLoading(false);
    }
  };

  const handleConfirmResume = async () => {
    if (!resumeId) return;
    setLoading(true);
    try {
      await api.post('/education/resume/confirm', {
        resume_id: resumeId,
        skills: resumeParsedData?.skills || [],
        education: resumeParsedData?.education || []
      });
      setResumeConfirmed(true);
      setTimeout(() => {
        handleLoadTimeline();
        setStudentStep(7);
      }, 1000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to confirm resume data');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Step 7 Timeline & Completion ---
  const handleLoadTimeline = async () => {
    try {
      const res = await api.get('/education/timeline');
      setTimeline(res.data.timeline || []);
    } catch (err) {
      console.error(err);
    }
  };

  const handleFinishOnboarding = async () => {
    setLoading(true);
    try {
      await api.post('/education/complete');
      localStorage.setItem('profileCompleted', 'true');
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to finalize profile');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Teacher Profile Submit ---
  const handleSaveTeacher = async () => {
    setLoading(true);
    setError(null);
    try {
      await api.post('/teacher/profile', {
        institution: teacherForm.institution,
        teaching_position: teacherForm.teachingPosition,
        department: teacherForm.department,
        qualification: teacherForm.qualification,
        specialization: teacherForm.specialization,
        teaching_experience_years: Number(teacherForm.experienceYears),
        subjects_taught: teacherForm.subjectsTaught.split(',').map(s => s.trim()).filter(Boolean),
        current_classes_semesters: teacherForm.currentClasses.split(',').map(s => s.trim()).filter(Boolean)
      });
      localStorage.setItem('profileCompleted', 'true');
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save educator profile');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Professional Profile Submit ---
  const handleSaveProfessional = async () => {
    setLoading(true);
    setError(null);
    try {
      await api.post('/professional/profile', {
        name: professionalForm.name || personalInfo.email.split('@')[0],
        profession: professionalForm.profession,
        organization: professionalForm.organization,
        skills: professionalForm.skills.split(',').map(s => s.trim()).filter(Boolean),
        career_goals: professionalForm.careerGoals,
        preferred_language: professionalForm.preferredLanguage,
        enabled_modules: professionalForm.enabledModules
      });
      localStorage.setItem('profileCompleted', 'true');
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save professional profile');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6">

      {/* Header Banner */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary-500/10 border border-primary-500/20 text-primary-400 text-xs font-semibold uppercase tracking-wider mb-2">
          <Sparkles className="w-3.5 h-3.5" /> First-Time Experience
        </div>
        <h1 className="text-3xl font-extrabold text-white">Setup Your Nexora AI Workspace</h1>
        <p className="text-gray-400 text-sm mt-1">
          Customize your personalized learning roadmap, research notebook suite, and pedagogical assistance.
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 text-sm flex items-center gap-3">
          <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* STAGE 0: Initial Account Type Selection */}
      {!accountType && (
        <div className="glass-panel p-8 rounded-3xl border border-white/10 shadow-2xl animate-in fade-in duration-300">
          <h2 className="text-2xl font-bold text-white text-center mb-2">
            How would you like to use Nexora AI?
          </h2>
          <p className="text-center text-gray-400 text-sm mb-8">
            Select your primary role. You can customize modules and change your profile settings anytime.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Student Card */}
            <div
              onClick={() => handleSelectAccountType('student')}
              className="p-6 rounded-2xl bg-dark-bg/60 border border-white/10 hover:border-primary-500/60 hover:bg-primary-500/5 cursor-pointer transition-all duration-300 group flex flex-col justify-between"
            >
              <div>
                <div className="p-4 rounded-2xl bg-primary-500/10 text-primary-400 w-fit mb-4 group-hover:scale-110 transition duration-300">
                  <GraduationCap className="w-8 h-8" />
                </div>
                <h3 className="text-lg font-bold text-white mb-1">Student / Scholar</h3>
                <p className="text-xs text-gray-400 leading-relaxed">
                  Step-by-step education journey, semester subjects, syllabus uploads, career roadmaps, and AI study notes.
                </p>
              </div>
              <button className="mt-6 w-full py-2.5 rounded-xl bg-primary-500/20 text-primary-300 text-xs font-semibold group-hover:bg-primary-600 group-hover:text-white transition">
                Continue as Student &rarr;
              </button>
            </div>

            {/* Teacher Card */}
            <div
              onClick={() => handleSelectAccountType('teacher')}
              className="p-6 rounded-2xl bg-dark-bg/60 border border-white/10 hover:border-indigo-500/60 hover:bg-indigo-500/5 cursor-pointer transition-all duration-300 group flex flex-col justify-between"
            >
              <div>
                <div className="p-4 rounded-2xl bg-indigo-500/10 text-indigo-400 w-fit mb-4 group-hover:scale-110 transition duration-300">
                  <BookOpen className="w-8 h-8" />
                </div>
                <h3 className="text-lg font-bold text-white mb-1">Teacher / Educator</h3>
                <p className="text-xs text-gray-400 leading-relaxed">
                  Manage teaching subjects, lecture notes, syllabus materials, and generate lesson plans, viva questions & MCQs.
                </p>
              </div>
              <button className="mt-6 w-full py-2.5 rounded-xl bg-indigo-500/20 text-indigo-300 text-xs font-semibold group-hover:bg-indigo-600 group-hover:text-white transition">
                Continue as Educator &rarr;
              </button>
            </div>

            {/* Professional Card */}
            <div
              onClick={() => handleSelectAccountType('professional')}
              className="p-6 rounded-2xl bg-dark-bg/60 border border-white/10 hover:border-emerald-500/60 hover:bg-emerald-500/5 cursor-pointer transition-all duration-300 group flex flex-col justify-between"
            >
              <div>
                <div className="p-4 rounded-2xl bg-emerald-500/10 text-emerald-400 w-fit mb-4 group-hover:scale-110 transition duration-300">
                  <Briefcase className="w-8 h-8" />
                </div>
                <h3 className="text-lg font-bold text-white mb-1">Other / Professional</h3>
                <p className="text-xs text-gray-400 leading-relaxed">
                  Research notebooks, career transitions, project tracking, developer connections, and custom workspace modules.
                </p>
              </div>
              <button className="mt-6 w-full py-2.5 rounded-xl bg-emerald-500/20 text-emerald-300 text-xs font-semibold group-hover:bg-emerald-600 group-hover:text-white transition">
                Continue as Professional &rarr;
              </button>
            </div>

          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* CASE A: STUDENT DYNAMIC EDUCATION PROFILE (7 STEPS) */}
      {/* ============================================================== */}
      {accountType === 'student' && (
        <div className="space-y-6">
          
          {/* Progress Tracker */}
          <div className="glass-panel p-4 rounded-2xl border border-white/10">
            <div className="flex justify-between items-center text-xs text-gray-400 mb-2">
              <span className="font-semibold text-primary-400">Step {studentStep} of 7: {
                studentStep === 1 ? 'Personal Info' :
                studentStep === 2 ? 'Education Qualifications' :
                studentStep === 3 ? 'Subjects & Syllabus' :
                studentStep === 4 ? 'Learning Preferences' :
                studentStep === 5 ? 'Career Goals' :
                studentStep === 6 ? 'Resume Upload (Optional)' : 'Timeline & Review'
              }</span>
              <span>{Math.round((studentStep / 7) * 100)}% Complete</span>
            </div>
            <div className="h-2 w-full bg-dark-bg rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-primary-500 to-indigo-500 transition-all duration-500 ease-out"
                style={{ width: `${(studentStep / 7) * 100}%` }}
              />
            </div>
          </div>

          {/* STEP 1: Personal Information */}
          {studentStep === 1 && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <User className="w-5 h-5 text-primary-400" /> Personal Information
                </h2>
                <p className="text-xs text-gray-400 mt-1">Let us know how to address you and locate relevant academic resources.</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Full Name *</label>
                  <input
                    type="text"
                    value={personalInfo.name}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, name: e.target.value })}
                    placeholder="e.g. Darshan Sharma"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Preferred Name</label>
                  <input
                    type="text"
                    value={personalInfo.preferredName}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, preferredName: e.target.value })}
                    placeholder="e.g. Darshan"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Phone Number (Optional)</label>
                  <input
                    type="text"
                    value={personalInfo.phoneNumber}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, phoneNumber: e.target.value })}
                    placeholder="+91 9876543210"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Date of Birth (Optional)</label>
                  <input
                    type="date"
                    value={personalInfo.dateOfBirth}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, dateOfBirth: e.target.value })}
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Country</label>
                  <input
                    type="text"
                    value={personalInfo.country}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, country: e.target.value })}
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">State / Province</label>
                  <input
                    type="text"
                    value={personalInfo.state}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, state: e.target.value })}
                    placeholder="Karnataka"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">City</label>
                  <input
                    type="text"
                    value={personalInfo.city}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, city: e.target.value })}
                    placeholder="Bengaluru"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Preferred Explanation Language</label>
                  <select
                    value={personalInfo.preferredLanguage}
                    onChange={(e) => setPersonalInfo({ ...personalInfo, preferredLanguage: e.target.value })}
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="English">English</option>
                    <option value="Hindi">Hindi</option>
                    <option value="Kannada">Kannada</option>
                    <option value="Tamil">Tamil</option>
                    <option value="Telugu">Telugu</option>
                    <option value="Malayalam">Malayalam</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end pt-4">
                <button
                  onClick={handleSaveStep1}
                  disabled={loading}
                  className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold text-sm flex items-center gap-2 transition"
                >
                  Continue to Education Qualifications <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 2: Education Qualifications (Dynamic Accordion / Multi-Level) */}
          {studentStep === 2 && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <GraduationCap className="w-5 h-5 text-primary-400" /> Education Journey
                </h2>
                <p className="text-xs text-gray-400 mt-1">
                  Add qualifications one level at a time in chronological order. Questions adapt whether you are completed or currently studying.
                </p>
              </div>

              {/* Education Level Selector Pills */}
              <div className="flex flex-wrap gap-2">
                {[
                  { key: 'SSLC', label: 'SSLC / 10th' },
                  { key: 'PUC', label: 'PUC / 12th' },
                  { key: 'Diploma', label: 'Diploma' },
                  { key: 'UG', label: 'Undergraduate (UG)' },
                  { key: 'PG', label: 'Postgraduate (PG)' },
                  { key: 'PhD', label: 'PhD / Research' },
                  { key: 'Other', label: 'Other Education' }
                ].map((item: any) => (
                  <button
                    key={item.key}
                    onClick={() => {
                      setActiveLevel(item.key);
                      setCurrentRecord({
                        ...currentRecord,
                        level: item.label,
                        status: item.key === 'UG' ? 'Currently studying' : 'Completed'
                      });
                    }}
                    className={`px-4 py-2 rounded-xl text-xs font-semibold border transition ${
                      activeLevel === item.key
                        ? 'bg-primary-500/20 border-primary-500 text-primary-300'
                        : 'bg-dark-bg/40 border-white/10 text-gray-400 hover:border-white/20'
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>

              {/* Dynamic Form based on selected active level */}
              <div className="p-5 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-4">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <h3 className="text-sm font-bold text-white">Configuring: {currentRecord.level}</h3>
                  <div className="flex gap-2 text-xs">
                    {['Completed', 'Currently studying', 'Not started'].map((st) => (
                      <button
                        key={st}
                        onClick={() => setCurrentRecord({ ...currentRecord, status: st })}
                        className={`px-3 py-1 rounded-lg border transition ${
                          currentRecord.status === st
                            ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 font-semibold'
                            : 'bg-dark-bg/60 border-white/10 text-gray-400'
                        }`}
                      >
                        {st}
                      </button>
                    ))}
                  </div>
                </div>

                {currentRecord.status === 'Not started' ? (
                  <p className="text-xs text-gray-400 py-4 text-center">
                    You have marked {currentRecord.level} as Not Started. You can proceed to your applicable degree.
                  </p>
                ) : (
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-medium text-gray-300 mb-1">Institution / School / College Name *</label>
                      <input
                        type="text"
                        value={currentRecord.institutionName}
                        onChange={(e) => setCurrentRecord({ ...currentRecord, institutionName: e.target.value })}
                        placeholder="e.g. BMS College of Engineering"
                        className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-300 mb-1">Board or University</label>
                      <input
                        type="text"
                        value={currentRecord.boardOrUniversity}
                        onChange={(e) => setCurrentRecord({ ...currentRecord, boardOrUniversity: e.target.value })}
                        placeholder="e.g. VTU / CBSE / State Board"
                        className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                      />
                    </div>

                    {(activeLevel === 'UG' || activeLevel === 'PG') && (
                      <>
                        <div>
                          <label className="block text-xs font-medium text-gray-300 mb-1">Degree Name</label>
                          <input
                            type="text"
                            value={currentRecord.degreeName}
                            onChange={(e) => setCurrentRecord({ ...currentRecord, degreeName: e.target.value })}
                            placeholder="BE / B.Tech / BCA / MCA"
                            className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-300 mb-1">Specialization / Major</label>
                          <input
                            type="text"
                            value={currentRecord.specialization}
                            onChange={(e) => setCurrentRecord({ ...currentRecord, specialization: e.target.value })}
                            placeholder="Computer Science, AI, Mechanical"
                            className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                      </>
                    )}

                    {currentRecord.status === 'Currently studying' && (
                      <>
                        <div>
                          <label className="block text-xs font-medium text-gray-300 mb-1">Current Academic Year</label>
                          <input
                            type="text"
                            value={currentRecord.currentClassOrYear}
                            onChange={(e) => setCurrentRecord({ ...currentRecord, currentClassOrYear: e.target.value })}
                            placeholder="e.g. 4th Year / Final Year"
                            className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-300 mb-1">Current Semester</label>
                          <input
                            type="text"
                            value={currentRecord.currentSemester}
                            onChange={(e) => setCurrentRecord({ ...currentRecord, currentSemester: e.target.value })}
                            placeholder="e.g. 7th Semester"
                            className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                      </>
                    )}

                    {currentRecord.status === 'Completed' && (
                      <>
                        <div>
                          <label className="block text-xs font-medium text-gray-300 mb-1">Passing Year</label>
                          <input
                            type="number"
                            value={currentRecord.passingYear}
                            onChange={(e) => setCurrentRecord({ ...currentRecord, passingYear: Number(e.target.value) })}
                            className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-300 mb-1">Result / Percentage / CGPA (Optional)</label>
                          <input
                            type="text"
                            value={currentRecord.resultPercentageCgpa}
                            onChange={(e) => setCurrentRecord({ ...currentRecord, resultPercentageCgpa: e.target.value })}
                            placeholder="e.g. 9.1 CGPA or 88.5%"
                            className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                      </>
                    )}
                  </div>
                )}

                <div className="flex justify-end pt-2">
                  <button
                    onClick={handleAddEducationRecord}
                    disabled={loading || currentRecord.status === 'Not started'}
                    className="px-4 py-2 rounded-xl bg-primary-500/20 border border-primary-500/40 text-primary-300 hover:bg-primary-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
                  >
                    <Plus className="w-4 h-4" /> Save Qualification Entry
                  </button>
                </div>
              </div>

              {/* Saved Records Summary */}
              {educationRecords.length > 0 && (
                <div className="space-y-2 pt-2">
                  <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Added Qualifications:</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {educationRecords.map((r, i) => (
                      <div key={i} className="p-3 rounded-xl bg-dark-bg/80 border border-white/10 text-xs flex justify-between items-center">
                        <div>
                          <span className="font-bold text-white">{r.level}</span> — <span className="text-primary-300">{r.status}</span>
                          <div className="text-gray-400">{r.institution_name} {r.degree_name ? `(${r.degree_name})` : ''}</div>
                        </div>
                        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex justify-between pt-4 border-t border-white/10">
                <button
                  onClick={() => setStudentStep(1)}
                  className="px-5 py-2.5 rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button
                  onClick={() => setStudentStep(3)}
                  className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold text-sm flex items-center gap-2 transition"
                >
                  Continue to Subjects & Syllabus <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 3: Current Subjects & Syllabus Ingestion */}
          {studentStep === 3 && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <BookOpen className="w-5 h-5 text-primary-400" /> Current Subjects & Syllabus Management
                </h2>
                <p className="text-xs text-gray-400 mt-1">
                  Which subjects are you studying currently? Add multiple subjects and optionally upload your syllabus file or paste text.
                </p>
              </div>

              {/* Add Subject Input */}
              <div className="p-4 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-3">
                <h3 className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Add a Current Subject</h3>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <input
                    type="text"
                    value={newSubject.name}
                    onChange={(e) => setNewSubject({ ...newSubject, name: e.target.value })}
                    placeholder="Subject Name (e.g. Distributed Systems)"
                    className="sm:col-span-2 bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                  <input
                    type="text"
                    value={newSubject.code}
                    onChange={(e) => setNewSubject({ ...newSubject, code: e.target.value })}
                    placeholder="Code (e.g. CS701)"
                    className="bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
                <div className="flex justify-end">
                  <button
                    onClick={handleAddSubject}
                    className="px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white text-xs font-semibold flex items-center gap-1.5 transition"
                  >
                    <Plus className="w-4 h-4" /> Add Subject
                  </button>
                </div>
              </div>

              {/* Active Subjects List */}
              <div className="space-y-3">
                <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Your Active Subjects ({subjects.length}):</h4>
                {subjects.length === 0 ? (
                  <p className="text-xs text-gray-500 italic p-4 text-center border border-dashed border-white/10 rounded-xl">
                    No subjects added yet. Add your current courses above to link your syllabus and lecture notes.
                  </p>
                ) : (
                  <div className="space-y-2">
                    {subjects.map((sub) => (
                      <div key={sub.id} className="p-4 rounded-xl bg-dark-bg/80 border border-white/10 flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                        <div>
                          <div className="font-bold text-white text-sm flex items-center gap-2">
                            {sub.name} {sub.code && <span className="text-xs px-2 py-0.5 rounded bg-primary-500/10 text-primary-400 border border-primary-500/20">{sub.code}</span>}
                          </div>
                          <div className="text-xs text-gray-400 mt-0.5">
                            Syllabus documents attached: <span className="text-primary-300 font-semibold">{sub.syllabi_count || 0}</span>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => setSyllabusModalSubject(sub)}
                            className="px-3 py-1.5 rounded-lg bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 hover:bg-indigo-500/30 text-xs font-semibold flex items-center gap-1.5 transition"
                          >
                            <Upload className="w-3.5 h-3.5" /> Attach Syllabus
                          </button>
                          <button
                            onClick={() => setSubjects(subjects.filter(s => s.id !== sub.id))}
                            className="p-1.5 rounded-lg text-gray-500 hover:text-red-400 hover:bg-white/5 transition"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Syllabus Attach Modal */}
              {syllabusModalSubject && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
                  <div className="w-full max-w-lg bg-dark-card border border-white/10 rounded-2xl p-6 glass-panel space-y-4">
                    <h3 className="text-base font-bold text-white flex items-center gap-2">
                      <FileText className="w-5 h-5 text-indigo-400" /> Attach Syllabus: {syllabusModalSubject.name}
                    </h3>
                    
                    {syllabusUploadSuccess && (
                      <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs">
                        {syllabusUploadSuccess}
                      </div>
                    )}

                    <div className="space-y-3">
                      <div>
                        <label className="block text-xs font-medium text-gray-300 mb-1">Upload File (PDF, DOCX, TXT, Image)</label>
                        <input
                          type="file"
                          accept=".pdf,.docx,.doc,.txt,.png,.jpg"
                          onChange={handleUploadSyllabusFile}
                          className="w-full text-xs text-gray-400 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-primary-500/20 file:text-primary-300 hover:file:bg-primary-500/30 cursor-pointer"
                        />
                      </div>

                      <div className="text-center text-xs text-gray-500">— OR PASTE TEXT —</div>

                      <div>
                        <label className="block text-xs font-medium text-gray-300 mb-1">Paste Syllabus Units / Course Outline</label>
                        <textarea
                          rows={4}
                          value={syllabusText}
                          onChange={(e) => setSyllabusText(e.target.value)}
                          placeholder="Paste syllabus modules, topics, or reference books..."
                          className="w-full bg-dark-bg/60 border border-white/10 rounded-xl p-3 text-xs text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>
                    </div>

                    <div className="flex justify-end gap-2 pt-2">
                      <button
                        onClick={() => setSyllabusModalSubject(null)}
                        className="px-4 py-2 rounded-xl text-xs text-gray-400 hover:bg-white/5"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={handleSaveSyllabusText}
                        disabled={loading || !syllabusText.trim()}
                        className="px-4 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white text-xs font-semibold disabled:opacity-50"
                      >
                        Save Syllabus Text
                      </button>
                    </div>
                  </div>
                </div>
              )}

              <div className="flex justify-between pt-4 border-t border-white/10">
                <button
                  onClick={() => setStudentStep(2)}
                  className="px-5 py-2.5 rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button
                  onClick={() => setStudentStep(4)}
                  className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold text-sm flex items-center gap-2 transition"
                >
                  Continue to Learning Preferences <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 4: Learning Preferences */}
          {studentStep === 4 && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Globe className="w-5 h-5 text-primary-400" /> Learning Preferences
                </h2>
                <p className="text-xs text-gray-400 mt-1">
                  Configure how AI explains technical concepts and formats revision materials.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Difficulty Level</label>
                  <select
                    value={learningPrefs.difficultyLevel}
                    onChange={(e) => setLearningPrefs({ ...learningPrefs, difficultyLevel: e.target.value })}
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="Beginner">Beginner (Foundational principles)</option>
                    <option value="Intermediate">Intermediate (Real-world applications)</option>
                    <option value="Advanced">Advanced (Internal memory models & RFCs)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Explanation Depth</label>
                  <select
                    value={learningPrefs.explanationDepth}
                    onChange={(e) => setLearningPrefs({ ...learningPrefs, explanationDepth: e.target.value })}
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="detailed">Detailed (Comprehensive notes & deep architecture)</option>
                    <option value="simple">Simple (Plain English & quick analogies)</option>
                  </select>
                </div>
              </div>

              {/* Toggles */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                {[
                  { key: 'codeExamplesRequired', label: 'Practical Code Examples' },
                  { key: 'visualExplanationsRequired', label: 'Visual Explanations & Diagrams' },
                  { key: 'practiceQuestionsRequired', label: 'Coding Practice Questions' },
                  { key: 'mcqsRequired', label: 'Multiple Choice Questions (MCQs)' },
                  { key: 'vivaPrepRequired', label: 'Viva Voce & Oral Exam Prep' },
                  { key: 'examPrepRequired', label: 'Standard University Exam Prep' }
                ].map((tog: any) => (
                  <label
                    key={tog.key}
                    className="flex items-center justify-between p-3.5 rounded-xl bg-dark-bg/60 border border-white/10 cursor-pointer hover:border-primary-500/40 transition"
                  >
                    <span className="text-xs font-medium text-white">{tog.label}</span>
                    <input
                      type="checkbox"
                      checked={(learningPrefs as any)[tog.key]}
                      onChange={(e) => setLearningPrefs({ ...learningPrefs, [tog.key]: e.target.checked })}
                      className="w-4 h-4 rounded text-primary-500 focus:ring-primary-500 bg-dark-bg border-white/20"
                    />
                  </label>
                ))}
              </div>

              <div className="flex justify-between pt-4 border-t border-white/10">
                <button
                  onClick={() => setStudentStep(3)}
                  className="px-5 py-2.5 rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button
                  onClick={handleSaveStep4}
                  className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold text-sm flex items-center gap-2 transition"
                >
                  Continue to Career Goals <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 5: Career Information */}
          {studentStep === 5 && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Briefcase className="w-5 h-5 text-primary-400" /> Career Goals & Roadmap Selection
                </h2>
                <p className="text-xs text-gray-400 mt-1">
                  Connect your academic studies with industry career tracks and daily learning targets.
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="sm:col-span-2">
                  <label className="block text-xs font-medium text-gray-300 mb-1">Career Goal / Target Role</label>
                  <input
                    type="text"
                    value={careerInfo.careerGoal}
                    onChange={(e) => setCareerInfo({ ...careerInfo, careerGoal: e.target.value })}
                    placeholder="e.g. Senior AI Systems Architect"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Preferred Career Roadmap</label>
                  <select
                    value={careerInfo.preferredPath}
                    onChange={(e) => setCareerInfo({ ...careerInfo, preferredPath: e.target.value })}
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="Java Full Stack Development">Java Full Stack Development (19 Topics)</option>
                    <option value="Python Full Stack Development">Python Full Stack Development (16 Topics)</option>
                    <option value="Data Analysis">Data Analysis & BI (14 Topics)</option>
                    <option value="AI / ML">AI / Machine Learning Engineering</option>
                    <option value="Cloud / DevOps">Cloud & DevOps Engineering</option>
                    <option value="Web Development">Modern Web Development</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-300 mb-1">Daily Available Study Time</label>
                  <select
                    value={careerInfo.dailyHours}
                    onChange={(e) => setCareerInfo({ ...careerInfo, dailyHours: Number(e.target.value) })}
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value={1}>1 Hour per day</option>
                    <option value={2}>2 Hours per day</option>
                    <option value={3}>3 Hours per day</option>
                    <option value={4}>4+ Hours per day</option>
                  </select>
                </div>

                <div className="sm:col-span-2">
                  <label className="block text-xs font-medium text-gray-300 mb-1">Current Skills (comma separated)</label>
                  <input
                    type="text"
                    value={careerInfo.skills}
                    onChange={(e) => setCareerInfo({ ...careerInfo, skills: e.target.value })}
                    placeholder="Python, SQL, React, Git"
                    className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
              </div>

              <div className="flex justify-between pt-4 border-t border-white/10">
                <button
                  onClick={() => setStudentStep(4)}
                  className="px-5 py-2.5 rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button
                  onClick={handleSaveStep5}
                  className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold text-sm flex items-center gap-2 transition"
                >
                  Continue to Resume Upload <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 6: Resume Upload (Optional with Confirmation) */}
          {studentStep === 6 && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <FileCheck className="w-5 h-5 text-primary-400" /> Resume Upload & Review (Optional)
                </h2>
                <p className="text-xs text-gray-400 mt-1">
                  Upload your CV in PDF, DOCX or TXT format. We will extract your skills, education, and projects for your review before saving.
                </p>
              </div>

              {!resumeParsedData ? (
                <div className="border-2 border-dashed border-white/20 rounded-2xl p-8 text-center space-y-3 bg-dark-bg/40 hover:border-primary-500/50 transition">
                  <div className="p-4 rounded-2xl bg-primary-500/10 text-primary-400 w-fit mx-auto">
                    <Upload className="w-8 h-8" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">Upload Your Resume</h3>
                    <p className="text-xs text-gray-400 mt-1">PDF, DOC, DOCX or TXT up to 10MB</p>
                  </div>
                  <input
                    type="file"
                    accept=".pdf,.docx,.doc,.txt"
                    onChange={handleResumeUpload}
                    className="hidden"
                    id="resume-file-input"
                  />
                  <label
                    htmlFor="resume-file-input"
                    className="inline-flex px-5 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white text-xs font-semibold cursor-pointer transition shadow-lg shadow-primary-500/20"
                  >
                    Select Resume File
                  </label>
                  <div className="pt-2">
                    <button
                      onClick={() => {
                        handleLoadTimeline();
                        setStudentStep(7);
                      }}
                      className="text-xs text-gray-400 hover:text-white underline"
                    >
                      Skip this step and continue
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center justify-between">
                    <span>Extracted structured sections ready for confirmation.</span>
                    {resumeConfirmed && <span className="font-bold flex items-center gap-1"><Check className="w-4 h-4" /> Confirmed</span>}
                  </div>

                  {/* Skills Extracted */}
                  <div className="p-4 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-2">
                    <h4 className="text-xs font-bold text-white uppercase tracking-wider">Identified Skills:</h4>
                    <div className="flex flex-wrap gap-1.5">
                      {resumeParsedData.skills?.map((sk: any, i: number) => (
                        <span key={i} className="px-2.5 py-1 rounded-lg bg-primary-500/10 text-primary-300 border border-primary-500/20 text-xs">
                          {sk.name || sk}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Projects Extracted */}
                  <div className="p-4 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-2">
                    <h4 className="text-xs font-bold text-white uppercase tracking-wider">Identified Projects:</h4>
                    <div className="space-y-1.5">
                      {resumeParsedData.projects?.map((pj: any, i: number) => (
                        <div key={i} className="text-xs text-gray-300">
                          &bull; <span className="font-semibold text-white">{pj.title}</span> — {pj.description}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-end gap-3 pt-2">
                    <button
                      onClick={handleConfirmResume}
                      disabled={loading || resumeConfirmed}
                      className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs flex items-center gap-2 transition disabled:opacity-50"
                    >
                      <Check className="w-4 h-4" /> Confirm & Merge Into Profile
                    </button>
                  </div>
                </div>
              )}

              <div className="flex justify-between pt-4 border-t border-white/10">
                <button
                  onClick={() => setStudentStep(5)}
                  className="px-5 py-2.5 rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button
                  onClick={() => {
                    handleLoadTimeline();
                    setStudentStep(7);
                  }}
                  className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-semibold text-sm flex items-center gap-2 transition"
                >
                  Next: Education Timeline <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {/* STEP 7: Education Timeline & Profile Finalization */}
          {studentStep === 7 && (
            <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
              <div className="border-b border-white/10 pb-4">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <Award className="w-5 h-5 text-emerald-400" /> Education Journey Timeline
                </h2>
                <p className="text-xs text-gray-400 mt-1">
                  Verify your complete academic trajectory before entering your personalized Nexora dashboard.
                </p>
              </div>

              {/* Visual Timeline Nodes */}
              <div className="space-y-4 py-2">
                {timeline.map((item, idx) => (
                  <div key={idx} className="relative flex items-start gap-4">
                    {/* Circle Node */}
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 border ${
                      item.status === 'Completed'
                        ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300'
                        : item.status === 'Currently studying'
                        ? 'bg-primary-500/20 border-primary-500 text-primary-300 animate-pulse'
                        : 'bg-dark-bg/60 border-white/10 text-gray-500'
                    }`}>
                      {item.status === 'Completed' ? <Check className="w-4 h-4" /> : idx + 1}
                    </div>

                    {/* Details */}
                    <div className="flex-1 p-3.5 rounded-xl bg-dark-bg/60 border border-white/10">
                      <div className="flex justify-between items-center">
                        <h4 className="font-bold text-white text-sm">{item.stage}</h4>
                        <span className={`text-xs px-2.5 py-0.5 rounded-full font-semibold ${
                          item.status === 'Completed' ? 'bg-emerald-500/10 text-emerald-300 border border-emerald-500/20' :
                          item.status === 'Currently studying' ? 'bg-primary-500/10 text-primary-300 border border-primary-500/20' :
                          'bg-white/5 text-gray-400'
                        }`}>
                          {item.status}
                        </span>
                      </div>
                      {item.institution && (
                        <p className="text-xs text-gray-300 mt-1">
                          {item.institution} {item.degree ? `(${item.degree})` : ''}
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex justify-between pt-4 border-t border-white/10">
                <button
                  onClick={() => setStudentStep(6)}
                  className="px-5 py-2.5 rounded-xl border border-white/10 text-gray-300 hover:bg-white/5 text-xs font-semibold flex items-center gap-1.5 transition"
                >
                  <ChevronLeft className="w-4 h-4" /> Back
                </button>
                <button
                  onClick={handleFinishOnboarding}
                  disabled={loading}
                  className="px-8 py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-sm shadow-xl shadow-emerald-500/20 flex items-center gap-2 transition"
                >
                  <CheckCircle2 className="w-5 h-5" /> Enter My Nexora Dashboard &rarr;
                </button>
              </div>
            </div>
          )}

        </div>
      )}

      {/* ============================================================== */}
      {/* CASE B: TEACHER / EDUCATOR PROFILE SETUP */}
      {/* ============================================================== */}
      {accountType === 'teacher' && (
        <div className="glass-panel p-8 rounded-3xl border border-white/10 space-y-6">
          <div className="border-b border-white/10 pb-4">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <BookOpen className="w-6 h-6 text-indigo-400" /> Teacher & Educator Profile
            </h2>
            <p className="text-xs text-gray-400 mt-1">
              Provide your institutional details to unlock AI lesson plans, lecture note creators, and question generators.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Institution / University *</label>
              <input
                type="text"
                value={teacherForm.institution}
                onChange={(e) => setTeacherForm({ ...teacherForm, institution: e.target.value })}
                placeholder="e.g. National Institute of Technology"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Teaching Position / Role</label>
              <input
                type="text"
                value={teacherForm.teachingPosition}
                onChange={(e) => setTeacherForm({ ...teacherForm, teachingPosition: e.target.value })}
                placeholder="e.g. Associate Professor"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Department</label>
              <input
                type="text"
                value={teacherForm.department}
                onChange={(e) => setTeacherForm({ ...teacherForm, department: e.target.value })}
                placeholder="e.g. Computer Science & Engineering"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Highest Qualification</label>
              <input
                type="text"
                value={teacherForm.qualification}
                onChange={(e) => setTeacherForm({ ...teacherForm, qualification: e.target.value })}
                placeholder="Ph.D / M.Tech / M.Sc"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="block text-xs font-medium text-gray-300 mb-1">Subjects Taught (comma separated)</label>
              <input
                type="text"
                value={teacherForm.subjectsTaught}
                onChange={(e) => setTeacherForm({ ...teacherForm, subjectsTaught: e.target.value })}
                placeholder="Data Structures, Machine Learning, Operating Systems"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-white/10">
            <button
              onClick={() => setAccountType(null)}
              className="text-xs text-gray-400 hover:text-white"
            >
              &larr; Switch Account Type
            </button>
            <button
              onClick={handleSaveTeacher}
              disabled={loading}
              className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-sm shadow-lg shadow-indigo-500/20 transition"
            >
              Save Educator Profile & Enter Dashboard &rarr;
            </button>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* CASE C: PROFESSIONAL / OTHER PROFILE SETUP */}
      {/* ============================================================== */}
      {accountType === 'professional' && (
        <div className="glass-panel p-8 rounded-3xl border border-white/10 space-y-6">
          <div className="border-b border-white/10 pb-4">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <Briefcase className="w-6 h-6 text-emerald-400" /> Professional & Workspace Customization
            </h2>
            <p className="text-xs text-gray-400 mt-1">
              Select which platform modules you want enabled and configure your enterprise skills.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Full Name</label>
              <input
                type="text"
                value={professionalForm.name}
                onChange={(e) => setProfessionalForm({ ...professionalForm, name: e.target.value })}
                placeholder="e.g. Darshan Sharma"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Profession / Role</label>
              <input
                type="text"
                value={professionalForm.profession}
                onChange={(e) => setProfessionalForm({ ...professionalForm, profession: e.target.value })}
                placeholder="Senior AI Platform Engineer"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Organization / Enterprise</label>
              <input
                type="text"
                value={professionalForm.organization}
                onChange={(e) => setProfessionalForm({ ...professionalForm, organization: e.target.value })}
                placeholder="e.g. Nexora AI Labs"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Career & Engineering Goals</label>
              <input
                type="text"
                value={professionalForm.careerGoals}
                onChange={(e) => setProfessionalForm({ ...professionalForm, careerGoals: e.target.value })}
                placeholder="Architect autonomous enterprise workflows"
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          {/* Module Selector Toggles */}
          <div className="space-y-2 pt-2">
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Enabled Workspace Modules:</h4>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {[
                { id: 'research', label: 'AI Research Notebook' },
                { id: 'career', label: 'Career Roadmaps' },
                { id: 'study', label: 'Study System' },
                { id: 'creator', label: 'Creator Studio' },
                { id: 'planner', label: 'Planner & Tasks' },
                { id: 'knowledge_base', label: 'Knowledge Base' }
              ].map((m) => {
                const isChecked = professionalForm.enabledModules.includes(m.id);
                return (
                  <button
                    key={m.id}
                    onClick={() => {
                      if (isChecked) {
                        setProfessionalForm({
                          ...professionalForm,
                          enabledModules: professionalForm.enabledModules.filter(x => x !== m.id)
                        });
                      } else {
                        setProfessionalForm({
                          ...professionalForm,
                          enabledModules: [...professionalForm.enabledModules, m.id]
                        });
                      }
                    }}
                    className={`p-3 rounded-xl border text-xs text-left transition flex items-center justify-between ${
                      isChecked
                        ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 font-semibold'
                        : 'bg-dark-bg/40 border-white/10 text-gray-400 hover:border-white/20'
                    }`}
                  >
                    <span>{m.label}</span>
                    {isChecked && <Check className="w-3.5 h-3.5" />}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-white/10">
            <button
              onClick={() => setAccountType(null)}
              className="text-xs text-gray-400 hover:text-white"
            >
              &larr; Switch Account Type
            </button>
            <button
              onClick={handleSaveProfessional}
              disabled={loading}
              className="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-sm shadow-lg shadow-emerald-500/20 transition"
            >
              Save Profile & Launch Platform &rarr;
            </button>
          </div>
        </div>
      )}

    </div>
  );
}
