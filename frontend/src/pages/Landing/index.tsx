import React from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, FlaskConical, Code2, Briefcase, Video, Calendar, Database, ArrowRight, Sparkles } from 'lucide-react';

const Landing = () => {
  const modules = [
    { title: 'Study', icon: BookOpen, desc: 'Syllabus, PDF RAG, Notes & Quizzes', color: 'bg-blue-500/10 text-blue-400' },
    { title: 'Research', icon: FlaskConical, desc: 'Papers, Literature Matrix & Citations', color: 'bg-purple-500/10 text-purple-400' },
    { title: 'Projects', icon: Code2, desc: 'Architecture, Roadmap & Documentation', color: 'bg-emerald-500/10 text-emerald-400' },
    { title: 'Career', icon: Briefcase, desc: 'Resume, Interview Prep & Voice', color: 'bg-orange-500/10 text-orange-400' },
    { title: 'Creator', icon: Video, desc: 'Video Scripts, Timeline & Content', color: 'bg-rose-500/10 text-rose-400' },
    { title: 'Planner', icon: Calendar, desc: 'Tasks, Reminders & Timetable', color: 'bg-indigo-500/10 text-indigo-400' },
    { title: 'Knowledge Base', icon: Database, desc: 'Your unified personal AI memory', color: 'bg-amber-500/10 text-amber-400' },
  ];

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white selection:bg-blue-500/30 overflow-x-hidden font-sans">
      {/* Background gradients */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/20 blur-[120px]" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-600/20 blur-[120px]" />
      </div>

      {/* Header */}
      <header className="relative z-10 border-b border-white/5 bg-black/40 backdrop-blur-md sticky top-0">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-blue-400" />
            <span className="text-xl font-bold tracking-tight">Nexora AI</span>
          </div>
          
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
            <a href="#" className="hover:text-white transition-colors">Home</a>
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#about" className="hover:text-white transition-colors">About</a>
          </nav>

          <div className="flex items-center gap-4">
            <Link to="/login" className="text-sm font-medium hover:text-blue-400 transition-colors">
              Login
            </Link>
            <Link 
              to="/register" 
              className="px-5 py-2.5 text-sm font-medium rounded-full bg-blue-600 hover:bg-blue-500 transition-all shadow-[0_0_20px_rgba(37,99,235,0.4)]"
            >
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="relative z-10 max-w-7xl mx-auto px-6 pt-32 pb-24 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-sm text-gray-300 mb-8 backdrop-blur-sm">
          <Sparkles className="w-4 h-4 text-amber-400" />
          <span>Meet your new personal AI assistant</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 bg-gradient-to-br from-white via-white to-gray-500 bg-clip-text text-transparent">
          Your Personal <br className="hidden md:block" /> AI Workspace
        </h1>
        
        <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mx-auto mb-12 leading-relaxed">
          Study smarter. Research better. Build projects. Prepare for your career. Create content.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link 
            to="/register" 
            className="w-full sm:w-auto group flex items-center justify-center gap-2 px-8 py-4 rounded-full bg-white text-black font-semibold hover:bg-gray-200 transition-all"
          >
            Get Started
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link 
            to="/login" 
            className="w-full sm:w-auto px-8 py-4 rounded-full bg-white/5 border border-white/10 font-semibold hover:bg-white/10 transition-all backdrop-blur-sm"
          >
            Login to Workspace
          </Link>
        </div>

        {/* Modules Grid */}
        <div id="features" className="mt-32 pt-20 border-t border-white/5 text-left">
          <div className="mb-16 text-center">
            <h2 className="text-3xl font-bold mb-4">Everything you need in one place</h2>
            <p className="text-gray-400">Nexora AI seamlessly integrates all aspects of your academic and professional life.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {modules.map((mod, idx) => (
              <div 
                key={idx} 
                className="group relative p-6 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] hover:border-white/10 transition-all overflow-hidden"
              >
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-6 ${mod.color}`}>
                  <mod.icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{mod.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{mod.desc}</p>
                
                {/* Hover gradient effect */}
                <div className="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Landing;
