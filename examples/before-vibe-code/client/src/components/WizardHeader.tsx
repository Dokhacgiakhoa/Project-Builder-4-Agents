import React from 'react';
import { CheckCircle2 } from 'lucide-react';

interface WizardHeaderProps {
  currentStep: number;
  totalSteps: number;
  stepTitles: string[];
}

export const WizardHeader: React.FC<WizardHeaderProps> = ({ currentStep, stepTitles }) => {
  return (
    <div className="w-full max-w-[85%] mx-auto px-2 sm:px-4">
      {/* Step Indicator Card (Border-free) */}
      <div className="floating-shadow">
        <div className="octa-card p-3.5 sm:p-4.5 bg-white/95 backdrop-blur-md">
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-2.5 sm:gap-3.5 w-full">
            {stepTitles.map((title, index) => {
              const stepNum = index + 1;
              const isCompleted = stepNum < currentStep;
              const isCurrent = stepNum === currentStep;

              return (
                <div key={title} className={isCurrent ? 'floating-shadow-blue' : isCompleted ? 'floating-shadow-sm' : ''}>
                  <div
                    className={`octa-btn flex items-center justify-center gap-2 py-3 px-3.5 text-xs sm:text-sm transition-all duration-200 select-none ${
                      isCurrent
                        ? 'bg-blue-700 text-white font-black'
                        : isCompleted
                        ? 'bg-orange-500 text-white font-bold'
                        : 'bg-blue-100 text-blue-950 font-bold'
                    }`}
                  >
                    {isCompleted ? (
                      <CheckCircle2 className="w-4.5 h-4.5 text-white shrink-0" />
                    ) : (
                      <span
                        className={`octa-card-sm w-5 h-5 flex items-center justify-center text-xs font-black shrink-0 ${
                          isCurrent ? 'bg-white text-blue-800' : 'bg-blue-200 text-blue-900'
                        }`}
                      >
                        {stepNum}
                      </span>
                    )}
                    <span className="truncate font-black">{title}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
