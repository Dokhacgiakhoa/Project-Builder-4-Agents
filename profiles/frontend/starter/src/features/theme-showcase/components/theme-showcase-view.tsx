import React, { useState } from 'react';
import { THEME_PRESETS } from '../data/presets';
import { ThemePresetId, ThemePreset } from '../types';
import { ThemeSwitcher } from './theme-switcher';
import { PreviewCard } from './preview-card';
import { Copy, Check, Palette, Code2, ExternalLink } from 'lucide-react';

export const ThemeShowcaseView: React.FC = () => {
  const [activeId, setActiveId] = useState<ThemePresetId>('linear-pro');
  const [copied, setCopied] = useState(false);

  const activePreset: ThemePreset =
    THEME_PRESETS.find((p) => p.id === activeId) ?? THEME_PRESETS[0];

  const handleCopyPrompt = async () => {
    try {
      if (navigator?.clipboard?.writeText) {
        await navigator.clipboard.writeText(activePreset.aiPromptSnippet);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch {
      // Fallback safe handling
      setCopied(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <div className="p-2 bg-gradient-to-tr from-sky-500 to-indigo-600 rounded-lg text-white">
                <Palette className="h-5 w-5" />
              </div>
              <h1 className="text-xl font-bold text-slate-900">
                UI/UX Design Archetypes & AI Visual DNA Studio
              </h1>
            </div>
            <p className="text-sm text-slate-600 mt-1 max-w-2xl">
              Choose and visually preview aesthetic style universes. Provide a Prompt to inject straight into
              Claude Code, Cursor, Antigravity so the AI generates a 100% consistent interface.
            </p>
          </div>

          <div className="flex items-center gap-2 self-start md:self-auto">
            <button
              onClick={handleCopyPrompt}
              className="flex items-center gap-1.5 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-semibold shadow-sm transition-all"
            >
              {copied ? (
                <>
                  <Check className="h-4 w-4 text-emerald-400" /> Prompt copied!
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4" /> Copy the Prompt for AI
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Preset Switcher Bar */}
      <ThemeSwitcher activePresetId={activeId} onSelectPreset={setActiveId} />

      {/* Main Grid: Live Preview & Token Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Live Interactive Preview */}
        <div className="lg:col-span-7 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
              <Code2 className="h-4 w-4 text-sky-600" /> Real Experience (Live Preview)
            </span>
            <span className="text-xs text-slate-500">
              Universe: <strong className="text-slate-800">{activePreset.universe}</strong>
            </span>
          </div>

          <PreviewCard preset={activePreset} />

          <p className="text-xs text-slate-500 italic">
            * Try interacting: click the "Run trial" button or type into the input to feel the visual response of each style.
          </p>
        </div>

        {/* Right Column: AI Prompt & Token Inspector */}
        <div className="lg:col-span-5 space-y-4">
          {/* AI Prompt Snippet Box */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                AI Visual DNA Prompt
              </span>
              <button
                onClick={handleCopyPrompt}
                className="text-xs text-sky-600 hover:text-sky-700 font-medium flex items-center gap-1"
              >
                {copied ? <Check className="h-3.5 w-3.5 text-emerald-600" /> : <Copy className="h-3.5 w-3.5" />}
                {copied ? 'Copied' : 'Copy'}
              </button>
            </div>

            <pre className="p-3 bg-slate-900 text-slate-100 rounded-lg text-[11px] leading-relaxed overflow-x-auto font-mono whitespace-pre-wrap">
              {activePreset.aiPromptSnippet}
            </pre>

            {/* Open Source References */}
            {Array.isArray(activePreset.openSourceRefs) && activePreset.openSourceRefs.length > 0 ? (
              <div className="pt-2 border-t border-slate-100">
                <span className="text-[11px] text-slate-500 block mb-1">Inspiration & Benchmark:</span>
                <div className="flex flex-wrap gap-1.5">
                  {activePreset.openSourceRefs.map((ref, idx) => (
                    <span
                      key={idx}
                      className="inline-flex items-center gap-1 text-[11px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded font-medium"
                    >
                      <ExternalLink className="h-2.5 w-2.5 text-slate-400" />
                      {ref}
                    </span>
                  ))}
                </div>
              </div>
            ) : null}
          </div>

          {/* Tokens Inspector Box */}
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-2 text-xs">
            <span className="font-bold uppercase tracking-wider text-slate-700 block text-[11px]">
              Extracted Design Tokens (Tailwind Classes)
            </span>
            <div className="space-y-1.5 text-[11px] font-mono text-slate-600">
              <div className="p-1.5 bg-slate-50 rounded border border-slate-100">
                <strong className="text-slate-800">Card:</strong> {activePreset.tokens.cardClass}
              </div>
              <div className="p-1.5 bg-slate-50 rounded border border-slate-100">
                <strong className="text-slate-800">Primary Button:</strong> {activePreset.tokens.primaryButtonClass}
              </div>
              <div className="p-1.5 bg-slate-50 rounded border border-slate-100">
                <strong className="text-slate-800">Badge:</strong> {activePreset.tokens.badgeClass}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
