import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { LogIn, UserPlus, Lock, Mail, User, ArrowRight, ShieldCheck, AlertCircle } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import gsap from 'gsap';

export const LoginPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { login } = useAuth();
  const cardRef = useRef<HTMLDivElement>(null);

  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const notice = (location.state as { notice?: string })?.notice;
  const redirectTarget = (location.state as { from?: string })?.from || '/studio';

  useEffect(() => {
    if (cardRef.current) {
      gsap.fromTo(
        cardRef.current,
        { opacity: 0, y: 30, scale: 0.96 },
        { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'power3.out', clearProps: 'transform' }
      );
    }
  }, [isRegister]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password.trim()) return;

    login(email, fullName || (isRegister ? fullName : email.split('@')[0]));

    if (isRegister) {
      setSuccessMsg('Registration successful! Redirecting to Setup Prompt...');
    } else {
      setSuccessMsg('Signed in successfully! Redirecting to Setup Prompt...');
    }

    setTimeout(() => {
      navigate(redirectTarget, { replace: true });
    }, 900);
  };

  return (
    <div className="max-w-lg mx-auto px-4 py-12 sm:py-20 relative z-10">
      <div ref={cardRef} className="floating-shadow-lg">
        <div className="octa-card-lg bg-white/95 p-8 sm:p-10 space-y-7 border border-slate-200/80 shadow-xl">
          <div className="text-center space-y-2.5">
            <div className="floating-shadow-sm inline-block">
              <div className="octa-card w-16 h-16 bg-blue-700 text-white flex items-center justify-center mx-auto shadow-md">
                {isRegister ? <UserPlus className="w-8 h-8" /> : <LogIn className="w-8 h-8" />}
              </div>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-slate-950 tracking-tight">
              {isRegister ? 'Create New Account' : 'Sign In'}
            </h2>
            <p className="text-sm sm:text-base text-slate-700 font-bold">
              {isRegister
                ? 'Persist project history and Master Prompts in Before Vibe Code'
                : 'Access the Setup Prompt architectural studio'}
            </p>
          </div>

          {notice && !successMsg && (
            <div className="octa-card-sm p-4 bg-orange-100 text-orange-950 text-sm flex items-center gap-3 font-bold">
              <AlertCircle className="w-5 h-5 text-orange-700 shrink-0" />
              <span>{notice}</span>
            </div>
          )}

          {successMsg && (
            <div className="octa-card-sm p-4 bg-blue-100 text-blue-950 text-sm flex items-center gap-2.5 font-bold">
              <ShieldCheck className="w-5 h-5 text-blue-700 shrink-0" />
              {successMsg}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {isRegister && (
              <div className="space-y-2">
                <label className="block text-base font-black text-slate-900">Full Name</label>
                <div className="relative">
                  <User className="w-5 h-5 text-slate-400 absolute left-4 top-3.5" />
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Alex Smith"
                    className="w-full pl-12 pr-5 py-3.5 bg-slate-100/90 text-slate-950 text-base placeholder:text-slate-400 font-bold rounded-lg border border-slate-200/80 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
                  />
                </div>
              </div>
            )}

            <div className="space-y-2">
              <label className="block text-base font-black text-slate-900">Email</label>
              <div className="relative">
                <Mail className="w-5 h-5 text-slate-400 absolute left-4 top-3.5" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@company.com"
                  className="w-full pl-12 pr-5 py-3.5 bg-slate-100/90 text-slate-950 text-base placeholder:text-slate-400 font-bold rounded-lg border border-slate-200/80 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="block text-base font-black text-slate-900">Password</label>
                {!isRegister && (
                  <a href="#forgot" className="text-xs sm:text-sm text-blue-700 font-black hover:underline">
                    Forgot password?
                  </a>
                )}
              </div>
              <div className="relative">
                <Lock className="w-5 h-5 text-slate-400 absolute left-4 top-3.5" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-12 pr-5 py-3.5 bg-slate-100/90 text-slate-950 text-base placeholder:text-slate-400 font-bold rounded-lg border border-slate-200/80 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent transition-all"
                />
              </div>
            </div>

            <div className="floating-shadow-blue pt-2">
              <button
                type="submit"
                className="octa-btn w-full inline-flex items-center justify-center gap-2 py-4 bg-blue-700 hover:bg-blue-800 text-white font-black text-base transition-transform duration-200 cursor-pointer hover:-translate-y-0.5"
              >
                {isRegister ? 'Sign Up & Continue' : 'Sign In & Continue'}
                <ArrowRight className="w-5 h-5" />
              </button>
            </div>
          </form>

          <div className="text-center pt-3 border-t border-slate-100 text-sm text-slate-700 font-medium">
            {isRegister ? (
              <p>
                Already have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setIsRegister(false); setSuccessMsg(''); }}
                  className="text-blue-700 font-black hover:underline ml-1 cursor-pointer"
                >
                  Sign in now
                </button>
              </p>
            ) : (
              <p>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={() => { setIsRegister(true); setSuccessMsg(''); }}
                  className="text-orange-600 font-black hover:underline ml-1 cursor-pointer"
                >
                  Sign up for free
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
