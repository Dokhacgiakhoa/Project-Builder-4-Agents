import React, { useState, useEffect, useRef } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Sparkles, Menu, X, LogIn, LogOut, Home, Terminal, MessageSquare } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, isAuthenticated, logout } = useAuth();

  const navLinks = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/studio', label: 'Setup Prompt', icon: Terminal },
    { path: '/contact', label: 'Contact & FAQ', icon: MessageSquare },
  ];

  // Sliding Indicator State for smooth tab transition
  const tabRefs = useRef<(HTMLAnchorElement | null)[]>([]);
  const [indicatorStyle, setIndicatorStyle] = useState<{ left: number; width: number; height: number; opacity: number }>({
    left: 0,
    width: 0,
    height: 0,
    opacity: 0
  });

  useEffect(() => {
    const activeIndex = navLinks.findIndex((l) => l.path === location.pathname);
    if (activeIndex !== -1 && tabRefs.current[activeIndex]) {
      const el = tabRefs.current[activeIndex];
      if (el) {
        setIndicatorStyle({
          left: el.offsetLeft,
          width: el.offsetWidth,
          height: el.offsetHeight,
          opacity: 1
        });
      }
    } else {
      setIndicatorStyle((prev) => ({ ...prev, opacity: 0 }));
    }
  }, [location.pathname]);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="w-full bg-white/95 backdrop-blur-md sticky top-0 z-50 shadow-sm">
      {/* 100% Full Width Container (Border-free) */}
      <div className="w-full px-6 sm:px-10 lg:px-14">
        <div className="flex items-center justify-between h-20">
          {/* Brand Logo & Subtitle */}
          <Link to="/" className="flex items-center gap-3.5 group shrink-0">
            <div className="octa-card-sm w-11 h-11 bg-blue-600 flex items-center justify-center shadow-md shadow-blue-600/20 group-hover:scale-105 transition-transform duration-200">
              <Sparkles className="w-6 h-6 text-white font-bold" />
            </div>
            <div className="flex flex-col">
              <div className="flex items-center gap-2">
                <span className="font-black text-xl sm:text-2xl text-slate-900 tracking-tight whitespace-nowrap">Before Vibe Code</span>
                <span className="octa-card-sm text-[11px] uppercase font-black tracking-wider px-2 py-0.5 bg-blue-50 text-blue-700 whitespace-nowrap">.NET 10 Core</span>
              </div>
              <p className="text-xs text-slate-500 font-semibold whitespace-nowrap">.NET Architecture & Master Prompt Studio</p>
            </div>
          </Link>

          {/* Desktop Sliding Indicator Navigation Menu */}
          <div className="hidden md:relative md:inline-flex items-center bg-slate-100 p-1.5 octa-card-sm shadow-inner">
            {/* Animated Sliding Pill Indicator */}
            <div
              className="absolute bg-blue-600 octa-btn transition-all duration-300 ease-out shadow-sm pointer-events-none"
              style={{
                left: `${indicatorStyle.left}px`,
                width: `${indicatorStyle.width}px`,
                height: `${indicatorStyle.height}px`,
                top: '6px',
                opacity: indicatorStyle.opacity
              }}
            />

            {navLinks.map((link, idx) => {
              const isActive = location.pathname === link.path;
              const Icon = link.icon;
              return (
                <Link
                  key={link.path}
                  to={link.path}
                  ref={(el) => {
                    tabRefs.current[idx] = el;
                  }}
                  className={`relative z-10 inline-flex items-center gap-2 px-6 py-2.5 text-sm font-black whitespace-nowrap transition-colors duration-200 select-none cursor-pointer ${
                    isActive ? 'text-white' : 'text-slate-700 hover:text-blue-700'
                  }`}
                >
                  <Icon className={`w-4 h-4 shrink-0 transition-colors duration-200 ${isActive ? 'text-white' : 'text-slate-500'}`} />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Right Action Buttons */}
          <div className="hidden md:flex items-center gap-3 shrink-0">
            {isAuthenticated ? (
              <div className="flex items-center gap-2.5">
                {/* Username & Avatar button linking to Account page */}
                <Link
                  to="/account"
                  title="View account details"
                  className={`octa-card-sm flex items-center gap-2.5 px-3.5 py-1.5 text-sm font-bold transition-all cursor-pointer group ${
                    location.pathname === '/account'
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'bg-slate-100 hover:bg-blue-50 text-slate-800 hover:text-blue-700'
                  }`}
                >
                  <img
                    src={user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'}
                    alt="Avatar"
                    className="w-7 h-7 rounded-full object-cover group-hover:scale-105 transition-transform"
                  />
                  <span className="max-w-[130px] truncate">{user?.fullName || user?.email}</span>
                </Link>

                <button
                  onClick={handleLogout}
                  title="Sign out"
                  className="octa-btn inline-flex items-center gap-1.5 px-4 py-2 bg-slate-100 hover:bg-rose-50 hover:text-rose-700 text-slate-700 text-sm font-bold transition-colors cursor-pointer"
                >
                  <LogOut className="w-4 h-4" /> Sign Out
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="octa-btn inline-flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold shadow-md shadow-blue-600/20 transition-all duration-200 hover:-translate-y-0.5"
              >
                <LogIn className="w-4 h-4" /> Sign In
              </Link>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="octa-btn p-2.5 bg-slate-100 text-slate-800 hover:bg-slate-200 transition-colors"
            >
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Dropdown */}
      {isOpen && (
        <div className="md:hidden bg-white px-6 pt-3 pb-5 space-y-2 shadow-xl">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              onClick={() => setIsOpen(false)}
              className={`octa-btn block px-4 py-3 text-center text-sm font-bold transition-colors ${
                location.pathname === link.path
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-50 text-slate-700 hover:bg-slate-100'
              }`}
            >
              {link.label}
            </Link>
          ))}
          <div className="pt-3 flex flex-col gap-2">
            {isAuthenticated ? (
              <div className="octa-card-sm flex items-center justify-between p-3 bg-slate-50">
                <Link
                  to="/account"
                  onClick={() => setIsOpen(false)}
                  className="flex items-center gap-2.5 text-sm font-bold text-slate-800 hover:text-blue-600 truncate"
                >
                  <img
                    src={user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80'}
                    alt="Avatar"
                    className="w-7 h-7 rounded-full object-cover"
                  />
                  <span className="truncate">{user?.fullName || user?.email}</span>
                </Link>
                <button
                  onClick={() => { handleLogout(); setIsOpen(false); }}
                  className="octa-btn px-3 py-1.5 bg-rose-600 text-white text-xs font-bold inline-flex items-center gap-1"
                >
                  <LogOut className="w-3.5 h-3.5" /> Sign Out
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                onClick={() => setIsOpen(false)}
                className="octa-btn flex items-center justify-center gap-2 w-full py-3 bg-blue-600 text-white text-sm font-bold shadow-md"
              >
                <LogIn className="w-4 h-4" /> Sign In
              </Link>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};
