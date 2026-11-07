import { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Sparkles, Compass, Microscope, CheckSquare, BookMarked, 
  User as UserIcon, LogIn, LogOut, ChevronDown, Menu, X,
  GraduationCap, Settings
} from 'lucide-react';

interface NavbarProps {
  userEmail?: string | null;
  onOpenAuth?: () => void;
  onLogout?: () => void;
}

export default function Navbar({ userEmail, onOpenAuth, onLogout }: NavbarProps) {
  const location = useLocation();
  const [profileMenuOpen, setProfileMenuOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [accountType, setAccountType] = useState<string | null>(null);

  useEffect(() => {
    const at = localStorage.getItem('accountType');
    setAccountType(at);
  }, [userEmail, location.pathname]);

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard', icon: Sparkles },
    { name: 'Career Roadmaps', path: '/career', icon: Compass },
    { name: 'Research Notebooks', path: '/research', icon: Microscope },
    { name: 'Planner', path: '/planner', icon: CheckSquare },
    { name: 'Knowledge Base', path: '/knowledge-base', icon: BookMarked },
  ];

  return (
    <header className="w-full sticky top-0 z-50 bg-dark-bg/85 backdrop-blur-xl border-b border-white/10 px-4 lg:px-8 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <div className="relative">
            <div className="absolute -inset-1 bg-gradient-to-r from-primary-500 to-indigo-600 rounded-xl blur opacity-40 group-hover:opacity-75 transition duration-300" />
            <div className="relative bg-dark-card p-2 rounded-xl border border-white/10 text-primary-400">
              <Sparkles className="w-5 h-5 text-primary-400" />
            </div>
          </div>
          <div>
            <span className="text-xl font-bold tracking-tight text-white">
              Nexora <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-indigo-400">AI</span>
            </span>
            <span className="hidden sm:inline-block ml-2 text-xs font-semibold px-2 py-0.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20">
              v2.5
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-1 bg-dark-card/60 p-1 rounded-xl border border-white/5 backdrop-blur-md">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname.startsWith(link.path);
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-primary-600 to-indigo-600 text-white shadow-md shadow-primary-600/30'
                    : 'text-gray-300 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {link.name}
              </Link>
            );
          })}
        </nav>

        {/* Right Section: Account Pill / Sign In Button */}
        <div className="flex items-center gap-3">
          {userEmail ? (
            <div className="relative">
              <button
                onClick={() => setProfileMenuOpen(!profileMenuOpen)}
                className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-dark-card border border-white/10 text-xs text-gray-200 hover:border-white/20 transition-all shadow-sm"
              >
                <div className="w-6 h-6 rounded-full bg-primary-500/20 text-primary-400 flex items-center justify-center font-bold text-xs uppercase">
                  {userEmail[0]}
                </div>
                <div className="hidden sm:flex flex-col text-left">
                  <span className="max-w-[130px] truncate font-semibold text-white">{userEmail.split('@')[0]}</span>
                  {accountType && (
                    <span className="text-[10px] text-primary-400 capitalize">{accountType}</span>
                  )}
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-gray-400" />
              </button>

              {profileMenuOpen && (
                <div className="absolute right-0 mt-2 w-52 bg-dark-card border border-white/10 rounded-2xl shadow-2xl py-2 z-50 animate-in fade-in slide-in-from-top-2 glass-panel">
                  <Link
                    to="/profile"
                    onClick={() => setProfileMenuOpen(false)}
                    className="flex items-center gap-2.5 px-4 py-2 text-xs text-gray-300 hover:text-white hover:bg-white/5 font-medium"
                  >
                    <UserIcon className="w-4 h-4 text-primary-400" />
                    Profile & Connections
                  </Link>
                  <Link
                    to="/onboarding"
                    onClick={() => setProfileMenuOpen(false)}
                    className="flex items-center gap-2.5 px-4 py-2 text-xs text-gray-300 hover:text-white hover:bg-white/5 font-medium"
                  >
                    <GraduationCap className="w-4 h-4 text-indigo-400" />
                    Education Journey Setup
                  </Link>
                  <Link
                    to="/profile?tab=settings"
                    onClick={() => setProfileMenuOpen(false)}
                    className="flex items-center gap-2.5 px-4 py-2 text-xs text-gray-300 hover:text-white hover:bg-white/5 font-medium"
                  >
                    <Settings className="w-4 h-4 text-gray-400" />
                    Switch Role / Settings
                  </Link>
                  <div className="my-1 border-t border-white/10" />
                  <button
                    onClick={() => {
                      setProfileMenuOpen(false);
                      if (onLogout) onLogout();
                    }}
                    className="w-full flex items-center gap-2.5 px-4 py-2 text-xs text-red-400 hover:text-red-300 hover:bg-red-500/10 text-left font-medium"
                  >
                    <LogOut className="w-4 h-4" />
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-primary-600 to-indigo-600 hover:from-primary-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-primary-500/25 flex items-center gap-1.5 transition"
            >
              <LogIn className="w-3.5 h-3.5" />
              Sign In
            </button>
          )}

          {/* Mobile Menu Trigger */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 rounded-xl border border-white/10 text-gray-400 hover:text-white"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>

      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden pt-4 pb-2 border-t border-white/10 mt-3 space-y-1 animate-in fade-in">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname.startsWith(link.path);
            return (
              <Link
                key={link.path}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold ${
                  isActive ? 'bg-primary-600 text-white' : 'text-gray-300 hover:bg-white/5'
                }`}
              >
                <Icon className="w-4 h-4" />
                {link.name}
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}
