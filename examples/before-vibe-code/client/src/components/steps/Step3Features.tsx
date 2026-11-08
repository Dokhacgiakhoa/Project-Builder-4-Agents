import React, { useState } from 'react';
import { Layers, Plus, Trash2, ArrowLeft, ArrowRight, Sparkles } from 'lucide-react';

interface FeatureItem {
  id?: number;
  title: string;
  description: string;
  priority: string;
}

interface Step3Props {
  features: FeatureItem[];
  setFeatures: React.Dispatch<React.SetStateAction<FeatureItem[]>>;
  onNext: () => void;
  onBack: () => void;
}

// List of common feature presets described in clear terms
const COMMON_FEATURES = [
  "User Authentication (Google & Email Sign-in)",
  "Role-Based Access Control & Admin Dashboard",
  "User Profile & Account Settings",
  "Smart Search & Multi-criteria Filtering",
  "Payment Gateway Integration (Stripe, PayPal, Card)",
  "Real-time Notifications & Alerts",
  "File Upload & Asset Storage Management",
  "Data Export & Reporting (Excel / PDF)"
];

export const Step3Features: React.FC<Step3Props> = ({
  features,
  setFeatures,
  onNext,
  onBack
}) => {
  const [newTitle, setNewTitle] = useState('');
  const [newPriority, setNewPriority] = useState('Medium');

  const handleAddFeature = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!newTitle.trim()) return;

    setFeatures(prev => [
      ...prev,
      {
        title: newTitle.trim(),
        description: '',
        priority: newPriority
      }
    ]);
    setNewTitle('');
  };

  const handleAddQuickFeature = (title: string) => {
    if (features.some(f => f.title.toLowerCase() === title.toLowerCase())) return;
    setFeatures(prev => [
      ...prev,
      {
        title,
        description: '',
        priority: 'Medium'
      }
    ]);
  };

  const handleRemoveFeature = (index: number) => {
    setFeatures(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="space-y-6">
      <div>
        <div className="octa-card-sm inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-950 text-sm font-black mb-3">
          <Layers className="w-4 h-4 text-orange-600" /> Step 3 / 6: Core Features
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-950 tracking-tight">What features does your system need?</h2>
        <p className="text-slate-700 text-base mt-1 font-semibold">
          Specify the primary actions users and administrators can execute in the application.
        </p>
      </div>

      {/* Quick Add Presets */}
      <div className="octa-card p-5 sm:p-6 bg-slate-50 space-y-3">
        <div className="flex items-center gap-2 text-sm font-black text-slate-900">
          <Sparkles className="w-4.5 h-4.5 text-orange-600" /> Click to add common feature presets:
        </div>
        <div className="flex flex-wrap gap-2.5">
          {COMMON_FEATURES.map((feat, i) => {
            const isAdded = features.some(f => f.title.toLowerCase() === feat.toLowerCase());
            return (
              <button
                key={i}
                type="button"
                disabled={isAdded}
                onClick={() => handleAddQuickFeature(feat)}
                className={`octa-btn px-4 py-2.5 text-sm font-black transition-all flex items-center gap-2 ${
                  isAdded
                    ? 'bg-slate-200 text-slate-500 cursor-not-allowed'
                    : 'bg-blue-100 hover:bg-blue-200 text-blue-950 shadow-2xs cursor-pointer'
                }`}
              >
                <Plus className="w-4 h-4 text-orange-600" /> {feat}
              </button>
            );
          })}
        </div>
      </div>

      {/* Input Custom Feature */}
      <form onSubmit={handleAddFeature} className="flex gap-2.5">
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Enter a feature name (e.g., Table reservation, Interactive clinic map)..."
          className="flex-1 px-5 py-3.5 bg-slate-100 text-base text-slate-950 placeholder:text-slate-400 font-bold rounded-lg focus:bg-white focus:shadow-md transition-all"
        />
        <select
          value={newPriority}
          onChange={(e) => setNewPriority(e.target.value)}
          className="octa-btn px-4 py-3.5 bg-slate-100 text-slate-950 text-sm font-black focus:outline-none cursor-pointer"
        >
          <option value="High">High Priority (MVP)</option>
          <option value="Medium">Medium Priority</option>
          <option value="Low">Low Priority (Post-MVP)</option>
        </select>
        <button
          type="submit"
          disabled={!newTitle.trim()}
          className="octa-btn floating-shadow-orange px-7 py-3.5 bg-orange-600 hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-black text-sm sm:text-base flex items-center gap-2 transition-colors cursor-pointer"
        >
          <Plus className="w-4.5 h-4.5" /> Add
        </button>
      </form>

      {/* Feature List */}
      <div className="space-y-2.5">
        <label className="block text-sm font-black uppercase tracking-wider text-slate-700">
          Selected Features ({features.length}):
        </label>
        {features.length === 0 ? (
          <div className="octa-card p-8 text-center text-slate-600 font-bold text-base bg-blue-50">
            No features selected yet. Click suggestions above or enter a custom requirement!
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-3 max-h-72 overflow-y-auto pr-1">
            {features.map((feat, index) => (
              <div key={index} className="floating-shadow-sm">
                <div className="octa-card flex items-center justify-between p-4 bg-white text-base group transition-all">
                  <div className="flex items-center gap-3.5">
                    <span className="octa-card-sm w-7 h-7 bg-blue-100 text-blue-900 flex items-center justify-center text-sm font-black">
                      {index + 1}
                    </span>
                    <span className="text-slate-950 font-bold text-base">{feat.title}</span>
                  </div>
                  <div className="flex items-center gap-3.5">
                    <span className={`octa-card-sm text-xs px-3 py-1.5 font-black uppercase ${
                      feat.priority === 'High'
                        ? 'bg-rose-100 text-rose-900'
                        : feat.priority === 'Low'
                        ? 'bg-blue-100 text-blue-950'
                        : 'bg-orange-100 text-orange-950'
                    }`}>
                      {feat.priority === 'High' ? 'High Priority' : feat.priority === 'Low' ? 'Low Priority' : 'Medium Priority'}
                    </span>
                    <button
                      type="button"
                      onClick={() => handleRemoveFeature(index)}
                      className="text-slate-500 hover:text-rose-600 transition-colors p-1.5 cursor-pointer"
                    >
                      <Trash2 className="w-4.5 h-4.5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="flex justify-between items-center pt-2">
        <button
          type="button"
          onClick={onBack}
          className="octa-btn inline-flex items-center gap-2 px-6 py-3 bg-blue-100 hover:bg-blue-200 text-blue-950 font-black text-base shadow-xs transition-all cursor-pointer"
        >
          <ArrowLeft className="w-4.5 h-4.5" /> Back
        </button>
        <button
          type="button"
          onClick={onNext}
          disabled={features.length === 0}
          className="octa-btn floating-shadow-blue inline-flex items-center gap-2 px-8 py-4 bg-blue-700 hover:bg-blue-800 disabled:opacity-50 disabled:cursor-not-allowed text-white font-black text-base transition-all cursor-pointer hover:-translate-y-0.5"
        >
          Continue: Architecture & Stack
          <ArrowRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};
