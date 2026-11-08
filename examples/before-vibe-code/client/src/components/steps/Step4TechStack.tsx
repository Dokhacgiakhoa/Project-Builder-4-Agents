import React, { useState } from 'react';
import { 
  ArrowLeft, ArrowRight, Globe, Sparkles, 
  SlidersHorizontal, Check, Database, Server
} from 'lucide-react';
import { SOLUTION_PACKS, QUALITY_STANDARDS, SolutionPack } from './tech-stack-presets';

interface Step4Props {
  frontendStack: string;
  setFrontendStack: (val: string) => void;
  backendStack: string;
  setBackendStack: (val: string) => void;
  databaseStack: string;
  setDatabaseStack: (val: string) => void;
  nonFunctionalReqs: string[];
  setNonFunctionalReqs: React.Dispatch<React.SetStateAction<string[]>>;
  onNext: () => void;
  onBack: () => void;
}

export const Step4TechStack: React.FC<Step4Props> = ({
  frontendStack,
  setFrontendStack,
  backendStack,
  setBackendStack,
  databaseStack,
  setDatabaseStack,
  nonFunctionalReqs,
  setNonFunctionalReqs,
  onNext,
  onBack
}) => {
  const [selectedPackId, setSelectedPackId] = useState<string>('enterprise');
  const [showAdvanced, setShowAdvanced] = useState<boolean>(false);

  const applyPack = (pack: SolutionPack) => {
    setSelectedPackId(pack.id);
    setBackendStack(pack.backend);
    setDatabaseStack(pack.database);
    setFrontendStack(pack.frontend);
    setNonFunctionalReqs(pack.nfrs);
  };

  const toggleStandard = (title: string) => {
    setNonFunctionalReqs(prev =>
      prev.includes(title) ? prev.filter(t => t !== title) : [...prev, title]
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="octa-card-sm inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-950 text-sm font-black mb-3">
          <Sparkles className="w-4 h-4 text-orange-600" /> Step 4 / 6: Architecture & Stack Selection
        </div>
        <h2 className="text-2xl sm:text-3xl font-black text-slate-950 tracking-tight">
          Which architectural path fits your project?
        </h2>
        <p className="text-slate-700 text-base mt-1 font-semibold">
          Select the package that best fits your product requirements and team capabilities.
        </p>
      </div>

      {/* 4 Solution Packs */}
      <div className="space-y-3">
        <label className="block text-sm font-black uppercase tracking-wider text-slate-900">
          Select 1 architecture package for your solution:
        </label>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {SOLUTION_PACKS.map((pack) => {
            const isSelected = selectedPackId === pack.id;
            const Icon = pack.icon;

            return (
              <div key={pack.id} className={isSelected ? 'floating-shadow-blue' : 'floating-shadow-sm'}>
                <button
                  type="button"
                  onClick={() => applyPack(pack)}
                  className={`octa-card w-full text-left p-5 sm:p-6 transition-all flex flex-col justify-between h-full cursor-pointer relative ${
                    isSelected
                      ? 'bg-blue-700 text-white'
                      : 'bg-white hover:bg-blue-50/70 text-slate-900'
                  }`}
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className={`octa-card-sm text-[11px] font-black uppercase px-2.5 py-1 ${
                        isSelected ? 'bg-orange-500 text-white' : 'bg-blue-100 text-blue-950'
                      }`}>
                        {pack.tag}
                      </span>
                      {isSelected && (
                        <div className="octa-card-sm w-6 h-6 bg-orange-500 text-white flex items-center justify-center shadow-xs">
                          <Check className="w-4 h-4 stroke-[3]" />
                        </div>
                      )}
                    </div>

                    <div className="flex items-start gap-3.5">
                      <div className={`octa-card-sm w-12 h-12 flex items-center justify-center shrink-0 ${
                        isSelected ? 'bg-white text-blue-800 shadow-sm' : 'bg-blue-100 text-blue-800'
                      }`}>
                        <Icon className="w-6 h-6" />
                      </div>
                      <div>
                        <div className={`font-black text-base sm:text-lg ${isSelected ? 'text-white' : 'text-slate-950'}`}>
                          {pack.title}
                        </div>
                        <p className={`text-xs sm:text-sm mt-1 leading-relaxed font-medium ${
                          isSelected ? 'text-blue-100' : 'text-slate-600'
                        }`}>
                          {pack.desc}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Summary Tech underneath */}
                  <div className={`mt-4 pt-3 border-t text-[11px] font-bold flex flex-wrap gap-2 ${
                    isSelected ? 'border-blue-600 text-blue-200' : 'border-slate-100 text-slate-500'
                  }`}>
                    <span>💻 {pack.frontend.split('(')[0].trim()}</span>
                    <span>•</span>
                    <span>⚙️ {pack.backend.split('(')[0].trim()}</span>
                    <span>•</span>
                    <span>🗄️ {pack.database.split('(')[0].trim()}</span>
                  </div>
                </button>
              </div>
            );
          })}
        </div>
      </div>

      {/* Advanced Toggle */}
      <div className="pt-1">
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="octa-btn inline-flex items-center gap-2 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs sm:text-sm font-black transition-colors cursor-pointer"
        >
          <SlidersHorizontal className="w-4 h-4 text-blue-600" />
          <span>{showAdvanced ? 'Hide advanced settings ▲' : 'Advanced developer? Click to customize language & database ▼'}</span>
        </button>

        {/* Detailed Tech Selectors */}
        {showAdvanced && (
          <div className="mt-4 p-5 octa-card bg-slate-50 space-y-4">
            <div className="text-xs font-black uppercase text-slate-800">
              Advanced Technical Customization:
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                  <Server className="w-3.5 h-3.5 text-blue-600" /> Backend Stack
                </label>
                <select
                  value={backendStack}
                  onChange={(e) => setBackendStack(e.target.value)}
                  className="w-full px-4 py-2.5 bg-white text-xs sm:text-sm text-slate-950 font-bold rounded-lg focus:outline-none cursor-pointer shadow-xs"
                >
                  <option value="ASP.NET Core 10 Web API (Clean Architecture / Repository)">ASP.NET Core 10 (.NET C#)</option>
                  <option value="Java Spring Boot 3.x (REST API + Spring Security + JPA)">Java Spring Boot 3.x</option>
                  <option value="Python FastAPI (High Performance Async + Pydantic)">Python FastAPI</option>
                  <option value="Python Django REST Framework (Full-featured)">Python Django</option>
                  <option value="Node.js / NestJS (TypeScript + Enterprise Modular)">Node.js NestJS (TypeScript)</option>
                  <option value="Node.js / Express.js (Lightweight REST API)">Node.js Express</option>
                  <option value="Golang (Gin Gonic / Fiber Microservices)">Golang (Gin / Fiber)</option>
                  <option value="PHP Laravel 11 (Eloquent ORM + MVC)">PHP Laravel 11</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                  <Database className="w-3.5 h-3.5 text-orange-600" /> Database Stack
                </label>
                <select
                  value={databaseStack}
                  onChange={(e) => setDatabaseStack(e.target.value)}
                  className="w-full px-4 py-2.5 bg-white text-xs sm:text-sm text-slate-950 font-bold rounded-lg focus:outline-none cursor-pointer shadow-xs"
                >
                  <option value="SQL Server + Entity Framework Core 10">SQL Server (Microsoft)</option>
                  <option value="PostgreSQL + Prisma / Dapper / Hibernate">PostgreSQL (High Performance RDBMS)</option>
                  <option value="MySQL / MariaDB + TypeORM / JPA">MySQL / MariaDB</option>
                  <option value="MongoDB + Mongoose (NoSQL Document Store)">MongoDB (NoSQL Document)</option>
                  <option value="SQLite (Lightweight Embedded Database)">SQLite (Lightweight Embedded)</option>
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
                  <Globe className="w-3.5 h-3.5 text-blue-600" /> Frontend Framework
                </label>
                <select
                  value={frontendStack}
                  onChange={(e) => setFrontendStack(e.target.value)}
                  className="w-full px-4 py-2.5 bg-white text-xs sm:text-sm text-slate-950 font-bold rounded-lg focus:outline-none cursor-pointer shadow-xs"
                >
                  <option value="React 19 + TypeScript + Tailwind CSS (SPA Client)">React 19 + TypeScript</option>
                  <option value="Next.js 15 (Fullstack SSR / App Router / RSC)">Next.js 15 (React SSR)</option>
                  <option value="Vue.js 3 + Vite + Pinia + Tailwind CSS">Vue.js 3 + Vite</option>
                  <option value="Flutter (Dart Cross-Platform Mobile / Web)">Flutter (Mobile App)</option>
                  <option value="Angular 18 (Enterprise Standalone Components)">Angular 18</option>
                </select>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Quality Standards Checklist */}
      <div className="space-y-3">
        <label className="block text-sm font-black uppercase tracking-wider text-slate-900">
          Quality standards and non-functional constraints for AI code generation:
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {QUALITY_STANDARDS.map((item) => {
            const isChecked = nonFunctionalReqs.includes(item.title);
            const Icon = item.icon;

            return (
              <div key={item.id} className={isChecked ? 'floating-shadow-blue' : 'floating-shadow-sm'}>
                <button
                  type="button"
                  onClick={() => toggleStandard(item.title)}
                  className={`octa-card w-full text-left p-4.5 transition-all flex flex-col justify-between h-full cursor-pointer ${
                    isChecked
                      ? 'bg-blue-700 text-white'
                      : 'bg-white hover:bg-blue-50/70 text-slate-900'
                  }`}
                >
                  <div className="space-y-2.5">
                    <div className="flex items-center justify-between">
                      <div className={`octa-card-sm w-10 h-10 flex items-center justify-center shrink-0 ${
                        isChecked ? 'bg-orange-500 text-white shadow-xs' : 'bg-blue-100 text-blue-800'
                      }`}>
                        <Icon className="w-5 h-5" />
                      </div>
                      {isChecked && (
                        <div className="octa-card-sm w-5 h-5 bg-orange-500 text-white flex items-center justify-center shadow-2xs">
                          <Check className="w-3.5 h-3.5 stroke-[3]" />
                        </div>
                      )}
                    </div>
                    <div className={`font-black text-sm sm:text-base leading-snug ${isChecked ? 'text-white' : 'text-slate-950'}`}>
                      {item.title}
                    </div>
                  </div>
                  <p className={`text-xs mt-2 leading-relaxed font-medium ${isChecked ? 'text-blue-100' : 'text-slate-600'}`}>
                    {item.desc}
                  </p>
                </button>
              </div>
            );
          })}
        </div>
      </div>

      {/* Navigation Buttons */}
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
          className="octa-btn floating-shadow-blue inline-flex items-center gap-2 px-8 py-4 bg-blue-700 hover:bg-blue-800 text-white font-black text-base transition-all cursor-pointer hover:-translate-y-0.5"
        >
          Continue: Analyze & Generate Prompt
          <ArrowRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};
