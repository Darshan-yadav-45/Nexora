import React, { useState, useEffect } from 'react';
import {
  User, GraduationCap, BookOpen, Briefcase, Link2, Settings,
  CheckCircle2, Eye, EyeOff, Trash2,
  ExternalLink, Check, AlertCircle
} from 'lucide-react';
import api from '../services/api';

const GithubIcon = ({ className }: { className?: string }) => (
  <svg className={className || "w-4 h-4"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

const LinkedinIcon = ({ className }: { className?: string }) => (
  <svg className={className || "w-4 h-4"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z" />
    <rect x="2" y="9" width="4" height="12" />
    <circle cx="4" cy="4" r="2" />
  </svg>
);

const TwitterIcon = ({ className }: { className?: string }) => (
  <svg className={className || "w-4 h-4"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 4l11.733 16h4.267l-11.733 -16z" />
    <path d="M4 20l6.768 -6.768m2.46 -2.46l6.772 -6.772" />
  </svg>
);

const YoutubeIcon = ({ className }: { className?: string }) => (
  <svg className={className || "w-4 h-4"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z" />
    <polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02" fill="currentColor" />
  </svg>
);

const InstagramIcon = ({ className }: { className?: string }) => (
  <svg className={className || "w-4 h-4"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="2" y="2" width="20" height="20" rx="5" ry="5" />
    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
    <line x1="17.5" y1="6.5" x2="17.51" y2="6.5" />
  </svg>
);

export default function Profile() {
  const [activeTab, setActiveTab] = useState<
    'personal' | 'education' | 'subjects' | 'career' | 'resume' | 'social' | 'settings'
  >('personal');

  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Profile data state
  const [personalInfo, setPersonalInfo] = useState<any>({
    full_name: '',
    preferred_name: '',
    email: '',
    phone_number: '',
    date_of_birth: '',
    country: 'India',
    state: '',
    city: '',
    preferred_language: 'English'
  });

  const [educationRecords, setEducationRecords] = useState<any[]>([]);
  const [subjects, setSubjects] = useState<any[]>([]);
  const [careerInfo, setCareerInfo] = useState<any>({
    career_goal: '',
    preferred_career_path: '',
    current_skills: [],
    technologies_interested: []
  });

  // Social accounts state
  const [socialAccounts, setSocialAccounts] = useState<any[]>([]);
  const [githubUsername, setGithubUsername] = useState('');
  const [linkPlatform, setLinkPlatform] = useState('linkedin');
  const [linkUrl, setLinkUrl] = useState('');
  const [customPlatformName, setCustomPlatformName] = useState('');

  // Account Type Setting
  const [currentAccountType, setCurrentAccountType] = useState<string>('student');

  useEffect(() => {
    fetchProfileData();
  }, [activeTab]);

  const fetchProfileData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'personal') {
        const res = await api.get('/education/personal-info');
        setPersonalInfo(res.data);
      } else if (activeTab === 'education') {
        const res = await api.get('/education/records');
        setEducationRecords(res.data);
      } else if (activeTab === 'subjects') {
        const res = await api.get('/education/subjects');
        setSubjects(res.data);
      } else if (activeTab === 'career') {
        const res = await api.get('/education/career-info');
        setCareerInfo(res.data);
      } else if (activeTab === 'social') {
        const res = await api.get('/social/accounts');
        setSocialAccounts(res.data);
      } else if (activeTab === 'settings') {
        const res = await api.get('/auth/status');
        setCurrentAccountType(res.data.account_type || 'student');
      }
    } catch (err: any) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Update Personal Info ---
  const handleUpdatePersonalInfo = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setSuccessMsg(null);
    try {
      await api.post('/education/personal-info', {
        name: personalInfo.full_name,
        preferred_name: personalInfo.preferred_name,
        email: personalInfo.email,
        phone_number: personalInfo.phone_number,
        date_of_birth: personalInfo.date_of_birth,
        country: personalInfo.country,
        state: personalInfo.state,
        city: personalInfo.city,
        preferred_language: personalInfo.preferred_language
      });
      setSuccessMsg('Personal information updated successfully.');
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to update personal information');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Connect GitHub ---
  const handleConnectGithub = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!githubUsername.trim()) return;
    setLoading(true);
    setSuccessMsg(null);
    try {
      await api.post('/social/connect-github', { username: githubUsername });
      setSuccessMsg(`GitHub account @${githubUsername} connected.`);
      setGithubUsername('');
      fetchProfileData();
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to connect GitHub');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Add Social Profile Link ---
  const handleAddProfileLink = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!linkUrl.trim()) return;
    setLoading(true);
    setSuccessMsg(null);
    try {
      await api.post('/social/add-profile-link', {
        platform: linkPlatform,
        profile_url: linkUrl,
        custom_platform_name: linkPlatform === 'other' ? customPlatformName : undefined
      });
      setSuccessMsg(`${linkPlatform.toUpperCase()} profile link added.`);
      setLinkUrl('');
      setCustomPlatformName('');
      fetchProfileData();
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to add profile link');
    } finally {
      setLoading(false);
    }
  };

  // --- Handlers: Disconnect Account ---
  const handleDisconnectSocial = async (accountId: string) => {
    try {
      await api.delete(`/social/disconnect/${accountId}`);
      setSocialAccounts(socialAccounts.filter(a => a.id !== accountId));
      setSuccessMsg('Account disconnected successfully.');
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to disconnect account');
    }
  };

  // --- Handlers: Toggle Visibility ---
  const handleToggleVisibility = async (accountId: string, currentVal: boolean) => {
    try {
      await api.put(`/social/visibility/${accountId}?show=${!currentVal}`);
      setSocialAccounts(socialAccounts.map(a => a.id === accountId ? { ...a, show_on_public_profile: !currentVal } : a));
    } catch (err: any) {
      console.error(err);
    }
  };

  // --- Handlers: Switch Account Type (without losing data) ---
  const handleSwitchAccountType = async (newType: string) => {
    setLoading(true);
    setSuccessMsg(null);
    try {
      await api.post('/auth/select-account-type', { account_type: newType });
      setCurrentAccountType(newType);
      localStorage.setItem('accountType', newType);
      setSuccessMsg(`Account role updated to ${newType.toUpperCase()}. Previous data preserved.`);
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to switch account type');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6 animate-in fade-in duration-300">
      
      {/* Profile Header */}
      <div className="glass-panel p-6 rounded-3xl border border-white/10 flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-primary-600 to-indigo-600 flex items-center justify-center text-white text-2xl font-bold shadow-xl shadow-primary-500/25">
            {personalInfo.full_name?.charAt(0) || 'U'}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">{personalInfo.full_name || 'Nexora Scholar'}</h1>
            <p className="text-xs text-gray-400 mt-0.5">{personalInfo.email}</p>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20 capitalize">
                Role: {currentAccountType}
              </span>
              <span className="text-[11px] text-emerald-400 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" /> Persistent in PostgreSQL
              </span>
            </div>
          </div>
        </div>
      </div>

      {successMsg && (
        <div className="p-3.5 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center gap-2">
          <Check className="w-4 h-4 text-emerald-400" />
          <span>{successMsg}</span>
        </div>
      )}

      {errorMsg && (
        <div className="p-3.5 rounded-2xl bg-red-500/10 border border-red-500/20 text-red-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-400" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Profile Tabs Navigation */}
      <div className="flex overflow-x-auto gap-2 border-b border-white/10 pb-2 text-xs font-semibold">
        {[
          { id: 'personal', label: 'Personal Information', icon: User },
          { id: 'education', label: 'Education & Qualifications', icon: GraduationCap },
          { id: 'subjects', label: 'Subjects & Syllabi', icon: BookOpen },
          { id: 'career', label: 'Skills & Career Goals', icon: Briefcase },
          { id: 'social', label: 'Connected Accounts', icon: Link2 },
          { id: 'settings', label: 'Account Settings', icon: Settings }
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-2.5 rounded-xl transition flex items-center gap-2 whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-primary-500/20 border border-primary-500 text-primary-300 shadow-sm'
                  : 'bg-dark-bg/40 border border-white/5 text-gray-400 hover:text-white hover:border-white/20'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* ============================================================== */}
      {/* TAB 1: PERSONAL INFORMATION */}
      {/* ============================================================== */}
      {activeTab === 'personal' && (
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <User className="w-5 h-5 text-primary-400" /> Personal Information
          </h2>

          <form onSubmit={handleUpdatePersonalInfo} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Full Name</label>
              <input
                type="text"
                value={personalInfo.full_name}
                onChange={(e) => setPersonalInfo({ ...personalInfo, full_name: e.target.value })}
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Preferred Name</label>
              <input
                type="text"
                value={personalInfo.preferred_name}
                onChange={(e) => setPersonalInfo({ ...personalInfo, preferred_name: e.target.value })}
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Phone Number</label>
              <input
                type="text"
                value={personalInfo.phone_number || ''}
                onChange={(e) => setPersonalInfo({ ...personalInfo, phone_number: e.target.value })}
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Date of Birth</label>
              <input
                type="date"
                value={personalInfo.date_of_birth || ''}
                onChange={(e) => setPersonalInfo({ ...personalInfo, date_of_birth: e.target.value })}
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">Country</label>
              <input
                type="text"
                value={personalInfo.country || 'India'}
                onChange={(e) => setPersonalInfo({ ...personalInfo, country: e.target.value })}
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-300 mb-1">City</label>
              <input
                type="text"
                value={personalInfo.city || ''}
                onChange={(e) => setPersonalInfo({ ...personalInfo, city: e.target.value })}
                className="w-full bg-dark-bg/60 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>

            <div className="sm:col-span-2 flex justify-end pt-2">
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-2.5 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs shadow-lg shadow-primary-500/20 transition"
              >
                Save Changes
              </button>
            </div>
          </form>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 2: EDUCATION RECORDS */}
      {/* ============================================================== */}
      {activeTab === 'education' && (
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <GraduationCap className="w-5 h-5 text-primary-400" /> Education Qualifications ({educationRecords.length})
          </h2>

          {educationRecords.length === 0 ? (
            <p className="text-xs text-gray-400">No education qualifications recorded yet.</p>
          ) : (
            <div className="space-y-3">
              {educationRecords.map((r) => (
                <div key={r.id} className="p-4 rounded-2xl bg-dark-bg/60 border border-white/10 flex justify-between items-center text-xs">
                  <div>
                    <span className="font-bold text-white text-sm">{r.level}</span> — <span className="text-primary-300 font-semibold">{r.status}</span>
                    <div className="text-gray-300 mt-1">{r.institution_name} {r.degree_name ? `(${r.degree_name})` : ''}</div>
                    <div className="text-gray-500 mt-0.5">
                      {r.board_or_university ? `Board/Univ: ${r.board_or_university}` : ''} {r.result_percentage_cgpa ? `| Result: ${r.result_percentage_cgpa}` : ''}
                    </div>
                  </div>
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 3: SUBJECTS & SYLLABI */}
      {/* ============================================================== */}
      {activeTab === 'subjects' && (
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-primary-400" /> Active Coursework & Syllabi ({subjects.length})
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {subjects.map((s) => (
              <div key={s.id} className="p-4 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-2 text-xs">
                <div className="flex justify-between items-start">
                  <span className="font-bold text-white text-sm">{s.name}</span>
                  {s.code && <span className="px-2 py-0.5 rounded bg-primary-500/10 text-primary-400 font-semibold">{s.code}</span>}
                </div>
                <p className="text-gray-400">{s.description || 'Semester course module'}</p>
                <div className="text-primary-300 pt-1">
                  Syllabus documents attached: <strong>{s.syllabi_count || 0}</strong>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 4: SKILLS & CAREER GOALS */}
      {/* ============================================================== */}
      {activeTab === 'career' && (
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-primary-400" /> Career Profile & Technologies
          </h2>

          <div className="p-4 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-3 text-xs">
            <div>
              <span className="text-gray-400 font-semibold uppercase tracking-wider">Target Goal:</span>
              <p className="text-sm font-bold text-white mt-0.5">{careerInfo.career_goal || 'Full Stack AI Engineer'}</p>
            </div>
            <div>
              <span className="text-gray-400 font-semibold uppercase tracking-wider">Active Career Track:</span>
              <p className="text-sm text-primary-300 font-semibold mt-0.5">{careerInfo.preferred_career_path}</p>
            </div>
            <div>
              <span className="text-gray-400 font-semibold uppercase tracking-wider">Verified Skills:</span>
              <div className="flex flex-wrap gap-1.5 mt-1.5">
                {(careerInfo.current_skills || ['Python', 'SQL', 'Git']).map((sk: string, i: number) => (
                  <span key={i} className="px-2.5 py-1 rounded-lg bg-primary-500/10 text-primary-300 border border-primary-500/20 text-xs">
                    {sk}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 5: CONNECTED ACCOUNTS (GitHub, LinkedIn, Instagram, X, YouTube) */}
      {/* ============================================================== */}
      {activeTab === 'social' && (
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
          <div className="border-b border-white/10 pb-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Link2 className="w-5 h-5 text-primary-400" /> Connected Accounts & Developer Profiles
            </h2>
            <p className="text-xs text-gray-400 mt-1">
              Connect your GitHub to import public repositories into your career profile, or link your LinkedIn, Instagram, X (Twitter), and YouTube.
            </p>
          </div>

          {/* Connect GitHub Section */}
          <div className="p-5 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-3 rounded-xl bg-white/5 text-white">
                <GithubIcon className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">GitHub Account Integration</h3>
                <p className="text-xs text-gray-400">Sync public repositories, star counts, and primary languages into your Career Profile.</p>
              </div>
            </div>

            <form onSubmit={handleConnectGithub} className="flex gap-2">
              <input
                type="text"
                value={githubUsername}
                onChange={(e) => setGithubUsername(e.target.value)}
                placeholder="Enter GitHub username (e.g. torvalds)"
                className="flex-1 bg-dark-bg/80 border border-white/10 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <button
                type="submit"
                disabled={loading || !githubUsername.trim()}
                className="px-5 py-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white font-bold text-xs transition"
              >
                Connect GitHub
              </button>
            </form>
          </div>

          {/* Add Other Social Platforms */}
          <div className="p-5 rounded-2xl bg-dark-bg/60 border border-white/10 space-y-4">
            <h3 className="text-sm font-bold text-white">Add Social / Profile Links</h3>
            <p className="text-xs text-gray-400">Add verified profile links. These can be toggled to show or hide on your Nexora public profile.</p>

            <form onSubmit={handleAddProfileLink} className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <select
                value={linkPlatform}
                onChange={(e) => setLinkPlatform(e.target.value)}
                className="bg-dark-bg/80 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="linkedin">LinkedIn</option>
                <option value="instagram">Instagram</option>
                <option value="twitter">X (Twitter)</option>
                <option value="youtube">YouTube</option>
                <option value="other">Other Platform</option>
              </select>

              {linkPlatform === 'other' ? (
                <input
                  type="text"
                  value={customPlatformName}
                  onChange={(e) => setCustomPlatformName(e.target.value)}
                  placeholder="Platform Name (e.g. Kaggle)"
                  className="bg-dark-bg/80 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              ) : null}

              <input
                type="url"
                required
                value={linkUrl}
                onChange={(e) => setLinkUrl(e.target.value)}
                placeholder="Profile URL (e.g. https://linkedin.com/in/...)"
                className="bg-dark-bg/80 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-primary-500"
              />

              <div className="sm:col-span-3 flex justify-end">
                <button
                  type="submit"
                  disabled={loading || !linkUrl.trim()}
                  className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs transition"
                >
                  Save Profile Link
                </button>
              </div>
            </form>
          </div>

          {/* List of Connected Accounts */}
          <div className="space-y-3">
            <h4 className="text-xs font-semibold text-gray-300 uppercase tracking-wider">Your Connected Accounts ({socialAccounts.length}):</h4>
            {socialAccounts.length === 0 ? (
              <p className="text-xs text-gray-500 italic p-4 text-center border border-dashed border-white/10 rounded-xl">
                No external accounts connected yet.
              </p>
            ) : (
              <div className="space-y-2">
                {socialAccounts.map((acc) => (
                  <div key={acc.id} className="p-4 rounded-2xl bg-dark-bg/80 border border-white/10 flex flex-col sm:flex-row justify-between sm:items-center gap-3">
                    <div className="flex items-center gap-3">
                      <div className="p-2.5 rounded-xl bg-white/5 text-primary-400">
                        {acc.platform === 'github' && <GithubIcon className="w-5 h-5" />}
                        {acc.platform === 'linkedin' && <LinkedinIcon className="w-5 h-5" />}
                        {acc.platform === 'twitter' && <TwitterIcon className="w-5 h-5" />}
                        {acc.platform === 'youtube' && <YoutubeIcon className="w-5 h-5" />}
                        {acc.platform === 'instagram' && <InstagramIcon className="w-5 h-5" />}
                        {acc.platform === 'other' && <Link2 className="w-5 h-5" />}
                      </div>

                      <div>
                        <div className="font-bold text-white text-xs flex items-center gap-2">
                          <span className="capitalize">{acc.platform}</span>
                          <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                            acc.is_connected ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-primary-500/10 text-primary-400 border border-primary-500/20'
                          }`}>
                            {acc.is_connected ? 'Connected' : 'Profile Link Added'}
                          </span>
                        </div>
                        <a
                          href={acc.profile_url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-xs text-primary-400 hover:underline flex items-center gap-1 mt-0.5"
                        >
                          {acc.profile_url} <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleToggleVisibility(acc.id, acc.show_on_public_profile)}
                        className="px-3 py-1.5 rounded-xl border border-white/10 bg-dark-bg/60 text-xs text-gray-300 hover:text-white flex items-center gap-1.5 transition"
                      >
                        {acc.show_on_public_profile ? <Eye className="w-3.5 h-3.5 text-emerald-400" /> : <EyeOff className="w-3.5 h-3.5 text-gray-500" />}
                        {acc.show_on_public_profile ? 'Public' : 'Hidden'}
                      </button>

                      <button
                        onClick={() => handleDisconnectSocial(acc.id)}
                        className="p-2 rounded-xl border border-white/10 text-gray-400 hover:text-red-400 hover:bg-white/5 transition"
                        title="Disconnect"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}

      {/* ============================================================== */}
      {/* TAB 6: ACCOUNT SETTINGS (Switch Role without losing data) */}
      {/* ============================================================== */}
      {activeTab === 'settings' && (
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-6">
          <div className="border-b border-white/10 pb-4">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Settings className="w-5 h-5 text-primary-400" /> Account Settings & Role Transition
            </h2>
            <p className="text-xs text-gray-400 mt-1">
              Switch your primary Nexora AI role anytime. All your research notebooks, education qualifications, and career roadmaps remain persistently stored in PostgreSQL.
            </p>
          </div>

          <div className="space-y-3">
            <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider">
              Change Account Role:
            </label>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {[
                { id: 'student', label: 'Student / Scholar', desc: 'Semester subjects & roadmaps' },
                { id: 'teacher', label: 'Teacher / Educator', desc: 'Lesson plans & pedagogical AI' },
                { id: 'professional', label: 'Other / Professional', desc: 'Research & modular workspace' }
              ].map((role) => (
                <button
                  key={role.id}
                  onClick={() => handleSwitchAccountType(role.id)}
                  className={`p-4 rounded-2xl border text-left transition flex flex-col justify-between ${
                    currentAccountType === role.id
                      ? 'bg-primary-500/20 border-primary-500 text-white font-bold'
                      : 'bg-dark-bg/60 border-white/10 text-gray-400 hover:border-white/20'
                  }`}
                >
                  <span className="text-sm">{role.label}</span>
                  <span className="text-xs text-gray-400 mt-1 font-normal">{role.desc}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
