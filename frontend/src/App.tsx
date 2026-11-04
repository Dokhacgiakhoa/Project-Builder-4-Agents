import React from 'react';
import { AppProviders } from '@/app/provider';
import { MainLayout } from '@/components/layouts/main-layout';
import { DashboardView } from '@/features/dashboard';
import { ChatInterface } from '@/features/ai-chat';

export const App: React.FC = () => {
  return (
    <AppProviders>
      <MainLayout>
        <div className="space-y-8">
          <DashboardView />
          <ChatInterface />
        </div>
      </MainLayout>
    </AppProviders>
  );
};

export default App;
