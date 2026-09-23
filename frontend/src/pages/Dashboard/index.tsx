import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { 
  LayoutDashboard, BookOpen, FlaskConical, Code2, Briefcase, 
  Video, Calendar, Database, Settings, LogOut, Bell, Search,
  Menu, X, Sparkles, Clock, CheckCircle2, ChevronRight
} from 'lucide-react';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    { name: 'Dashboard', icon: LayoutDashboard, path: '/dashboard', active: true },
    { name: 'Study', icon: BookOpen, path: '/study', active: false },
    { name: 'Research', icon: FlaskConical, path: '/research', active: false },
    { name: 'Projects', icon: Code2, path: '/projects', active: false },
    { name: 'Career', icon: Briefcase, path: '/career', active: false },
    { name: 'Creator', icon: Video, path: '/creator', active: false },
    { name: 'Planner', icon: Calendar, path: '/planner', active: false },
    { name: 'Knowledge Base', icon: Database, path: '/knowledge', active: false },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-black/80 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-[#111] border-r border-white/10 transition-transform duration-300 lg:static lg:translate-x-0 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="h-20 flex items-center px-6 border-b border-white/10">
          <Link to="/" className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-blue-400" />
            <span className="text-xl font-bold">Nexora AI</span>
          </Link>
          <button 
            className="ml-auto lg:hidden text-gray-400 hover:text-white"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="flex flex-col h-[calc(100%-5rem)] py-6 px-4 overflow-y-auto">
          <nav className="space-y-1 flex-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all ${
                  item.active 
                    ? 'bg-blue-600/10 text-blue-400 font-medium' 
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <item.icon className={`w-5 h-5 ${item.active ? 'text-blue-400' : 'text-gray-500'}`} />
                {item.name}
              </Link>
            ))}
          </nav>
          
          <div className="mt-8 space-y-1">
            <Link
              to="/profile"
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-all"
            >
              <Settings className="w-5 h-5 text-gray-500" />
              Settings
            </Link>
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-red-400/80 hover:text-red-400 hover:bg-red-400/10 transition-all text-left"
            >
              <LogOut className="w-5 h-5" />
              Logout
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        {/* Header */}
        <header className="h-20 flex items-center justify-between px-4 sm:px-8 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5 sticky top-0 z-30">
          <div className="flex items-center gap-4">
            <button 
              className="lg:hidden p-2 text-gray-400 hover:text-white rounded-lg hover:bg-white/5"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="w-5 h-5" />
            </button>
            <h1 className="text-xl font-semibold hidden sm:block">Welcome back, {user?.profile?.preferred_name || user?.profile?.first_name || user?.email?.split('@')[0]}</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="relative hidden md:block">
              <Search className="w-4 h-4 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input 
                type="text" 
                placeholder="Ask Nexora AI..." 
                className="w-64 pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-full text-sm text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
              />
            </div>
            <button className="p-2 text-gray-400 hover:text-white rounded-full hover:bg-white/5 relative">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-500 rounded-full"></span>
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center cursor-pointer border border-white/20">
              <span className="text-sm font-medium">{(user?.profile?.preferred_name || user?.profile?.first_name || user?.email || 'U')[0].toUpperCase()}</span>
            </div>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-8">
          <div className="max-w-7xl mx-auto space-y-8">
            
            {/* Action Banner */}
            <div className="relative rounded-2xl bg-gradient-to-r from-blue-900/40 to-purple-900/40 border border-blue-500/20 p-6 sm:p-8 overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/20 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/3" />
              
              <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div>
                  <h2 className="text-2xl font-bold mb-2">Ready to crush your goals today?</h2>
                  <p className="text-gray-300">You have 3 tasks due today and 1 upcoming deadline.</p>
                </div>
                <button className="px-6 py-3 bg-white text-black font-medium rounded-xl hover:bg-gray-100 transition-colors whitespace-nowrap shadow-[0_0_20px_rgba(255,255,255,0.2)]">
                  Open Planner
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Main Column */}
              <div className="lg:col-span-2 space-y-8">
                {/* Recent Activity */}
                <section>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold">Recent Activity</h3>
                    <button className="text-sm text-blue-400 hover:text-blue-300">View all</button>
                  </div>
                  
                  <div className="bg-[#111] border border-white/5 rounded-2xl p-2 shadow-xl">
                    {[
                      { title: 'Machine Learning Notes', type: 'Study', icon: BookOpen, time: '2 hours ago', color: 'text-blue-400', bg: 'bg-blue-500/10' },
                      { title: 'Resume v4 Draft', type: 'Career', icon: Briefcase, time: '5 hours ago', color: 'text-orange-400', bg: 'bg-orange-500/10' },
                      { title: 'Transformer Architecture Paper', type: 'Research', icon: FlaskConical, time: 'Yesterday', color: 'text-purple-400', bg: 'bg-purple-500/10' },
                    ].map((item, idx) => (
                      <div key={idx} className="flex items-center gap-4 p-4 rounded-xl hover:bg-white/5 cursor-pointer transition-colors group">
                        <div className={`p-3 rounded-lg ${item.bg} ${item.color}`}>
                          <item.icon className="w-5 h-5" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-medium text-white truncate">{item.title}</h4>
                          <p className="text-sm text-gray-500">{item.type}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-gray-500 mb-1">{item.time}</p>
                          <ChevronRight className="w-4 h-4 text-gray-600 group-hover:text-gray-300 ml-auto transition-colors" />
                        </div>
                      </div>
                    ))}
                  </div>
                </section>
              </div>

              {/* Sidebar Column */}
              <div className="space-y-8">
                {/* Up Next */}
                <section>
                  <h3 className="text-lg font-semibold mb-4">Up Next</h3>
                  <div className="bg-[#111] border border-white/5 rounded-2xl p-5 space-y-5 shadow-xl">
                    <div className="flex gap-4">
                      <div className="flex flex-col items-center min-w-[3rem]">
                        <span className="text-xs font-semibold text-blue-400 uppercase">Oct</span>
                        <span className="text-xl font-bold">12</span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-200">Data Structures Midterm</h4>
                        <p className="text-sm text-gray-500 mt-1 flex items-center gap-1"><Clock className="w-3 h-3" /> 10:00 AM</p>
                      </div>
                    </div>
                    
                    <div className="h-px bg-white/5" />
                    
                    <div className="flex gap-4">
                      <div className="flex flex-col items-center min-w-[3rem]">
                        <span className="text-xs font-semibold text-purple-400 uppercase">Oct</span>
                        <span className="text-xl font-bold">15</span>
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-200">Submit Research Draft</h4>
                        <p className="text-sm text-gray-500 mt-1 flex items-center gap-1"><Clock className="w-3 h-3" /> 11:59 PM</p>
                      </div>
                    </div>
                  </div>
                </section>

                {/* Quick Tasks */}
                <section>
                  <h3 className="text-lg font-semibold mb-4">Quick Tasks</h3>
                  <div className="bg-[#111] border border-white/5 rounded-2xl p-2 shadow-xl">
                    {['Review PR #42', 'Read chapter 5', 'Update LinkedIn profile'].map((task, idx) => (
                      <label key={idx} className="flex items-center gap-3 p-3 rounded-xl hover:bg-white/5 cursor-pointer transition-colors group">
                        <input type="checkbox" className="w-4 h-4 rounded border-gray-600 bg-transparent text-blue-500 focus:ring-0 focus:ring-offset-0 transition-colors" />
                        <span className="text-sm text-gray-400 group-hover:text-white transition-colors">{task}</span>
                      </label>
                    ))}
                  </div>
                </section>
              </div>
            </div>
            
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
