import React from 'react';
import { Card } from '@/components/ui/card';
import { Layers, Activity, Cpu, Database } from 'lucide-react';

export const DashboardView: React.FC = () => {
  const metrics = [
    { label: 'Architecture', val: 'Bulletproof React', icon: Layers, status: 'healthy' },
    { label: 'API Connection', val: 'OpenAPI 3.0 Ready', icon: Activity, status: 'healthy' },
    { label: 'AI Agent Engine', val: 'Multi-Agent Support', icon: Cpu, status: 'healthy' },
    { label: 'State Sync', val: 'Zustand + TanStack Query', icon: Database, status: 'healthy' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Project Overview</h1>
        <p className="text-sm text-slate-500">Feature-Driven Frontend Blueprint kết nối sẵn sàng cùng Clean Architecture Backend.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((m, idx) => {
          const Icon = m.icon;
          return (
            <Card key={idx} className="hover:border-sky-300 transition-colors">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-600">{m.label}</span>
                <div className="p-2 bg-sky-50 text-sky-600 rounded-lg">
                  <Icon className="h-5 w-5" />
                </div>
              </div>
              <div className="mt-4">
                <span className="text-lg font-bold text-slate-900">{m.val}</span>
              </div>
              <div className="mt-2 flex items-center text-xs text-emerald-600">
                <span className="h-2 w-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
                Active & Operational
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
