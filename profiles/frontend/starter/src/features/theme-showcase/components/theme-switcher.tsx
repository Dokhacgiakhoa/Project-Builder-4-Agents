import React from 'react';
import { THEME_PRESETS } from '../data/presets';
import { ThemePresetId } from '../types';
import { Sparkles } from 'lucide-react';

interface ThemeSwitcherProps {
  activePresetId: ThemePresetId;
  onSelectPreset: (id: ThemePresetId) => void;
}

export const ThemeSwitcher: React.FC<ThemeSwitcherProps> = ({
  activePresetId,
  onSelectPreset,
}) => {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm">
      <div className="flex items-center gap-2 mb-3 px-1">
        <Sparkles className="h-4 w-4 text-sky-600" />
        <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
          Choose an Aesthetic Style (UI/UX Archetypes)
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-2">
        {THEME_PRESETS.map((preset) => {
          const isActive = preset.id === activePresetId;
          return (
            <button
              key={preset.id}
              onClick={() => onSelectPreset(preset.id)}
              className={`flex flex-col items-start text-left p-2.5 rounded-lg border text-xs transition-all ${
                isActive
                  ? 'border-sky-600 bg-sky-50/80 shadow-sm ring-1 ring-sky-500'
                  : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50'
              }`}
            >
              <span className={`font-semibold ${isActive ? 'text-sky-900' : 'text-slate-800'}`}>
                {preset.name}
              </span>
              <span className="text-[10px] text-slate-500 line-clamp-1 mt-0.5">
                {preset.universe}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
