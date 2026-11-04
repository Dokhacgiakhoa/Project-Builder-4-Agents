import React from 'react';
import { useAuthStore } from '@/stores/use-auth-store';
import { Button } from '@/components/ui/button';
import { Bot, LogOut, ShieldCheck } from 'lucide-react';

export const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isAuthenticated, logout } = useAuthStore();

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-sky-600 rounded-lg text-white">
              <Bot className="h-5 w-5" />
            </div>
            <span className="font-bold text-lg text-slate-900">Universal Starter Kit</span>
            <span className="text-xs bg-sky-100 text-sky-800 px-2 py-0.5 rounded-full font-medium">Frontend</span>
          </div>

          <nav className="flex items-center space-x-4">
            <span className="text-sm text-slate-600 flex items-center gap-1">
              <ShieldCheck className="h-4 w-4 text-emerald-600" />
              {isAuthenticated ? (user?.fullName ?? user?.email ?? 'Developer') : 'Guest Mode'}
            </span>
            {isAuthenticated ? (
              <Button variant="outline" size="sm" onClick={logout} className="flex items-center gap-1">
                <LogOut className="h-4 w-4" /> Đăng xuất
              </Button>
            ) : null}
          </nav>
        </div>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        Built with Universal AI-Native Starter Kit • Feature-Driven Architecture
      </footer>
    </div>
  );
};
