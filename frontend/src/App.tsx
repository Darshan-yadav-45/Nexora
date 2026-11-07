import { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import AuthModal from './components/AuthModal';
import Home from './pages/Home';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';
import Career from './pages/Career';
import Research from './pages/Research';
import Planner from './pages/Planner';
import KnowledgeBase from './pages/KnowledgeBase';
import Profile from './pages/Profile';

function App() {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [authModalOpen, setAuthModalOpen] = useState(false);

  useEffect(() => {
    const savedEmail = localStorage.getItem('userEmail');
    const token = localStorage.getItem('token');
    if (savedEmail && token) {
      setUserEmail(savedEmail);
    }
  }, []);

  const handleLoginSuccess = (email: string, isFirstTime: boolean) => {
    setUserEmail(email);
    setAuthModalOpen(false);
    if (isFirstTime) {
      navigate('/onboarding');
    } else {
      navigate('/dashboard');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('accountType');
    localStorage.removeItem('profileCompleted');
    setUserEmail(null);
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-dark-bg text-gray-100 flex flex-col selection:bg-primary-500/30">
      <Navbar
        userEmail={userEmail}
        onOpenAuth={() => setAuthModalOpen(true)}
        onLogout={handleLogout}
      />

      <main className="flex-1 w-full px-4 sm:px-6 lg:px-8 py-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/career" element={<Career />} />
          <Route path="/research" element={<Research />} />
          <Route path="/planner" element={<Planner />} />
          <Route path="/knowledge-base" element={<KnowledgeBase />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>

      <AuthModal
        isOpen={authModalOpen}
        onClose={() => setAuthModalOpen(false)}
        onSuccess={handleLoginSuccess}
      />
    </div>
  );
}

export default App;
