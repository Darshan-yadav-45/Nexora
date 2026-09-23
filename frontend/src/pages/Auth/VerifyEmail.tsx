import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Mail, ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';
import api from '../../services/api';

const VerifyEmail = () => {
  const location = useLocation();
  const [email] = useState(location.state?.email || '');
  const [verifying, setVerifying] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleVerify = async () => {
    setVerifying(true);
    try {
      // In a real app, this would get a token from the URL
      await api.post('/auth/verify-email', null, { params: { token: 'mock-token' } });
      setSuccess(true);
    } catch (err) {
      console.error(err);
    } finally {
      setVerifying(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans relative overflow-hidden">
      <div className="absolute top-[-20%] left-[20%] w-[40%] h-[40%] rounded-full bg-blue-600/10 blur-[120px] pointer-events-none" />
      
      <div className="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <Link to="/" className="flex justify-center items-center gap-2 mb-8 group">
          <Sparkles className="w-8 h-8 text-blue-400 group-hover:text-blue-300 transition-colors" />
          <span className="text-3xl font-bold tracking-tight">Nexora AI</span>
        </Link>
        <h2 className="text-center text-2xl font-bold tracking-tight text-white mb-2">
          Verify your email
        </h2>
        <p className="text-center text-sm text-gray-400 max-w-sm mx-auto">
          We've sent a verification link to <span className="text-white font-medium">{email || 'your email'}</span>.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md relative z-10">
        <div className="bg-white/[0.03] border border-white/10 py-8 px-4 shadow-2xl sm:rounded-2xl sm:px-10 text-center backdrop-blur-xl">
          {!success ? (
            <>
              <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <Mail className="w-8 h-8 text-blue-400" />
              </div>
              <p className="text-gray-300 mb-8">
                Please check your inbox and click the link to verify your account. (Mock: Click button below)
              </p>
              <button
                onClick={handleVerify}
                disabled={verifying}
                className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-500 focus:outline-none transition-all group disabled:opacity-50"
              >
                {verifying ? 'Verifying...' : 'Simulate Verification'}
              </button>
            </>
          ) : (
            <>
              <div className="w-16 h-16 bg-emerald-500/10 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle2 className="w-8 h-8 text-emerald-400" />
              </div>
              <p className="text-emerald-400 font-medium mb-8">
                Email verified successfully!
              </p>
              <Link
                to="/onboarding"
                className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-500 focus:outline-none transition-all group"
              >
                Continue to Profile Setup
                <ArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default VerifyEmail;
