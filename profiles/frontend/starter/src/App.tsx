import React, { useState } from 'react';
import { AppProviders } from '@/app/provider';
import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardView } from '@/features/dashboard';
import { ChatInterface } from '@/features/ai-chat';
import { ThemeShowcaseView } from '@/features/theme-showcase';
import { LayoutDashboard, MessageSquare, Palette } from 'lucide-react';

type ActiveTab = 'dashboard' | 'chat' | 'theme-showcase';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');

  return (
    <AppProviders>
      <MainLayout>
        <div className="space-y-6">
          {/* Navigation Bar Tabs */}
          <div className="flex items-center gap-1.5 p-1 bg-white border border-slate-200 rounded-xl w-fit shadow-sm">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-sky-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <LayoutDashboard className="h-3.5 w-3.5" />
              Tổng Quan (Dashboard)
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'chat'
                  ? 'bg-sky-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <MessageSquare className="h-3.5 w-3.5" />
              AI Assistant Chat
            </button>
            <button
              onClick={() => setActiveTab('theme-showcase')}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'theme-showcase'
                  ? 'bg-sky-600 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              <Palette className="h-3.5 w-3.5" />
              UI/UX Presets Studio
            </button>
          </div>

          {/* Tab Views */}
          {activeTab === 'dashboard' && <DashboardView />}
          {activeTab === 'chat' && <ChatInterface />}
          {activeTab === 'theme-showcase' && <ThemeShowcaseView />}
        </div>
      </MainLayout>
    </AppProviders>
  );
};

export default App;
