import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronRight, ChevronLeft, Check, Sparkles, UserCircle, GraduationCap, Briefcase, Loader2 } from 'lucide-react';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const steps = [
  { id: 'basic', title: 'Basic Info', icon: UserCircle },
  { id: 'education', title: 'Education', icon: GraduationCap },
  { id: 'role', title: 'Role & Interests', icon: Briefcase },
];

const ProfileSetup = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [formData, setFormData] = useState({
    preferredName: '',
    dateOfBirth: '',
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    bio: '',
    educationLevel: 'Undergraduate',
    degree: '',
    university: '',
    graduationYear: new Date().getFullYear() + 2,
    primaryRole: 'Student'
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleNext = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(prev => prev + 1);
    } else {
      handleSubmit();
    }
  };

  const handleBack = () => {
    if (currentStep > 0) setCurrentStep(prev => prev - 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      if (formData.preferredName) {
        await api.post('/profile/user', {
          preferred_name: formData.preferredName,
          date_of_birth: formData.dateOfBirth || undefined,
          timezone: formData.timezone,
          bio: formData.bio
        });
      }
      
      if (formData.university) {
        await api.post('/profile/education', {
          education_level: formData.educationLevel,
          degree: formData.degree,
          university: formData.university,
          graduation_year: formData.graduationYear
        });
      }

      navigate('/dashboard');
    } catch (error) {
      console.error('Failed to setup profile', error);
      // For now, continue to dashboard on error as it might already exist
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const StepIcon = steps[currentStep].icon;

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white py-12 px-4 sm:px-6 lg:px-8 font-sans overflow-x-hidden">
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[10%] right-[10%] w-[30%] h-[30%] rounded-full bg-blue-600/10 blur-[120px]" />
      </div>

      <div className="max-w-3xl mx-auto relative z-10">
        <div className="text-center mb-12">
          <Sparkles className="w-12 h-12 text-blue-400 mx-auto mb-4" />
          <h2 className="text-3xl font-bold tracking-tight">Welcome to Nexora AI</h2>
          <p className="mt-2 text-gray-400">Let's set up your personal workspace</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-12">
          <div className="flex items-center justify-between relative">
            <div className="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-white/10 rounded-full" />
            <div 
              className="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-blue-500 rounded-full transition-all duration-300"
              style={{ width: `${(currentStep / (steps.length - 1)) * 100}%` }}
            />
            
            {steps.map((step, idx) => (
              <div key={step.id} className="relative z-10 flex flex-col items-center">
                <div 
                  className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors ${
                    idx <= currentStep 
                      ? 'bg-blue-600 border-blue-600 text-white shadow-[0_0_15px_rgba(37,99,235,0.5)]' 
                      : 'bg-[#0a0a0a] border-white/20 text-gray-500'
                  }`}
                >
                  {idx < currentStep ? <Check className="w-5 h-5" /> : <span>{idx + 1}</span>}
                </div>
                <span className={`absolute top-12 text-xs font-medium whitespace-nowrap ${
                  idx <= currentStep ? 'text-blue-400' : 'text-gray-500'
                }`}>
                  {step.title}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Form Container */}
        <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-8 backdrop-blur-xl mt-16 transition-all duration-300">
          <div className="flex items-center gap-3 mb-8 pb-4 border-b border-white/10">
            <div className="p-3 bg-blue-500/10 rounded-xl text-blue-400">
              <StepIcon className="w-6 h-6" />
            </div>
            <h3 className="text-2xl font-semibold">{steps[currentStep].title}</h3>
          </div>

          <div className="space-y-6">
            {currentStep === 0 && (
              <div className="animate-in fade-in slide-in-from-right-4 duration-500">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Preferred Name</label>
                    <input
                      type="text"
                      name="preferredName"
                      value={formData.preferredName}
                      onChange={handleChange}
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="What should we call you?"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Date of Birth</label>
                    <input
                      type="date"
                      name="dateOfBirth"
                      value={formData.dateOfBirth}
                      onChange={handleChange}
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all [color-scheme:dark]"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Timezone</label>
                    <input
                      type="text"
                      name="timezone"
                      value={formData.timezone}
                      readOnly
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-white/5 text-gray-400 cursor-not-allowed"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Short Bio</label>
                    <textarea
                      name="bio"
                      value={formData.bio}
                      onChange={handleChange}
                      rows={3}
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="Tell us a little about yourself..."
                    />
                  </div>
                </div>
              </div>
            )}

            {currentStep === 1 && (
              <div className="animate-in fade-in slide-in-from-right-4 duration-500">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Education Level</label>
                    <select
                      name="educationLevel"
                      value={formData.educationLevel}
                      onChange={handleChange}
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    >
                      <option className="bg-gray-900">High School</option>
                      <option className="bg-gray-900">Undergraduate</option>
                      <option className="bg-gray-900">Graduate</option>
                      <option className="bg-gray-900">PhD</option>
                      <option className="bg-gray-900">Bootcamp</option>
                      <option className="bg-gray-900">Self-Taught</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Degree / Major</label>
                    <input
                      type="text"
                      name="degree"
                      value={formData.degree}
                      onChange={handleChange}
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="e.g. B.S. Computer Science"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">University / Institution</label>
                    <input
                      type="text"
                      name="university"
                      value={formData.university}
                      onChange={handleChange}
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                      placeholder="e.g. Stanford University"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Expected Graduation Year</label>
                    <input
                      type="number"
                      name="graduationYear"
                      value={formData.graduationYear}
                      onChange={handleChange}
                      min="2000"
                      max="2050"
                      className="block w-full px-4 py-3 border border-white/10 rounded-xl bg-black/20 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    />
                  </div>
                </div>
              </div>
            )}

            {currentStep === 2 && (
              <div className="animate-in fade-in slide-in-from-right-4 duration-500">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">Primary Role</label>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-2">
                      {['Student', 'Researcher', 'Developer', 'Creator'].map(role => (
                        <div 
                          key={role}
                          onClick={() => setFormData(prev => ({ ...prev, primaryRole: role }))}
                          className={`cursor-pointer p-4 rounded-xl border transition-all ${
                            formData.primaryRole === role 
                              ? 'bg-blue-500/20 border-blue-500 text-white' 
                              : 'bg-black/20 border-white/10 text-gray-400 hover:border-white/30'
                          }`}
                        >
                          <div className="font-medium">{role}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="mt-10 flex items-center justify-between pt-6 border-t border-white/10">
            <button
              type="button"
              onClick={handleBack}
              disabled={currentStep === 0 || loading}
              className={`flex items-center py-2 px-4 rounded-lg font-medium transition-colors ${
                currentStep === 0 ? 'text-transparent cursor-default' : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              <ChevronLeft className="w-5 h-5 mr-1" /> Back
            </button>
            
            <button
              onClick={handleNext}
              disabled={loading}
              className="flex items-center py-2.5 px-6 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-medium shadow-[0_0_15px_rgba(37,99,235,0.3)] transition-all disabled:opacity-50 group"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : currentStep === steps.length - 1 ? (
                <>
                  Complete Setup
                  <Check className="w-5 h-5 ml-2" />
                </>
              ) : (
                <>
                  Continue
                  <ChevronRight className="w-5 h-5 ml-1 group-hover:translate-x-1 transition-transform" />
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileSetup;
