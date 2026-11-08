import React, { useState, Suspense } from 'react';
import { AppProviders } from '@/app/provider';
import { MainLayout } from '@/components/layouts/main-layout';
import { ErrorBoundary } from '@/components/ui/error-boundary';
import { LayoutDashboard, MessageSquare, Palette } from 'lucide-react';

// Code-splitting via React.lazy for route/view bundles
const DashboardView = React.lazy(() => import('@/features/dashboard').then(m => ({ default: m.DashboardView })));
const ChatInterface = React.lazy(() => import('@/features/ai-chat').then(m => ({ default: m.ChatInterface })));
const ThemeShowcaseView = React.lazy(() => import('@/features/theme-showcase').then(m => ({ default: m.ThemeShowcaseView })));

type ActiveTab = 'dashboard' | 'chat' | 'theme-showcase';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');

  return (
    <AppProviders>
      <MainLayout>
        <ErrorBoundary>
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
                Overview (Dashboard)
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

            {/* Tab Views with Suspense */}
            <Suspense fallback={<div className="p-8 text-center text-slate-500">Loading content...</div>}>
              {activeTab === 'dashboard' && <DashboardView />}
              {activeTab === 'chat' && <ChatInterface />}
              {activeTab === 'theme-showcase' && <ThemeShowcaseView />}
            </Suspense>
          </div>
        </ErrorBoundary>
      </MainLayout>
    </AppProviders>
  );
};

export default App;
