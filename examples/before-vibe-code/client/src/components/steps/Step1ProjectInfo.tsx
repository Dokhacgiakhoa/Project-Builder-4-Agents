import React from 'react';
import { Lightbulb, Rocket, ArrowRight } from 'lucide-react';

interface Step1Props {
  projectName: string;
  setProjectName: (val: string) => void;
  description: string;
  setDescription: (val: string) => void;
  onNext: () => void;
}

const TEMPLATES = [
  {
    name: "Hotel & Homestay Booking Platform",
    desc: "Search accommodations, preview 360-degree rooms, and pay seamlessly via integrated digital wallets."
  },
  {
    name: "Learning Management System (LMS)",
    desc: "Enables instructors to publish video courses, students to complete quizzes, and auto-issues certificates."
  },
  {
    name: "Expense Tracker & Personal Finance App",
    desc: "Tracks daily expenses, analyzes spending patterns, and provides intelligent budget recommendations."
  }
];

export const Step1ProjectInfo: React.FC<Step1Props> = ({
  projectName,
  setProjectName,
  description,
  setDescription,
  onNext
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!projectName.trim() || !description.trim()) return;
    onNext();
  };

  const applyTemplate = (tpl: { name: string; desc: string }) => {
    setProjectName(tpl.name);
    setDescription(tpl.desc);
  };

  return (
    <div className="space-y-6">
      <div>
        <div className="octa-card-sm inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-950 text-sm font-black mb-3">
          <Rocket className="w-4 h-4 text-orange-600" /> Step 1 / 6: Project Concept
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-950 tracking-tight">What do you want to build?</h2>
        <p className="text-slate-700 text-base mt-1 font-semibold">
          Describe your idea in plain language. Technical architecture will be inferred automatically.
        </p>
      </div>

      {/* Preset Ideas (Border-free - Floating Shadow) */}
      <div className="octa-card p-5 sm:p-6 bg-slate-50 space-y-3.5">
        <div className="flex items-center gap-2 text-sm font-black text-slate-900">
          <Lightbulb className="w-4.5 h-4.5 text-orange-600" /> Or pick a sample project to get started:
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
          {TEMPLATES.map((tpl, i) => (
            <div key={i} className="floating-shadow-sm">
              <button
                type="button"
                onClick={() => applyTemplate(tpl)}
                className="octa-card w-full text-left p-4 bg-white hover:bg-blue-50 transition-all text-sm group cursor-pointer"
              >
                <div className="font-black text-slate-950 group-hover:text-blue-700 transition-colors text-base">{tpl.name}</div>
                <div className="text-slate-700 line-clamp-2 mt-1.5 leading-relaxed font-medium text-sm">{tpl.desc}</div>
              </button>
            </div>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-2">
          <label className="block text-base font-black text-slate-950">
            Project Name <span className="text-orange-600">*</span>
          </label>
          <input
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="e.g. FoodHub, EcoStay, SmartTutor..."
            required
            className="w-full px-5 py-3.5 bg-slate-100 text-base text-slate-950 placeholder:text-slate-400 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all"
          />
        </div>

        <div className="space-y-2">
          <label className="block text-base font-black text-slate-950">
            Summary & Objectives <span className="text-orange-600">*</span>
          </label>
          <textarea
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe your product in 2-3 sentences: what problem it solves and what core actions users perform..."
            required
            className="w-full px-5 py-3.5 bg-slate-100 text-base text-slate-950 placeholder:text-slate-400 resize-none font-bold rounded-lg focus:bg-white focus:shadow-md transition-all leading-relaxed"
          />
        </div>

        <div className="flex justify-end pt-2">
          <button
            type="submit"
            disabled={!projectName.trim() || !description.trim()}
            className="octa-btn floating-shadow-blue inline-flex items-center gap-2 px-8 py-4 bg-blue-700 hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed text-white font-black text-base transition-all cursor-pointer hover:-translate-y-0.5"
          >
            Continue: Target Audience
            <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  );
};
