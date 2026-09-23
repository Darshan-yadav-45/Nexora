import React, { useState } from 'react';
import { User, Shield, Key, Smartphone, Monitor, Lock, Loader2, ArrowLeft, Settings, Save } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const Security = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  
  const [passwords, setPasswords] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPasswords(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setSuccessMsg('');
    setErrorMsg('');

    if (passwords.newPassword !== passwords.confirmPassword) {
      setErrorMsg('New passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      // Simulating network delay for mock
      await new Promise(resolve => setTimeout(resolve, 1000));
      setSuccessMsg('Password updated successfully.');
      setPasswords({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to change password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white flex">
      {/* Mini Sidebar */}
      <aside className="w-64 bg-[#111] border-r border-white/10 flex flex-col h-screen hidden md:flex">
        <div className="h-20 flex items-center px-6 border-b border-white/10">
          <span className="text-xl font-bold">Settings</span>
        </div>
        <div className="p-4 flex-1 space-y-2">
          <Link to="/dashboard" className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-all mb-4">
            <ArrowLeft className="w-5 h-5" /> Back to Dashboard
          </Link>
          <div className="font-medium text-xs text-gray-500 uppercase tracking-wider mb-2 px-3 pt-4">Profile Settings</div>
          <Link to="/profile" className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-all">
            <User className="w-5 h-5 text-gray-500" /> My Information
          </Link>
          <Link to="/settings/security" className="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-blue-600/10 text-blue-400 font-medium transition-all">
            <Shield className="w-5 h-5 text-blue-400" /> Security & Password
          </Link>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto">
        <header className="h-20 flex items-center justify-between px-8 bg-[#0a0a0a]/80 backdrop-blur-md border-b border-white/5 sticky top-0 z-30">
          <div className="flex items-center gap-4 md:hidden">
            <Link to="/dashboard" className="text-gray-400 hover:text-white">
              <ArrowLeft className="w-5 h-5" />
            </Link>
          </div>
          <h1 className="text-xl font-semibold">Security</h1>
          <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
             {(user?.profile?.preferred_name || user?.profile?.first_name || user?.email || 'U')[0].toUpperCase()}
          </div>
        </header>

        <div className="p-4 sm:p-8 max-w-4xl mx-auto space-y-8">
          
          {/* Change Password */}
          <div className="bg-[#111] border border-white/5 rounded-2xl p-6 sm:p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-blue-500/10 rounded-lg">
                <Key className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="text-lg font-semibold">Change Password</h3>
            </div>
            
            {successMsg && (
              <div className="p-3 mb-6 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-sm">
                {successMsg}
              </div>
            )}
            {errorMsg && (
              <div className="p-3 mb-6 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
                {errorMsg}
              </div>
            )}

            <form onSubmit={handlePasswordChange} className="space-y-4 max-w-md">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Current Password</label>
                <input
                  type="password"
                  name="currentPassword"
                  required
                  value={passwords.currentPassword}
                  onChange={handleChange}
                  className="block w-full px-4 py-2.5 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-all"
                  placeholder="••••••••"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">New Password</label>
                <input
                  type="password"
                  name="newPassword"
                  required
                  value={passwords.newPassword}
                  onChange={handleChange}
                  className="block w-full px-4 py-2.5 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-all"
                  placeholder="••••••••"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">Confirm New Password</label>
                <input
                  type="password"
                  name="confirmPassword"
                  required
                  value={passwords.confirmPassword}
                  onChange={handleChange}
                  className="block w-full px-4 py-2.5 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-all"
                  placeholder="••••••••"
                />
              </div>
              <div className="pt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-xl transition-all shadow-[0_0_15px_rgba(37,99,235,0.3)] disabled:opacity-50"
                >
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Lock className="w-4 h-4" />}
                  Update Password
                </button>
              </div>
            </form>
          </div>

          {/* Two-Factor Authentication */}
          <div className="bg-[#111] border border-white/5 rounded-2xl p-6 sm:p-8">
            <div className="flex items-start justify-between">
              <div className="flex gap-4">
                <div className="p-3 bg-purple-500/10 rounded-xl h-fit">
                  <Smartphone className="w-6 h-6 text-purple-400" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-1">Two-Factor Authentication</h3>
                  <p className="text-sm text-gray-400 max-w-md leading-relaxed">
                    Add an extra layer of security to your account. When logging in, you'll need to provide a code along with your password.
                  </p>
                </div>
              </div>
              <button className="px-5 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-colors text-sm font-medium whitespace-nowrap">
                Enable 2FA
              </button>
            </div>
          </div>

          {/* Active Sessions */}
          <div className="bg-[#111] border border-white/5 rounded-2xl p-6 sm:p-8">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-emerald-500/10 rounded-lg">
                <Monitor className="w-5 h-5 text-emerald-400" />
              </div>
              <h3 className="text-lg font-semibold">Active Sessions</h3>
            </div>
            
            <div className="space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border border-white/10 bg-white/5">
                <div className="flex items-center gap-4 mb-4 sm:mb-0">
                  <Monitor className="w-8 h-8 text-gray-400" />
                  <div>
                    <p className="font-medium">Windows • Chrome</p>
                    <p className="text-sm text-gray-500">192.168.1.1 • Active now</p>
                  </div>
                </div>
                <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 text-xs font-medium rounded-full self-start sm:self-auto">
                  Current Session
                </span>
              </div>

              <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border border-transparent hover:bg-white/5 transition-colors">
                <div className="flex items-center gap-4 mb-4 sm:mb-0">
                  <Smartphone className="w-8 h-8 text-gray-400" />
                  <div>
                    <p className="font-medium">iPhone 13 • Safari</p>
                    <p className="text-sm text-gray-500">10.0.0.1 • Last active: 2 hours ago</p>
                  </div>
                </div>
                <button className="px-4 py-2 text-sm text-red-400 hover:bg-red-500/10 rounded-lg transition-colors self-start sm:self-auto font-medium">
                  Revoke
                </button>
              </div>
            </div>
          </div>
          
        </div>
      </main>
    </div>
  );
};

export default Security;
