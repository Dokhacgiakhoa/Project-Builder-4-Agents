import React, { useState } from 'react';
import { ThemePreset } from '../types';
import { Terminal, Shield, Zap, Sparkles, X, Minus, Square } from 'lucide-react';

interface PreviewCardProps {
  preset: ThemePreset;
}

export const PreviewCard: React.FC<PreviewCardProps> = ({ preset }) => {
  const [taskInput, setTaskInput] = useState('Initialize a Microservice with an AI Agent');
  const [clickCount, setClickCount] = useState(0);

  const { tokens } = preset;

  return (
    <div className={`transition-all duration-300 ${tokens.containerClass}`}>
      {/* XP specific Window Header */}
      {preset.id === 'win-xp' ? (
        <div className={tokens.headerClass}>
          <div className={tokens.titleClass}>
            <span className="w-3.5 h-3.5 bg-white/20 rounded-sm flex items-center justify-center text-[9px]">
              🚀
            </span>
            <span>Task Manager - Luna Blue Edition</span>
          </div>
          <div className="flex items-center gap-1">
            <button className="w-4 h-4 bg-[#0055ea] border border-white text-white flex items-center justify-center text-[9px] hover:bg-blue-700">
              <Minus className="h-2.5 w-2.5" />
            </button>
            <button className="w-4 h-4 bg-[#0055ea] border border-white text-white flex items-center justify-center text-[9px] hover:bg-blue-700">
              <Square className="h-2 w-2" />
            </button>
            <button className="w-4 h-4 bg-[#e81123] border border-white text-white flex items-center justify-center text-[9px] font-bold hover:bg-red-700">
              <X className="h-2.5 w-2.5" />
            </button>
          </div>
        </div>
      ) : (
        <div className={tokens.headerClass}>
          <div>
            <div className={tokens.titleClass}>
              {preset.id === 'cyberpunk-hud' && <Terminal className="h-4 w-4 text-cyan-400" />}
              {preset.id === 'terminal-tui' && <span>&gt;</span>}
              {preset.name}
            </div>
            <p className={tokens.subtitleClass}>{preset.tagline}</p>
          </div>

          <div className="flex items-center gap-2">
            <span className={tokens.badgeClass}>
              {preset.id === 'terminal-tui' ? '[STATUS: READY]' : 'ACTIVE PRESET'}
            </span>
          </div>
        </div>
      )}

      {/* Cyberpunk HUD Coordinate Line */}
      {preset.id === 'cyberpunk-hud' && (
        <div className="flex justify-between text-[10px] text-cyan-500/80 mb-3 border-b border-cyan-900/40 pb-1">
          <span>SYS.SEC // AGENT-04</span>
          <span>COORDINATES: 21.0285° N, 105.8542° E</span>
        </div>
      )}

      {/* Main Inner Card */}
      <div className={tokens.cardClass}>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4" />
            <span className="text-xs font-semibold">Executing Task (Agent Task)</span>
          </div>
          <span className={tokens.accentTextClass}>
            {preset.id === 'terminal-tui' ? 'PORT: 8080 // OK' : 'v2.4.0-Production'}
          </span>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-[11px] mb-1 font-medium opacity-80">
              {preset.id === 'terminal-tui' ? '$ INPUT_TASK_NAME:' : 'Task name:'}
            </label>
            <input
              type="text"
              value={taskInput}
              onChange={(e) => setTaskInput(e.target.value)}
              className={tokens.inputClass}
              placeholder="Enter a task name..."
            />
          </div>

          {/* Metric Stats */}
          <div className="grid grid-cols-2 gap-3 pt-1">
            <div className="p-2.5 rounded-lg bg-black/5 dark:bg-white/5 border border-current/10">
              <span className="text-[10px] opacity-70 block">Interaction count</span>
              <span className="text-base font-bold flex items-center gap-1">
                <Zap className="h-3.5 w-3.5" /> {clickCount} times
              </span>
            </div>
            <div className="p-2.5 rounded-lg bg-black/5 dark:bg-white/5 border border-current/10">
              <span className="text-[10px] opacity-70 block">Agent status</span>
              <span className="text-base font-bold flex items-center gap-1">
                <Sparkles className="h-3.5 w-3.5" /> Ready
              </span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2 pt-2">
            <button
              onClick={() => setClickCount((prev) => prev + 1)}
              className={tokens.primaryButtonClass}
            >
              {preset.id === 'terminal-tui' ? '[ EXECUTE_TASK ]' : 'Run trial'}
            </button>
            <button
              onClick={() => setClickCount(0)}
              className={tokens.secondaryButtonClass}
            >
              {preset.id === 'terminal-tui' ? '[ RESET ]' : 'Reset'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
