import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Landing from './pages/Landing';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import VerifyEmail from './pages/Auth/VerifyEmail';
import ForgotPassword from './pages/Auth/ForgotPassword';
import ResetPassword from './pages/Auth/ResetPassword';
import ProfileSetup from './pages/Onboarding/ProfileSetup';
import Dashboard from './pages/Dashboard';
import MyInformation from './pages/Profile/MyInformation';
import Security from './pages/Settings/Security';
import ResearchWorkspace from './pages/Research/ResearchWorkspace';
import ProjectDetails from './pages/Research/ProjectDetails';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { user, loading } = useAuth();
  
  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">Loading...</div>;
  }
  
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  
  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/verify-email" element={<VerifyEmail />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />

          <Route path="/onboarding" element={<ProtectedRoute><ProfileSetup /></ProtectedRoute>} />
          <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><MyInformation /></ProtectedRoute>} />
          <Route path="/settings/security" element={<ProtectedRoute><Security /></ProtectedRoute>} />
          
          {/* Research Module */}
          <Route path="/research" element={<ProtectedRoute><ResearchWorkspace /></ProtectedRoute>} />
          <Route path="/research/:projectId" element={<ProtectedRoute><ProjectDetails /></ProtectedRoute>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;

