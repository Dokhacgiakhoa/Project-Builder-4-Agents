import React, { useState } from 'react';
import { 
  Key, CheckCircle2, AlertTriangle, Eye, EyeOff, Mail, RefreshCw
} from 'lucide-react';

interface SecuritySectionProps {
  userEmail: string;
  isEmailVerified: boolean;
  onEmailVerified: () => void;
}

export const SecuritySection: React.FC<SecuritySectionProps> = ({
  userEmail,
  isEmailVerified,
  onEmailVerified
}) => {
  // Password Change States (.NET Identity)
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showCurrentPw, setShowCurrentPw] = useState(false);
  const [showNewPw, setShowNewPw] = useState(false);
  const [showConfirmPw, setShowConfirmPw] = useState(false);
  const [pwSuccessMsg, setPwSuccessMsg] = useState('');
  const [pwErrorMsg, setPwErrorMsg] = useState('');

  // Email Verification States
  const [showVerifyModal, setShowVerifyModal] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [generatedOtp, setGeneratedOtp] = useState('888666');
  const [verifyError, setVerifyError] = useState('');
  const [verifySuccess, setVerifySuccess] = useState(false);

  // Validation Rules
  const hasMinLength = newPassword.length >= 8;
  const hasUpperCase = /[A-Z]/.test(newPassword);
  const hasLowerCase = /[a-z]/.test(newPassword);
  const hasDigit = /[0-9]/.test(newPassword);
  const hasSpecialChar = /[^a-zA-Z0-9]/.test(newPassword);
  const isPasswordMatch = newPassword.length > 0 && newPassword === confirmPassword;

  const strengthScore = [hasMinLength, hasUpperCase, hasLowerCase, hasDigit, hasSpecialChar].filter(Boolean).length;
  const getStrengthLabel = () => {
    if (strengthScore <= 2) return { text: 'Weak', color: 'bg-rose-500 text-rose-600', percent: '25%' };
    if (strengthScore === 3) return { text: 'Medium', color: 'bg-amber-500 text-amber-600', percent: '50%' };
    if (strengthScore === 4) return { text: 'Strong', color: 'bg-blue-600 text-blue-600', percent: '75%' };
    return { text: 'Very Strong (.NET Standard)', color: 'bg-emerald-600 text-emerald-600', percent: '100%' };
  };

  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault();
    setPwSuccessMsg('');
    setPwErrorMsg('');

    if (strengthScore < 4) {
      setPwErrorMsg('New password does not satisfy .NET Identity security standards!');
      return;
    }
    if (!isPasswordMatch) {
      setPwErrorMsg('Password confirmation does not match!');
      return;
    }

    setPwSuccessMsg('Password updated successfully following .NET Identity!');
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
    setTimeout(() => setPwSuccessMsg(''), 4000);
  };

  const handleStartVerifyEmail = () => {
    const randomCode = Math.floor(100000 + Math.random() * 900000).toString();
    setGeneratedOtp(randomCode);
    setVerifyError('');
    setVerifySuccess(false);
    setShowVerifyModal(true);
  };

  const handleConfirmOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (otpCode !== generatedOtp) {
      setVerifyError('Invalid verification OTP code. Please retry!');
      return;
    }

    setVerifySuccess(true);
    setTimeout(() => {
      onEmailVerified();
      setShowVerifyModal(false);
      setOtpCode('');
      setVerifySuccess(false);
    }, 1500);
  };

  return (
    <>
      <div className="floating-shadow">
        <div className="octa-card bg-white p-7 sm:p-8 space-y-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 font-black text-slate-950 text-lg">
              <Key className="w-5 h-5 text-orange-500" />
              <span>Update Password (.NET Identity Standard)</span>
            </div>
            {!isEmailVerified && (
              <button
                type="button"
                onClick={handleStartVerifyEmail}
                className="text-xs font-bold text-blue-600 hover:underline"
              >
                Verify Email Now
              </button>
            )}
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
            <div className="space-y-1.5">
              <label className="block text-xs font-black text-slate-800">Current Password</label>
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

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <label className="block text-xs font-black text-slate-800">New Password</label>
                <div className="relative">
                  <input
                    type={showNewPw ? 'text' : 'password'}
                    required
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="New password..."
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
                <label className="block text-xs font-black text-slate-800">Confirm New Password</label>
                <div className="relative">
                  <input
                    type={showConfirmPw ? 'text' : 'password'}
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Repeat new password..."
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

            {newPassword.length > 0 && (
              <div className="space-y-2 pt-1">
                <div className="flex justify-between items-center text-xs font-bold">
                  <span className="text-slate-600">Password Strength:</span>
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

            <div className="octa-card-sm p-4 bg-slate-50 space-y-2 text-xs">
              <div className="font-black text-slate-800 uppercase tracking-wider text-[11px]">
                Mandatory Requirements (.NET Identity Standard):
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 font-semibold">
                <div className={`flex items-center gap-1.5 ${hasMinLength ? 'text-emerald-600' : 'text-slate-500'}`}>
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                  <span>At least 8 characters</span>
                </div>
                <div className={`flex items-center gap-1.5 ${hasUpperCase ? 'text-emerald-600' : 'text-slate-500'}`}>
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                  <span>At least 1 uppercase letter (A-Z)</span>
                </div>
                <div className={`flex items-center gap-1.5 ${hasLowerCase ? 'text-emerald-600' : 'text-slate-500'}`}>
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                  <span>At least 1 lowercase letter (a-z)</span>
                </div>
                <div className={`flex items-center gap-1.5 ${hasDigit ? 'text-emerald-600' : 'text-slate-500'}`}>
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                  <span>At least 1 number (0-9)</span>
                </div>
                <div className={`flex items-center gap-1.5 ${hasSpecialChar ? 'text-emerald-600' : 'text-slate-500'}`}>
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                  <span>At least 1 special character</span>
                </div>
                <div className={`flex items-center gap-1.5 ${isPasswordMatch ? 'text-emerald-600' : 'text-slate-500'}`}>
                  <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                  <span>Confirmation match</span>
                </div>
              </div>
            </div>

            <div className="flex justify-end pt-1">
              <button
                type="submit"
                disabled={strengthScore < 4 || !isPasswordMatch}
                className="octa-btn inline-flex items-center gap-2 px-6 py-2.5 bg-orange-500 hover:bg-orange-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold text-sm shadow-sm transition-all cursor-pointer"
              >
                <Key className="w-4 h-4" /> Update Password
              </button>
            </div>
          </form>
        </div>
      </div>

      {showVerifyModal && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 z-50 animate-in fade-in duration-200">
          <div className="octa-card-lg bg-white p-7 sm:p-9 max-w-md w-full space-y-6 shadow-2xl">
            <div className="text-center space-y-2">
              <div className="octa-card w-14 h-14 bg-blue-100 text-blue-700 flex items-center justify-center mx-auto shadow-sm">
                <Mail className="w-7 h-7" />
              </div>
              <h3 className="text-2xl font-black text-slate-950">Verify Email Address</h3>
              <p className="text-xs text-slate-600 font-semibold">
                A 6-digit verification code was sent to: <br />
                <strong className="text-blue-700">{userEmail}</strong>
              </p>
            </div>

            <div className="octa-card-sm p-3 bg-blue-50 text-xs text-blue-900 font-semibold text-center">
              Simulation OTP (.NET OTP): <strong className="font-mono text-blue-800 text-sm">{generatedOtp}</strong>
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
                <span>Email verified successfully! Updating status...</span>
              </div>
            )}

            <form onSubmit={handleConfirmOtp} className="space-y-4">
              <div className="space-y-1.5">
                <label className="block text-xs font-black text-slate-800 text-center">
                  Enter 6-digit OTP code:
                </label>
                <input
                  type="text"
                  maxLength={6}
                  required
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  placeholder="e.g. 888666"
                  className="w-full px-5 py-3.5 bg-slate-100 text-center font-mono text-xl tracking-widest text-slate-950 font-black rounded-lg focus:bg-white focus:shadow-md transition-all"
                />
              </div>

              <div className="flex justify-between items-center text-xs text-slate-500 font-semibold">
                <span>Didn't receive code?</span>
                <button
                  type="button"
                  onClick={handleStartVerifyEmail}
                  className="text-blue-600 font-bold hover:underline flex items-center gap-1"
                >
                  <RefreshCw className="w-3 h-3" /> Resend code
                </button>
              </div>

              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowVerifyModal(false)}
                  className="octa-btn flex-1 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-sm transition-colors cursor-pointer"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={otpCode.length < 6}
                  className="octa-btn flex-1 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold text-sm shadow-md transition-colors cursor-pointer"
                >
                  Confirm
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
};
