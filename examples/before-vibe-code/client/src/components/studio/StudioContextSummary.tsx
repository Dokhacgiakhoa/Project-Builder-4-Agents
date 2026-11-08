import React from 'react';
import { Sparkles, Edit3, Cpu, Users, Layers, Rocket, ShieldCheck } from 'lucide-react';

interface StudioContextSummaryProps {
  currentStep: number;
  onNavigateStep: (step: number) => void;
  projectName: string;
  targetAudience: string;
  features: Array<{ title: string }>;
  frontendStack: string;
  backendStack: string;
  databaseStack: string;
  nonFunctionalReqs: string[];
}

export const StudioContextSummary: React.FC<StudioContextSummaryProps> = ({
  currentStep,
  onNavigateStep,
  projectName,
  targetAudience,
  features,
  frontendStack,
  backendStack,
  databaseStack,
  nonFunctionalReqs
}) => {
  return (
    <div className="lg:col-span-3 space-y-4 lg:sticky lg:top-24">
      <div className="floating-shadow">
        <div className="octa-card bg-white p-5 sm:p-6 space-y-5">
          <div className="flex items-center justify-between pb-2">
            <div className="flex items-center gap-2 text-slate-950 font-black text-sm">
              <Sparkles className="w-4 h-4 text-orange-500" />
              <span>Selected Context</span>
            </div>
            <span className="octa-card-sm text-[10px] uppercase font-black px-2.5 py-1 bg-blue-100 text-blue-950">
              {currentStep > 1 ? `Steps 1-${currentStep - 1} OK` : 'Initialize'}
            </span>
          </div>

          {/* Step 1 Summary */}
          <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
            currentStep > 1 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
          }`}>
            <div className="flex items-center justify-between text-xs font-black">
              <span className="flex items-center gap-1.5 text-blue-950">
                <Rocket className="w-3.5 h-3.5 text-orange-600" /> 1. Project Idea
              </span>
              {currentStep > 1 && (
                <button
                  type="button"
                  onClick={() => onNavigateStep(1)}
                  title="Edit step 1"
                  className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
            <p className="text-xs font-bold truncate">
              {projectName || (currentStep === 1 ? 'Typing...' : 'Untitled')}
            </p>
          </div>

          {/* Step 2 Summary */}
          <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
            currentStep > 2 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
          }`}>
            <div className="flex items-center justify-between text-xs font-black">
              <span className="flex items-center gap-1.5 text-blue-950">
                <Users className="w-3.5 h-3.5 text-blue-600" /> 2. Audience
              </span>
              {currentStep > 2 && (
                <button
                  type="button"
                  onClick={() => onNavigateStep(2)}
                  title="Edit step 2"
                  className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
            <p className="text-xs font-bold line-clamp-2">
              {targetAudience || (currentStep === 2 ? 'Typing...' : 'Not specified')}
            </p>
          </div>

          {/* Step 3 Summary */}
          <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
            currentStep > 3 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
          }`}>
            <div className="flex items-center justify-between text-xs font-black">
              <span className="flex items-center gap-1.5 text-blue-950">
                <Layers className="w-3.5 h-3.5 text-orange-600" /> 3. Features ({features.length})
              </span>
              {currentStep > 3 && (
                <button
                  type="button"
                  onClick={() => onNavigateStep(3)}
                  title="Edit step 3"
                  className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
            <div className="space-y-1">
              {features.slice(0, 2).map((f, i) => (
                <div key={i} className="text-[11px] font-bold truncate text-slate-800">
                  • {f.title}
                </div>
              ))}
              {features.length > 2 && (
                <div className="text-[10px] text-blue-800 font-black">
                  +{features.length - 2} more features...
                </div>
              )}
            </div>
          </div>

          {/* Step 4 Summary */}
          <div className={`space-y-1.5 p-3.5 octa-card-sm transition-all ${
            currentStep > 4 ? 'bg-blue-100/70 text-slate-950' : 'bg-slate-100 text-slate-600'
          }`}>
            <div className="flex items-center justify-between text-xs font-black">
              <span className="flex items-center gap-1.5 text-blue-950">
                <Cpu className="w-3.5 h-3.5 text-blue-700" /> 4. Tech Stack
              </span>
              {currentStep > 4 && (
                <button
                  type="button"
                  onClick={() => onNavigateStep(4)}
                  title="Edit step 4"
                  className="text-blue-700 hover:text-blue-900 p-0.5 cursor-pointer"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
            <div className="text-[11px] font-bold space-y-0.5 text-slate-800">
              <div className="truncate">💻 {frontendStack.split('(')[0].trim()}</div>
              <div className="truncate">⚙️ {backendStack.split('(')[0].trim()}</div>
              <div className="truncate">🗄️ {databaseStack.split('(')[0].trim()}</div>
            </div>
          </div>

          {/* Standards Summary */}
          {nonFunctionalReqs.length > 0 && currentStep > 4 && (
            <div className="space-y-1.5 p-3.5 octa-card-sm bg-blue-100/70 text-slate-950">
              <div className="flex items-center gap-1.5 text-xs font-black text-blue-950">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> Standards ({nonFunctionalReqs.length})
              </div>
              <div className="text-[11px] font-bold space-y-0.5 text-slate-800">
                {nonFunctionalReqs.slice(0, 2).map((req, idx) => (
                  <div key={idx} className="truncate">✓ {req}</div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
