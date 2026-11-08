import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Mail, Shield, Calendar, Sparkles, FileCode2, LogOut, CheckCircle2, 
  Save, Award, Camera
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { SecuritySection } from './account/SecuritySection';

const PRESET_AVATARS = [
  'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=150&auto=format&fit=crop&q=80',
];

export const AccountPage: React.FC = () => {
  const { user, updateProfile, logout } = useAuth();
  const navigate = useNavigate();

  // Profile Form States
  const [fullName, setFullName] = useState(user?.fullName || 'K.AI Labs');
  const [avatar, setAvatar] = useState(user?.avatar || PRESET_AVATARS[0]);
  const [role, setRole] = useState(user?.role || '.NET Fullstack Architect');
  const [isSaved, setIsSaved] = useState(false);
  const [isEmailVerified, setIsEmailVerified] = useState(user?.isEmailVerified ?? false);

  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    updateProfile({ fullName, avatar, role });
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const recentProjects = [
    { name: 'ASP.NET Core 10 Clean Architecture', tech: 'C# / SQL Server / MediatR', date: 'Just now', status: 'Completed' },
    { name: 'SaaS Multi-tenant Starter', tech: 'React 19 / Tailwind / EF Core', date: '2 hours ago', status: 'Running' },
    { name: 'E-Commerce High Load Microservices', tech: 'Docker / Redis / PostgreSQL', date: 'Yesterday', status: 'Completed' },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-300">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-black text-slate-950 tracking-tight flex items-center gap-3">
          <Shield className="w-8 h-8 text-blue-600" />
          <span>Profile & Account Settings</span>
        </h1>
        <p className="text-slate-600 text-sm mt-1 font-semibold">
          Manage credentials, preferences, and enterprise .NET Identity security settings.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Avatar & User Card */}
        <div className="lg:col-span-5 space-y-6">
          <div className="floating-shadow">
            <div className="octa-card bg-white p-7 sm:p-8 space-y-6 text-center">
              <div className="relative inline-block mx-auto">
                <img
                  src={avatar}
                  alt={fullName}
                  className="w-28 h-28 rounded-full object-cover border-4 border-blue-100 shadow-md mx-auto"
                />
                <button
                  type="button"
                  title="Change avatar"
                  className="octa-card-sm absolute bottom-0 right-0 p-2 bg-blue-600 text-white shadow-md hover:bg-blue-700 transition-colors"
                >
                  <Camera className="w-4 h-4" />
                </button>
              </div>

              <div>
                <h2 className="text-xl font-black text-slate-950">{fullName}</h2>
                <p className="text-xs font-bold text-blue-700 mt-0.5">{role}</p>
                <div className="flex items-center justify-center gap-1.5 text-xs text-slate-500 font-semibold mt-2">
                  <Mail className="w-3.5 h-3.5" />
                  <span>{user?.email || 'user@example.com'}</span>
                </div>
              </div>

              {/* Avatar Selector */}
              <div className="pt-2 border-t border-slate-100">
                <label className="block text-xs font-black uppercase tracking-wider text-slate-700 mb-2">
                  Choose a preset avatar:
                </label>
                <div className="flex justify-center gap-2 flex-wrap">
                  {PRESET_AVATARS.map((avUrl, i) => (
                    <button
                      key={i}
                      type="button"
                      onClick={() => setAvatar(avUrl)}
                      className={`w-9 h-9 rounded-full overflow-hidden border-2 transition-transform hover:scale-110 ${
                        avatar === avUrl ? 'border-blue-600 ring-2 ring-blue-300' : 'border-transparent'
                      }`}
                    >
                      <img src={avUrl} alt="" className="w-full h-full object-cover" />
                    </button>
                  ))}
                </div>
              </div>

              {/* Account Stats */}
              <div className="grid grid-cols-2 gap-3 pt-2 text-left">
                <div className="octa-card-sm p-3.5 bg-slate-50">
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 font-bold">
                    <Calendar className="w-3.5 h-3.5 text-blue-600" /> Joined Date
                  </div>
                  <div className="text-xs font-black text-slate-950 mt-1">05/11/2026</div>
                </div>
                <div className="octa-card-sm p-3.5 bg-slate-50">
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 font-bold">
                    <Sparkles className="w-3.5 h-3.5 text-orange-500" /> Master Prompts
                  </div>
                  <div className="text-xs font-black text-slate-950 mt-1">12 Created</div>
                </div>
              </div>

              <button
                type="button"
                onClick={handleLogout}
                className="octa-btn w-full py-3 bg-rose-50 hover:bg-rose-100 text-rose-700 font-black text-xs sm:text-sm flex items-center justify-center gap-2 transition-colors cursor-pointer"
              >
                <LogOut className="w-4 h-4" /> Sign Out on This Device
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Profile Form & Security */}
        <div className="lg:col-span-7 space-y-6">
          {/* Edit Profile Form */}
          <div className="floating-shadow">
            <div className="octa-card bg-white p-7 sm:p-8 space-y-5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 font-black text-slate-950 text-lg">
                  <Award className="w-5 h-5 text-blue-600" />
                  <span>Edit Profile Information</span>
                </div>
                {isSaved && (
                  <div className="octa-card-sm px-3 py-1 bg-emerald-100 text-emerald-900 text-xs font-black flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" /> Profile saved!
                  </div>
                )}
              </div>

              <form onSubmit={handleSaveProfile} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="block text-xs font-black text-slate-800">Full Name</label>
                    <input
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      className="w-full px-5 py-3.5 bg-slate-100 text-sm text-slate-950 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="block text-xs font-black text-slate-800">Email Address</label>
                    <input
                      type="email"
                      disabled
                      value={user?.email || 'user@example.com'}
                      className="w-full px-5 py-3.5 bg-slate-200/80 text-sm text-slate-500 font-bold rounded-lg cursor-not-allowed"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="block text-xs font-black text-slate-800">Role / Technical Focus</label>
                  <select
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    className="w-full px-5 py-3.5 bg-slate-100 text-sm text-slate-950 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all cursor-pointer"
                  >
                    <option value=".NET Fullstack Architect">.NET Fullstack Architect</option>
                    <option value="Non-Tech Founder / Product Owner">Non-Tech Founder / Product Owner</option>
                    <option value="Senior ASP.NET Core Engineer">Senior ASP.NET Core Engineer</option>
                    <option value="Prompt Engineer & AI Specialist">Prompt Engineer & AI Specialist</option>
                  </select>
                </div>

                <div className="flex justify-end pt-1">
                  <button
                    type="submit"
                    className="octa-btn inline-flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-sm transition-all cursor-pointer"
                  >
                    <Save className="w-4 h-4" /> Save Changes
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Security & Password Section */}
          <SecuritySection
            userEmail={user?.email || 'user@example.com'}
            isEmailVerified={isEmailVerified}
            onEmailVerified={() => setIsEmailVerified(true)}
          />

          {/* Recent Master Prompts */}
          <div className="floating-shadow">
            <div className="octa-card bg-white p-7 sm:p-8 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 font-black text-slate-950 text-lg">
                  <FileCode2 className="w-5 h-5 text-orange-500" />
                  <span>Recent Projects & Master Prompts</span>
                </div>
                <Link to="/studio" className="text-xs font-bold text-blue-600 hover:underline">
                  + Create New
                </Link>
              </div>

              <div className="space-y-3">
                {recentProjects.map((proj, idx) => (
                  <div
                    key={idx}
                    className="octa-card-sm p-4 bg-slate-50 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-blue-50/50 transition-colors"
                  >
                    <div className="space-y-1">
                      <div className="font-black text-slate-950 text-sm">{proj.name}</div>
                      <div className="text-xs text-slate-500 font-semibold">{proj.tech}</div>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-slate-400 font-medium">{proj.date}</span>
                      <span className="octa-card-sm text-[11px] font-black px-2.5 py-1 bg-emerald-100 text-emerald-800">
                        {proj.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
