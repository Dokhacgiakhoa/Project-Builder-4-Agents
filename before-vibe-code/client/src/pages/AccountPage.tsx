import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Mail, Shield, Calendar, Sparkles, FileCode2, LogOut, CheckCircle2, 
  Save, Key, Award, Camera, Check, AlertTriangle, Eye, EyeOff, Send, RefreshCw
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

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

  // Email Verification States
  const [isEmailVerified, setIsEmailVerified] = useState(user?.isEmailVerified ?? false);
  const [showVerifyModal, setShowVerifyModal] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [generatedOtp, setGeneratedOtp] = useState('888666');
  const [verifyError, setVerifyError] = useState('');
  const [verifySuccess, setVerifySuccess] = useState(false);

  // Password Change States (Standard .NET Identity)
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showCurrentPw, setShowCurrentPw] = useState(false);
  const [showNewPw, setShowNewPw] = useState(false);
  const [showConfirmPw, setShowConfirmPw] = useState(false);
  const [pwSuccessMsg, setPwSuccessMsg] = useState('');
  const [pwErrorMsg, setPwErrorMsg] = useState('');

  // Password Validation Rules (.NET Identity Standards)
  const hasMinLength = newPassword.length >= 8;
  const hasUpperCase = /[A-Z]/.test(newPassword);
  const hasLowerCase = /[a-z]/.test(newPassword);
  const hasDigit = /[0-9]/.test(newPassword);
  const hasSpecialChar = /[^a-zA-Z0-9]/.test(newPassword);
  const isPasswordMatch = newPassword.length > 0 && newPassword === confirmPassword;

  // Calculate Password Strength (0 - 4)
  const strengthScore = [hasMinLength, hasUpperCase, hasLowerCase, hasDigit, hasSpecialChar].filter(Boolean).length;
  const getStrengthLabel = () => {
    if (strengthScore <= 2) return { text: 'Yếu', color: 'bg-rose-500 text-rose-600', percent: '25%' };
    if (strengthScore === 3) return { text: 'Trung Bình', color: 'bg-amber-500 text-amber-600', percent: '50%' };
    if (strengthScore === 4) return { text: 'Khá Mạnh', color: 'bg-blue-600 text-blue-600', percent: '75%' };
    return { text: 'Cực Mạnh (Chuẩn .NET)', color: 'bg-emerald-600 text-emerald-600', percent: '100%' };
  };

  // Mock recent generated prompts
  const recentProjects = [
    {
      name: "Smart Clinic Management",
      tech: "ASP.NET Core 10 + EF Core + SQL Server",
      date: "19/08/2026",
      status: "Master Prompt Ready"
    },
    {
      name: "Food Delivery Marketplace",
      tech: "ASP.NET Core Minimal APIs + React SPA",
      date: "18/08/2026",
      status: "Exported"
    }
  ];

  // Handle Save Profile
  const handleSaveProfile = (e: React.FormEvent) => {
    e.preventDefault();
    updateProfile({
      fullName,
      avatar,
      role
    });
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  // Handle Send OTP for Email Verification
  const handleStartVerifyEmail = () => {
    const randomOtp = Math.floor(100000 + Math.random() * 900000).toString();
    setGeneratedOtp(randomOtp);
    setShowVerifyModal(true);
    setVerifyError('');
    setOtpCode('');
  };

  // Handle Submit OTP
  const handleConfirmOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (otpCode.trim() === generatedOtp || otpCode.trim() === '888666') {
      setIsEmailVerified(true);
      updateProfile({ isEmailVerified: true });
      setVerifySuccess(true);
      setTimeout(() => {
        setVerifySuccess(false);
        setShowVerifyModal(false);
      }, 1500);
    } else {
      setVerifyError('Mã OTP không đúng! Vui lòng kiểm tra lại mã xác nhận.');
    }
  };

  // Handle Change Password
  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault();
    setPwErrorMsg('');
    setPwSuccessMsg('');

    if (!currentPassword) {
      setPwErrorMsg('Vui lòng nhập mật khẩu hiện tại.');
      return;
    }

    if (strengthScore < 4) {
      setPwErrorMsg('Mật khẩu mới chưa đáp ứng đầy đủ các tiêu chuẩn bảo mật .NET Identity.');
      return;
    }

    if (!isPasswordMatch) {
      setPwErrorMsg('Xác nhận mật khẩu mới không khớp.');
      return;
    }

    setPwSuccessMsg('Đổi mật khẩu thành công theo chuẩn ASP.NET Core Identity!');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
    setTimeout(() => setPwSuccessMsg(''), 4000);
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="w-full max-w-[85%] mx-auto px-4 py-10 sm:py-16 space-y-10 relative z-10">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4">
        <div>
          <div className="octa-card-sm inline-flex items-center gap-2 px-3.5 py-1.5 bg-blue-100 text-blue-950 text-xs font-black mb-2">
            <Shield className="w-4 h-4 text-blue-600" /> Hồ Sơ & Quản Trị Tài Khoản
          </div>
          <h1 className="text-3xl sm:text-4xl font-black text-slate-950 tracking-tight">Trung Tâm Tài Khoản</h1>
          <p className="text-sm text-slate-600 font-semibold mt-1">
            Quản lý thông tin định danh, bảo mật mật khẩu chuẩn .NET và xem lịch sử Master Prompt.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/studio"
            className="octa-btn inline-flex items-center gap-2 px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm shadow-sm transition-all"
          >
            <Sparkles className="w-4 h-4 text-orange-400" /> Vào Setup Prompt
          </Link>
          <button
            onClick={handleLogout}
            className="octa-btn inline-flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 font-bold text-sm transition-colors cursor-pointer"
          >
            <LogOut className="w-4 h-4" /> Đăng Xuất
          </button>
        </div>
      </div>

      {/* Main Grid: User Profile Info & Actions (Hoàn Toàn Không Viền) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Avatar & Account Summary (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          {/* Main User Card */}
          <div className="floating-shadow">
            <div className="octa-card bg-white p-7 space-y-6">
              {/* Avatar & Info */}
              <div className="flex items-center gap-4">
                <div className="relative group">
                  <img
                    src={avatar}
                    alt={fullName}
                    className="octa-card w-20 h-20 object-cover shadow-md"
                  />
                  <div className="absolute -bottom-1 -right-1 octa-card-sm p-1.5 bg-blue-600 text-white shadow-sm">
                    <Camera className="w-3.5 h-3.5" />
                  </div>
                </div>
                <div className="space-y-1 min-w-0">
                  <h2 className="text-xl font-black text-slate-950 truncate">{fullName}</h2>
                  <div className="flex items-center gap-1.5 text-xs text-slate-500 font-semibold truncate">
                    <Mail className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span>{user?.email || 'user@example.com'}</span>
                  </div>
                  <div className="octa-card-sm inline-flex items-center gap-1 px-2.5 py-0.5 bg-blue-100 text-blue-950 text-[11px] font-black">
                    <Award className="w-3.5 h-3.5 text-orange-600" />
                    <span>{role}</span>
                  </div>
                </div>
              </div>

              {/* Avatar Preset Picker */}
              <div className="space-y-2 pt-2">
                <label className="block text-xs font-black uppercase tracking-wider text-slate-700">
                  Chọn Avatar Mẫu (6 Kiểu Phong Cách):
                </label>
                <div className="grid grid-cols-6 gap-2">
                  {PRESET_AVATARS.map((av, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setAvatar(av)}
                      className={`relative octa-card-sm overflow-hidden p-0.5 transition-all cursor-pointer ${
                        avatar === av ? 'ring-2 ring-blue-600 scale-105 shadow-xs' : 'opacity-80 hover:opacity-100'
                      }`}
                    >
                      <img src={av} alt="Preset" className="w-full h-9 object-cover rounded-xs" />
                      {avatar === av && (
                        <div className="absolute inset-0 bg-blue-600/30 flex items-center justify-center">
                          <Check className="w-3.5 h-3.5 text-white stroke-[3]" />
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* Email Verification Box */}
              <div className="octa-card-sm p-4 bg-slate-50 space-y-2.5">
                <div className="flex items-center justify-between">
                  <div className="text-xs font-black uppercase text-slate-700">Xác Thực Email</div>
                  {isEmailVerified ? (
                    <span className="octa-card-sm text-[11px] font-black px-2.5 py-0.5 bg-emerald-100 text-emerald-800 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" /> Đã Xác Thực
                    </span>
                  ) : (
                    <span className="octa-card-sm text-[11px] font-black px-2.5 py-0.5 bg-amber-100 text-amber-900 flex items-center gap-1">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-600" /> Chưa Xác Thực
                    </span>
                  )}
                </div>
                <p className="text-xs text-slate-500 font-semibold leading-relaxed">
                  {isEmailVerified
                    ? 'Tài khoản đã hoàn tất xác thực danh tính với ASP.NET Core Identity.'
                    : 'Xác thực email để bảo vệ tài khoản và nhận file SRS qua hộp thư đến.'}
                </p>
                {!isEmailVerified && (
                  <button
                    type="button"
                    onClick={handleStartVerifyEmail}
                    className="octa-btn w-full py-2 bg-orange-500 hover:bg-orange-600 text-white font-bold text-xs flex items-center justify-center gap-1.5 shadow-xs transition-colors cursor-pointer"
                  >
                    <Send className="w-3.5 h-3.5" /> Gửi Mã Xác Thực Email
                  </button>
                )}
              </div>

              {/* Quick Metrics */}
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="octa-card-sm p-3.5 bg-slate-50 space-y-1">
                  <div className="text-xs text-slate-500 font-bold">Số Prompt Đã Xuất</div>
                  <div className="text-2xl font-black text-blue-700">12</div>
                </div>
                <div className="octa-card-sm p-3.5 bg-slate-50 space-y-1">
                  <div className="text-xs text-slate-500 font-bold">Trạng Thái Hệ Thống</div>
                  <div className="text-sm font-black text-emerald-600 flex items-center gap-1 mt-1">
                    <CheckCircle2 className="w-4 h-4" /> Active .NET
                  </div>
                </div>
              </div>

              {/* Account Metadata */}
              <div className="space-y-2.5 pt-2 text-xs font-semibold text-slate-600">
                <div className="flex items-center justify-between">
                  <span className="flex items-center gap-1.5 text-slate-500">
                    <Calendar className="w-4 h-4" /> Ngày đăng ký:
                  </span>
                  <span className="text-slate-950 font-bold">19/08/2026</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="flex items-center gap-1.5 text-slate-500">
                    <Shield className="w-4 h-4" /> Phương thức bảo mật:
                  </span>
                  <span className="text-slate-950 font-bold">ASP.NET Identity + JWT</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Edit Profile & Password Standardization (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Section 1: Edit Profile Form */}
          <div className="floating-shadow">
            <div className="octa-card bg-white p-7 sm:p-8 space-y-5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 font-black text-slate-950 text-lg">
                  <Award className="w-5 h-5 text-blue-600" />
                  <span>Cập Nhật Thông Tin Cá Nhân</span>
                </div>
                {isSaved && (
                  <div className="octa-card-sm px-3 py-1 bg-emerald-100 text-emerald-900 text-xs font-black flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4" /> Đã lưu thông tin!
                  </div>
                )}
              </div>

              <form onSubmit={handleSaveProfile} className="space-y-4">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="block text-xs font-black text-slate-800">Họ và Tên</label>
                    <input
                      type="text"
                      required
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      className="w-full px-5 py-3.5 bg-slate-100 text-sm text-slate-950 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="block text-xs font-black text-slate-800">Email (Định danh)</label>
                    <input
                      type="email"
                      disabled
                      value={user?.email || 'user@example.com'}
                      className="w-full px-5 py-3.5 bg-slate-200/80 text-sm text-slate-500 font-bold rounded-lg cursor-not-allowed"
                    />
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="block text-xs font-black text-slate-800">Vai Trò / Định Hướng Kỹ Thuật</label>
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
                    <Save className="w-4 h-4" /> Lưu Thay Đổi
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Section 2: Password Standardization (.NET Identity Security) */}
          <div className="floating-shadow">
            <div className="octa-card bg-white p-7 sm:p-8 space-y-5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 font-black text-slate-950 text-lg">
                  <Key className="w-5 h-5 text-orange-500" />
                  <span>Chuẩn Hóa & Đổi Mật Khẩu (.NET Identity)</span>
                </div>
              </div>

              {pwSuccessMsg && (
                <div className="octa-card-sm p-3.5 bg-emerald-100 text-emerald-950 text-xs font-bold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{pwSuccessMsg}</span>
                </div>
              )}

              {pwErrorMsg && (
                <div className="octa-card-sm p-3.5 bg-rose-100 text-rose-950 text-xs font-bold flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
                  <span>{pwErrorMsg}</span>
                </div>
              )}

              <form onSubmit={handleChangePassword} className="space-y-4">
                {/* Current Password */}
                <div className="space-y-1.5">
                  <label className="block text-xs font-black text-slate-800">Mật khẩu hiện tại</label>
                  <div className="relative">
                    <input
                      type={showCurrentPw ? 'text' : 'password'}
                      required
                      value={currentPassword}
                      onChange={(e) => setCurrentPassword(e.target.value)}
                      placeholder="••••••••"
                      className="w-full px-5 py-3.5 pr-10 bg-slate-100 text-sm text-slate-950 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all"
                    />
                    <button
                      type="button"
                      onClick={() => setShowCurrentPw(!showCurrentPw)}
                      className="absolute right-3 top-3 text-slate-400 hover:text-slate-600"
                    >
                      {showCurrentPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* New Password & Confirm */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="block text-xs font-black text-slate-800">Mật khẩu mới</label>
                    <div className="relative">
                      <input
                        type={showNewPw ? 'text' : 'password'}
                        required
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        placeholder="Mật khẩu mới..."
                        className="w-full px-5 py-3.5 pr-10 bg-slate-100 text-sm text-slate-950 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all"
                      />
                      <button
                        type="button"
                        onClick={() => setShowNewPw(!showNewPw)}
                        className="absolute right-3 top-3 text-slate-400 hover:text-slate-600"
                      >
                        {showNewPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  <div className="space-y-1.5">
                    <label className="block text-xs font-black text-slate-800">Xác nhận mật khẩu mới</label>
                    <div className="relative">
                      <input
                        type={showConfirmPw ? 'text' : 'password'}
                        required
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Nhập lại mật khẩu mới..."
                        className="w-full px-5 py-3.5 pr-10 bg-slate-100 text-sm text-slate-950 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all"
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirmPw(!showConfirmPw)}
                        className="absolute right-3 top-3 text-slate-400 hover:text-slate-600"
                      >
                        {showConfirmPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Password Strength Meter */}
                {newPassword.length > 0 && (
                  <div className="space-y-2 pt-1">
                    <div className="flex justify-between items-center text-xs font-bold">
                      <span className="text-slate-600">Độ mạnh mật khẩu:</span>
                      <span className={`font-black ${getStrengthLabel().color}`}>{getStrengthLabel().text}</span>
                    </div>
                    <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                      <div
                        className={`h-full transition-all duration-300 ${getStrengthLabel().color.split(' ')[0]}`}
                        style={{ width: getStrengthLabel().percent }}
                      />
                    </div>
                  </div>
                )}

                {/* Password Requirements Checklist */}
                <div className="octa-card-sm p-4 bg-slate-50 space-y-2 text-xs">
                  <div className="font-black text-slate-800 uppercase tracking-wider text-[11px]">
                    Tiêu chuẩn bắt buộc (.NET Identity Standard):
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 font-semibold">
                    <div className={`flex items-center gap-1.5 ${hasMinLength ? 'text-emerald-600' : 'text-slate-500'}`}>
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Tối thiểu 8 ký tự</span>
                    </div>
                    <div className={`flex items-center gap-1.5 ${hasUpperCase ? 'text-emerald-600' : 'text-slate-500'}`}>
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Ít nhất 1 chữ in hoa (A-Z)</span>
                    </div>
                    <div className={`flex items-center gap-1.5 ${hasLowerCase ? 'text-emerald-600' : 'text-slate-500'}`}>
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Ít nhất 1 chữ thường (a-z)</span>
                    </div>
                    <div className={`flex items-center gap-1.5 ${hasDigit ? 'text-emerald-600' : 'text-slate-500'}`}>
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Ít nhất 1 chữ số (0-9)</span>
                    </div>
                    <div className={`flex items-center gap-1.5 ${hasSpecialChar ? 'text-emerald-600' : 'text-slate-500'}`}>
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Ít nhất 1 ký tự đặc biệt (@, #, $...)</span>
                    </div>
                    <div className={`flex items-center gap-1.5 ${isPasswordMatch ? 'text-emerald-600' : 'text-slate-500'}`}>
                      <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                      <span>Mật khẩu xác nhận khớp</span>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end pt-1">
                  <button
                    type="submit"
                    disabled={strengthScore < 4 || !isPasswordMatch}
                    className="octa-btn inline-flex items-center gap-2 px-6 py-2.5 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold text-sm shadow-sm transition-all cursor-pointer"
                  >
                    <Key className="w-4 h-4" /> Cập Nhật Mật Khẩu
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Section 3: Recent Master Prompts */}
          <div className="floating-shadow">
            <div className="octa-card bg-white p-7 sm:p-8 space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 font-black text-slate-950 text-lg">
                  <FileCode2 className="w-5 h-5 text-orange-500" />
                  <span>Dự Án & Master Prompt Đã Tạo Gần Đây</span>
                </div>
                <Link to="/studio" className="text-xs font-bold text-blue-600 hover:underline">
                  + Tạo Mới
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

      {/* Verify Email Modal */}
      {showVerifyModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-in fade-in duration-200">
          <div className="octa-card-lg bg-white p-7 sm:p-9 max-w-md w-full space-y-6 shadow-2xl">
            <div className="text-center space-y-2">
              <div className="octa-card w-14 h-14 bg-blue-100 text-blue-700 flex items-center justify-center mx-auto shadow-sm">
                <Mail className="w-7 h-7" />
              </div>
              <h3 className="text-2xl font-black text-slate-950">Xác Thực Hộp Thư Email</h3>
              <p className="text-xs text-slate-600 font-semibold">
                Mã xác nhận 6 số đã được gửi tới: <br />
                <strong className="text-blue-700">{user?.email || 'user@example.com'}</strong>
              </p>
            </div>

            {/* Test Simulation Hint */}
            <div className="octa-card-sm p-3 bg-blue-50 text-xs text-blue-900 font-semibold text-center">
              Mã xác nhận giả lập (.NET OTP): <strong className="font-mono text-blue-800 text-sm">{generatedOtp}</strong>
            </div>

            {verifyError && (
              <div className="octa-card-sm p-3 bg-rose-100 text-rose-950 text-xs font-bold flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>{verifyError}</span>
              </div>
            )}

            {verifySuccess && (
              <div className="octa-card-sm p-3 bg-emerald-100 text-emerald-950 text-xs font-bold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Xác thực email thành công! Đang cập nhật trạng thái...</span>
              </div>
            )}

            <form onSubmit={handleConfirmOtp} className="space-y-4">
              <div className="space-y-1.5">
                <label className="block text-xs font-black text-slate-800 text-center">
                  Nhập mã OTP 6 số:
                </label>
                <input
                  type="text"
                  maxLength={6}
                  required
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  placeholder="Ví dụ: 888666"
                  className="w-full px-5 py-3.5 bg-slate-100 text-center font-mono text-xl tracking-widest text-slate-950 font-black rounded-lg focus:bg-white focus:shadow-md transition-all"
                />
              </div>

              <div className="flex justify-between items-center text-xs text-slate-500 font-semibold">
                <span>Chưa nhận được mã?</span>
                <button
                  type="button"
                  onClick={handleStartVerifyEmail}
                  className="text-blue-600 font-bold hover:underline flex items-center gap-1"
                >
                  <RefreshCw className="w-3 h-3" /> Gửi lại mã
                </button>
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowVerifyModal(false)}
                  className="octa-btn flex-1 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm transition-colors cursor-pointer"
                >
                  Hủy Bỏ
                </button>
                <button
                  type="submit"
                  disabled={otpCode.length < 6}
                  className="octa-btn flex-1 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold text-sm shadow-md transition-colors cursor-pointer"
                >
                  Xác Nhận
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
