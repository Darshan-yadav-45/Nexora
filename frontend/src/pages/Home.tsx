import { Link } from 'react-router-dom';
import {
  Sparkles, Compass, Microscope, ArrowRight, BookOpen,
  GraduationCap, CheckCircle2, ShieldCheck, Zap,
  Layers, FileText
} from 'lucide-react';

const GithubIcon = ({ className }: { className?: string }) => (
  <svg className={className || "w-4 h-4"} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

export default function Home() {
  const token = localStorage.getItem('token');

  return (
    <div className="w-full max-w-7xl mx-auto py-8 md:py-16 space-y-24 animate-in fade-in duration-500">
      
      {/* ================================================================ */}
      {/* HERO SECTION */}
      {/* ================================================================ */}
      <div className="text-center space-y-6 max-w-4xl mx-auto pt-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20 text-xs font-bold uppercase tracking-wider shadow-inner">
          <Sparkles className="w-4 h-4" />
          The Unified AI Education & Academic Research Platform
        </div>

        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight text-white leading-tight">
          Pioneer Your Research. <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 via-indigo-400 to-purple-400">
            Master Your Career.
          </span>
        </h1>

        <p className="text-gray-300 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto">
          The premier platform uniting NotebookLM-style grounded AI research notebooks, dynamic student education profiles, complete expandable career roadmaps, and developer connections—all backed by PostgreSQL 17.
        </p>

        <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
          <Link
            to={token ? "/dashboard" : "/onboarding"}
            className="px-8 py-4 rounded-2xl bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-500 hover:to-indigo-500 text-white font-bold text-sm flex items-center gap-2.5 shadow-2xl shadow-primary-500/30 transition transform hover:-translate-y-0.5"
          >
            <Sparkles className="w-4 h-4" />
            {token ? "Go to Workspace Dashboard" : "Get Started — Free Account"}
            <ArrowRight className="w-4 h-4" />
          </Link>

          <Link
            to="/research"
            className="px-8 py-4 rounded-2xl bg-dark-card hover:bg-white/10 text-white font-bold text-sm flex items-center gap-2.5 border border-white/10 transition transform hover:-translate-y-0.5"
          >
            <Microscope className="w-4 h-4 text-purple-400" />
            Explore Research Notebooks
          </Link>
        </div>

        {/* Feature Badges */}
        <div className="flex flex-wrap justify-center items-center gap-6 pt-6 text-xs text-gray-400">
          <span className="flex items-center gap-1.5"><ShieldCheck className="w-4 h-4 text-emerald-400" /> PostgreSQL Persistence</span>
          <span className="flex items-center gap-1.5"><Zap className="w-4 h-4 text-amber-400" /> NotebookLM Grounded Citations</span>
          <span className="flex items-center gap-1.5"><Layers className="w-4 h-4 text-indigo-400" /> Dynamic Education Journey</span>
          <span className="flex items-center gap-1.5"><GithubIcon className="w-4 h-4 text-white" /> GitHub & Social Sync</span>
        </div>
      </div>

      {/* ================================================================ */}
      {/* INTERACTIVE PRODUCT PREVIEW SHOWCASE */}
      {/* ================================================================ */}
      <div className="relative rounded-3xl p-1 bg-gradient-to-b from-primary-500/30 via-indigo-500/10 to-transparent shadow-2xl">
        <div className="bg-dark-card/90 rounded-[22px] p-6 sm:p-10 border border-white/10 backdrop-blur-xl space-y-6">
          <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-white/10 pb-4">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-red-500/80" />
              <div className="w-3 h-3 rounded-full bg-amber-500/80" />
              <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
              <span className="text-xs text-gray-400 font-mono ml-2">nexora.ai/workspace/research-notebook</span>
            </div>
            <div className="text-xs text-emerald-400 font-semibold flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Source Grounded &bull; Zero Hallucination
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
            {/* Panel 1 Preview: Sources */}
            <div className="p-4 rounded-2xl bg-dark-bg/80 border border-white/10 space-y-3">
              <div className="font-bold text-white flex items-center gap-2">
                <FileText className="w-4 h-4 text-primary-400" /> Sources Panel
              </div>
              <p className="text-gray-400 text-[11px]">Multi-format reference uploads: PDF, DOCX, TXT, or web URLs with page preservation.</p>
              <div className="space-y-1.5">
                <div className="p-2 rounded-lg bg-white/5 text-gray-300">📄 Attention Is All You Need.pdf (15 p.)</div>
                <div className="p-2 rounded-lg bg-white/5 text-gray-300">📄 ResNet Clinical Imaging.pdf (12 p.)</div>
              </div>
            </div>

            {/* Panel 2 Preview: Chat */}
            <div className="p-4 rounded-2xl bg-dark-bg/80 border border-white/10 space-y-3">
              <div className="font-bold text-white flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-indigo-400" /> AI Grounded Assistant
              </div>
              <p className="text-gray-400 text-[11px]">Strictly source-grounded answers with inline citation tags and direct page quotes.</p>
              <div className="p-3 rounded-xl bg-primary-500/10 border border-primary-500/20 text-gray-200 text-[11px] leading-relaxed">
                "According to <strong className="text-primary-300">[1] ResNet Paper, p. 3</strong>, the architecture achieves 98.4% diagnostic accuracy while reducing false negatives."
              </div>
            </div>

            {/* Panel 3 Preview: Studio */}
            <div className="p-4 rounded-2xl bg-dark-bg/80 border border-white/10 space-y-3">
              <div className="font-bold text-white flex items-center gap-2">
                <Compass className="w-4 h-4 text-purple-400" /> Studio & Humanizer
              </div>
              <p className="text-gray-400 text-[11px]">20 AI generators (Summaries, Gaps, Methodology, Podcast Scripts) & Writing Humanizer.</p>
              <div className="flex flex-wrap gap-1.5">
                <span className="px-2 py-1 rounded bg-white/5 text-gray-300">Summary</span>
                <span className="px-2 py-1 rounded bg-white/5 text-gray-300">Gaps</span>
                <span className="px-2 py-1 rounded bg-white/5 text-gray-300">Viva Voce</span>
                <span className="px-2 py-1 rounded bg-white/5 text-gray-300">Humanize</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ================================================================ */}
      {/* COMPLETE FEATURE HIGHLIGHTS */}
      {/* ================================================================ */}
      <div className="space-y-12">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-extrabold text-white">Engineered For Students, Educators & Professionals</h2>
          <p className="text-gray-400 text-sm max-w-xl mx-auto">
            Discover a purpose-built workspace engineered for academic rigor and career mastery.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Feature 1: AI Research Notebook */}
          <div className="p-6 rounded-3xl bg-dark-card border border-white/10 glass-panel space-y-4 hover:border-primary-500/40 transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-primary-500/10 text-primary-400 border border-primary-500/20 flex items-center justify-center mb-4">
                <Microscope className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">AI Research Notebook (NotebookLM)</h3>
              <p className="text-xs text-gray-400 leading-relaxed mt-1">
                Create a notebook using only a title. Ingest PDFs, DOCX, and TXT files. AI chat answers strictly grounded in your references with exact page citations and clickable quotes.
              </p>
            </div>
            <Link to="/research" className="text-xs text-primary-400 font-bold hover:underline flex items-center gap-1 pt-4 border-t border-white/5">
              Launch Research Studio &rarr;
            </Link>
          </div>

          {/* Feature 2: Dynamic Education Profile */}
          <div className="p-6 rounded-3xl bg-dark-card border border-white/10 glass-panel space-y-4 hover:border-indigo-500/40 transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center justify-center mb-4">
                <GraduationCap className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Dynamic Education Profile</h3>
              <p className="text-xs text-gray-400 leading-relaxed mt-1">
                Step-by-step qualification tracking: SSLC, PUC, Diploma, UG, PG, PhD. Dynamic questions adapt whether you are completed or ongoing, attaching course syllabi and lecture notes.
              </p>
            </div>
            <Link to="/onboarding" className="text-xs text-indigo-400 font-bold hover:underline flex items-center gap-1 pt-4 border-t border-white/5">
              Setup Education Journey &rarr;
            </Link>
          </div>

          {/* Feature 3: Career Roadmaps */}
          <div className="p-6 rounded-3xl bg-dark-card border border-white/10 glass-panel space-y-4 hover:border-purple-500/40 transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-purple-500/10 text-purple-400 border border-purple-500/20 flex items-center justify-center mb-4">
                <Compass className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Complete Career Roadmaps</h3>
              <p className="text-xs text-gray-400 leading-relaxed mt-1">
                Full-stack tracks for Java, Python, and Data Analysis. Every single topic contains all 17 master learning sections: notes, syntax, code examples, MCQs, and mini-projects.
              </p>
            </div>
            <Link to="/career" className="text-xs text-purple-400 font-bold hover:underline flex items-center gap-1 pt-4 border-t border-white/5">
              Browse Full Curricula &rarr;
            </Link>
          </div>

          {/* Feature 4: Writing Humanizer & Diff Review */}
          <div className="p-6 rounded-3xl bg-dark-card border border-white/10 glass-panel space-y-4 hover:border-emerald-500/40 transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center justify-center mb-4">
                <FileText className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Humanize & Improve Writing</h3>
              <p className="text-xs text-gray-400 leading-relaxed mt-1">
                Transform rough drafts into clear, natural, or publication-grade academic prose with 7 specialized modes while strictly keeping all factual findings, data, and citations.
              </p>
            </div>
            <Link to="/research" className="text-xs text-emerald-400 font-bold hover:underline flex items-center gap-1 pt-4 border-t border-white/5">
              Try Writing Humanizer &rarr;
            </Link>
          </div>

          {/* Feature 5: Teacher Pedagogical Studio */}
          <div className="p-6 rounded-3xl bg-dark-card border border-white/10 glass-panel space-y-4 hover:border-amber-500/40 transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-amber-500/10 text-amber-400 border border-amber-500/20 flex items-center justify-center mb-4">
                <BookOpen className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Teacher & Educator Studio</h3>
              <p className="text-xs text-gray-400 leading-relaxed mt-1">
                Faculty tools for 60-minute lesson plans, diagnostic MCQ generation, viva voce defense question sets, and student learning resource packs.
              </p>
            </div>
            <Link to="/onboarding" className="text-xs text-amber-400 font-bold hover:underline flex items-center gap-1 pt-4 border-t border-white/5">
              Configure Educator Tools &rarr;
            </Link>
          </div>

          {/* Feature 6: Social & Developer Connections */}
          <div className="p-6 rounded-3xl bg-dark-card border border-white/10 glass-panel space-y-4 hover:border-pink-500/40 transition flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-pink-500/10 text-pink-400 border border-pink-500/20 flex items-center justify-center mb-4">
                <GithubIcon className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white">Developer Accounts & Profile Links</h3>
              <p className="text-xs text-gray-400 leading-relaxed mt-1">
                Connect GitHub to sync public repositories into your career profile, or link LinkedIn, Instagram, X (Twitter), and YouTube with privacy visibility toggles.
              </p>
            </div>
            <Link to="/profile" className="text-xs text-pink-400 font-bold hover:underline flex items-center gap-1 pt-4 border-t border-white/5">
              Connect Your Accounts &rarr;
            </Link>
          </div>

        </div>
      </div>

      {/* ================================================================ */}
      {/* HOW IT WORKS (4 STEPS) */}
      {/* ================================================================ */}
      <div className="glass-panel p-8 sm:p-12 rounded-3xl border border-white/10 space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold uppercase text-primary-400 tracking-wider">Streamlined Methodology</span>
          <h2 className="text-3xl font-extrabold text-white">How Nexora AI Works</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            {
              step: '01',
              title: 'Role & Profile Setup',
              desc: 'Select Student, Teacher, or Professional. Build your dynamic qualifications journey or enter teaching subjects.'
            },
            {
              step: '02',
              title: 'Create AI Notebooks',
              desc: 'Enter your research title. Ingest PDFs and notes with page-level chunking and zero hallucination risk.'
            },
            {
              step: '03',
              title: 'Master Roadmaps',
              desc: 'Progress through complete Java, Python, and Data tracks with 17 structured components per topic.'
            },
            {
              step: '04',
              title: 'Sync & Persist',
              desc: 'Convert tasks to the Planner, save research notes to the Knowledge Base, and export to Markdown/CSV.'
            }
          ].map((s, idx) => (
            <div key={idx} className="p-5 rounded-2xl bg-dark-bg/60 border border-white/5 space-y-2 relative">
              <span className="text-3xl font-black text-white/20">{s.step}</span>
              <h3 className="text-sm font-bold text-white">{s.title}</h3>
              <p className="text-xs text-gray-400 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* ================================================================ */}
      {/* MODERN FOOTER */}
      {/* ================================================================ */}
      <footer className="border-t border-white/10 pt-12 pb-8 text-xs text-gray-500 space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-lg bg-primary-600 flex items-center justify-center text-white font-bold text-xs">
              N
            </div>
            <span className="font-bold text-white text-sm">Nexora AI Platform</span>
          </div>

          <div className="flex flex-wrap gap-6 text-gray-400">
            <Link to="/career" className="hover:text-white transition">Career Roadmaps</Link>
            <Link to="/research" className="hover:text-white transition">Research Notebooks</Link>
            <Link to="/planner" className="hover:text-white transition">Planner</Link>
            <Link to="/knowledge-base" className="hover:text-white transition">Knowledge Base</Link>
            <Link to="/profile" className="hover:text-white transition">Profile Settings</Link>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-center gap-2 pt-4 border-t border-white/5 text-[11px]">
          <p>© 2026 Nexora AI Inc. All rights reserved. Persistent PostgreSQL Architecture.</p>
          <div className="flex gap-4">
            <span className="hover:text-gray-400 cursor-pointer">Privacy Policy</span>
            <span className="hover:text-gray-400 cursor-pointer">Terms of Service</span>
            <span className="hover:text-gray-400 cursor-pointer">Documentation</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
