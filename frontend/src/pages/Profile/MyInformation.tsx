import React, { useState, useEffect } from 'react';
import { User, Mail, Clock, Calendar, Save, Loader2, Link as LinkIcon, Camera, LayoutDashboard, Settings, LogOut, ArrowLeft } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

const MyInformation = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  
  const [profile, setProfile] = useState({
    preferred_name: '',
    date_of_birth: '',
    bio: '',
    timezone: '',
    profile_photo_url: ''
  });

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const res = await api.get('/profile/user');
      if (res.data) {
        setProfile({
          preferred_name: res.data.preferred_name || '',
          date_of_birth: res.data.date_of_birth || '',
          bio: res.data.bio || '',
          timezone: res.data.timezone || '',
          profile_photo_url: res.data.profile_photo_url || ''
        });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setProfile(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccessMsg('');
    setErrorMsg('');

    try {
      await api.put('/profile/user', profile);
      setSuccessMsg('Profile updated successfully.');
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setSaving(false);
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
          <Link to="/profile" className="flex items-center gap-3 px-3 py-2.5 rounded-xl bg-blue-600/10 text-blue-400 font-medium transition-all">
            <User className="w-5 h-5 text-blue-400" /> My Information
          </Link>
          <Link to="/settings/security" className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-all">
            <Settings className="w-5 h-5 text-gray-500" /> Security & Password
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
          <h1 className="text-xl font-semibold">My Information</h1>
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center">
            {(user?.profile?.preferred_name || user?.profile?.first_name || user?.email || 'U')[0].toUpperCase()}
          </div>
        </header>

        <div className="p-4 sm:p-8 max-w-4xl mx-auto">
          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
            </div>
          ) : (
            <div className="space-y-8">
              {/* Profile Photo Section */}
              <div className="bg-[#111] border border-white/5 rounded-2xl p-6 sm:p-8">
                <h3 className="text-lg font-semibold mb-6">Profile Photo</h3>
                <div className="flex items-center gap-6">
                  <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center text-3xl font-bold border-4 border-[#0a0a0a] shadow-xl">
                    {(user?.profile?.preferred_name || user?.profile?.first_name || user?.email || 'U')[0].toUpperCase()}
                  </div>
                  <div>
                    <button className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl transition-colors mb-2 text-sm font-medium">
                      <Camera className="w-4 h-4" /> Change Photo
                    </button>
                    <p className="text-xs text-gray-500">Recommended size: 256x256px</p>
                  </div>
                </div>
              </div>

              {/* Personal Information Form */}
              <div className="bg-[#111] border border-white/5 rounded-2xl p-6 sm:p-8">
                <h3 className="text-lg font-semibold mb-6">Personal Details</h3>
                
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

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Email Address</label>
                      <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <Mail className="h-5 w-5 text-gray-500" />
                        </div>
                        <input
                          type="email"
                          value={user?.email || ''}
                          readOnly
                          className="block w-full pl-10 pr-3 py-2.5 border border-white/10 rounded-xl bg-white/5 text-gray-400 cursor-not-allowed sm:text-sm"
                        />
                      </div>
                      <p className="mt-1 text-xs text-gray-500">Contact support to change email.</p>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Preferred Name</label>
                      <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <User className="h-5 w-5 text-gray-500" />
                        </div>
                        <input
                          type="text"
                          name="preferred_name"
                          value={profile.preferred_name}
                          onChange={handleChange}
                          className="block w-full pl-10 pr-3 py-2.5 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-all"
                          placeholder="Your preferred name"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Date of Birth</label>
                      <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <Calendar className="h-5 w-5 text-gray-500" />
                        </div>
                        <input
                          type="date"
                          name="date_of_birth"
                          value={profile.date_of_birth}
                          onChange={handleChange}
                          className="block w-full pl-10 pr-3 py-2.5 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-all [color-scheme:dark]"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-300 mb-2">Timezone</label>
                      <div className="relative">
                        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                          <Clock className="h-5 w-5 text-gray-500" />
                        </div>
                        <input
                          type="text"
                          name="timezone"
                          value={profile.timezone}
                          onChange={handleChange}
                          className="block w-full pl-10 pr-3 py-2.5 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-all"
                          placeholder="e.g. America/Los_Angeles"
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Short Bio</label>
                    <textarea
                      name="bio"
                      value={profile.bio}
                      onChange={handleChange}
                      rows={4}
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent sm:text-sm transition-all"
                      placeholder="Write a little about yourself..."
                    />
                  </div>

                  <div className="pt-4 border-t border-white/5 flex justify-end">
                    <button
                      type="submit"
                      disabled={saving}
                      className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-xl transition-all shadow-[0_0_15px_rgba(37,99,235,0.3)] disabled:opacity-50"
                    >
                      {saving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
                      Save Changes
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default MyInformation;
