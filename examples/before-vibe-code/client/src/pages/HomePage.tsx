import React, { useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, FileText, CheckCircle2, Layers, Terminal } from 'lucide-react';
import gsap from 'gsap';

export const HomePage: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Hero entrance animation
      gsap.fromTo(
        '.gsap-hero-item',
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, stagger: 0.12, duration: 0.7, ease: 'power2.out', clearProps: 'transform' }
      );

      // Comparison cards
      gsap.fromTo(
        '.gsap-comp-card',
        { opacity: 0, y: 25 },
        { opacity: 1, y: 0, stagger: 0.15, duration: 0.7, ease: 'power2.out', delay: 0.2, clearProps: 'transform' }
      );

      // Pillars cards
      gsap.fromTo(
        '.gsap-pillar-card',
        { opacity: 0, y: 25 },
        { opacity: 1, y: 0, stagger: 0.12, duration: 0.7, ease: 'power2.out', delay: 0.35, clearProps: 'transform' }
      );
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={containerRef} className="space-y-16 py-10 sm:py-16 relative z-10 w-full max-w-[85%] mx-auto px-2 sm:px-4">
      {/* 1. Hero Section */}
      <section className="max-w-5xl mx-auto text-center px-4 space-y-6">
        <div className="gsap-hero-item inline-block">
          <div className="octa-btn inline-flex items-center gap-2 px-5 py-2.5 bg-blue-100 text-blue-950 text-sm font-black shadow-xs">
            <Sparkles className="w-4 h-4 text-orange-500" />
            <span>The Essential Pre-Coding Toolkit for Developers & AI Agents</span>
          </div>
        </div>

        <h1 className="gsap-hero-item text-4xl sm:text-5xl md:text-6xl font-black text-slate-950 tracking-tight leading-tight">
          Prepare <span className="text-blue-600">Context</span> & <span className="text-orange-500">Architecture</span> Before Letting AI Code
        </h1>

        <p className="gsap-hero-item text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto leading-relaxed font-medium">
          Stop letting AI guess project architecture! <strong>Before Vibe Code</strong> guides you step-by-step through generating 
          SRS requirements, system architecture diagrams, and comprehensive <strong>Master Prompts</strong> in minutes.
        </p>

        <div className="gsap-hero-item flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
          <Link
            to="/studio"
            className="octa-btn w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-black text-base shadow-md shadow-blue-600/25 transition-all duration-200 hover:scale-105 cursor-pointer"
          >
            <Sparkles className="w-5 h-5 text-orange-300" /> Start Setup Prompt
            <ArrowRight className="w-5 h-5" />
          </Link>
          <Link
            to="/contact"
            className="octa-btn w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 bg-white hover:bg-slate-50 text-slate-800 font-bold text-base shadow-sm transition-all duration-200 cursor-pointer"
          >
            What is Vibe Coding?
          </Link>
        </div>
      </section>

      {/* 2. Problem & Solution Comparison (Border-free) */}
      <section className="w-full">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Box 1: Without Before Vibe Code */}
          <div className="gsap-comp-card opacity-100 floating-shadow">
            <div className="octa-card p-8 sm:p-10 bg-rose-50 space-y-5">
              <div className="octa-card-sm inline-flex items-center gap-2 px-3.5 py-1.5 bg-rose-200 text-rose-950 text-xs sm:text-sm font-black uppercase tracking-wider">
                Vibe Coding Without Guardrails ❌
              </div>
              <h3 className="text-2xl font-black text-rose-950">Brittle codebase, frequent regressions</h3>
              <ul className="space-y-3.5 text-base text-slate-800 font-semibold">
                <li className="flex items-start gap-3">
                  <span className="text-rose-600 font-black text-lg leading-none">✕</span>
                  <span>AI invents arbitrary file layouts without clean architectural boundaries.</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-rose-600 font-black text-lg leading-none">✕</span>
                  <span>Basic security standards are forgotten (plain passwords, missing JWTs).</span>
                </li>
                <li className="flex items-start gap-3">
                  <span className="text-rose-600 font-black text-lg leading-none">✕</span>
                  <span>As scope expands, fixing one module quietly breaks another (regressions).</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Box 2: With Before Vibe Code */}
          <div className="gsap-comp-card opacity-100 floating-shadow">
            <div className="octa-card p-8 sm:p-10 bg-blue-50 space-y-5">
              <div className="octa-card-sm inline-flex items-center gap-2 px-3.5 py-1.5 bg-orange-500 text-white text-xs sm:text-sm font-black uppercase tracking-wider">
                With Before Vibe Code Pre-Scaffolding ✅
              </div>
              <h3 className="text-2xl font-black text-blue-950">Resilient architecture, predictable AI output</h3>
              <ul className="space-y-3.5 text-base text-slate-900 font-bold">
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                  <span>Pre-generated <code className="text-blue-900 bg-blue-200 px-2 py-0.5 font-mono text-sm font-black">REQUIREMENTS.md</code> and <code className="text-blue-900 bg-blue-200 px-2 py-0.5 font-mono text-sm font-black">ARCHITECTURE.md</code>.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                  <span>Includes calibrated <strong>Master System Prompts</strong> for Cursor, Copilot, or Claude Code.</span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
                  <span>Follows industry architectural patterns (Repository & Service Pattern).</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 3. 3-Pillar Features (Border-free) */}
      <section className="w-full space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-3xl sm:text-4xl font-black text-slate-950">3 Pillars Delivered Across 6 Steps</h2>
          <p className="text-base text-slate-600 font-bold">Bundled into standard Markdown and ZIP download packages</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-7">
          <div className="gsap-pillar-card hover:-translate-y-1.5 transition-transform duration-300 opacity-100 floating-shadow">
            <div className="octa-card bg-white p-8 space-y-4">
              <div className="octa-card-sm w-13 h-13 bg-blue-600 text-white flex items-center justify-center shadow-sm">
                <FileText className="w-6.5 h-6.5" />
              </div>
              <h3 className="font-black text-xl text-slate-950">1. Requirements Document (SRS)</h3>
              <p className="text-base text-slate-600 leading-relaxed font-normal">
                Extracts structured functional (FR) and non-functional requirements (NFR) with strict priorities.
              </p>
            </div>
          </div>

          <div className="gsap-pillar-card hover:-translate-y-1.5 transition-transform duration-300 opacity-100 floating-shadow">
            <div className="octa-card bg-white p-8 space-y-4">
              <div className="octa-card-sm w-13 h-13 bg-orange-500 text-white flex items-center justify-center shadow-sm">
                <Layers className="w-6.5 h-6.5" />
              </div>
              <h3 className="font-black text-xl text-slate-950">2. Mermaid Architecture Diagrams</h3>
              <p className="text-base text-slate-600 leading-relaxed font-normal">
                Generates Mermaid diagrams visualizing data flow from client layers to server and database tiers.
              </p>
            </div>
          </div>

          <div className="gsap-pillar-card hover:-translate-y-1.5 transition-transform duration-300 opacity-100 floating-shadow">
            <div className="octa-card bg-white p-8 space-y-4">
              <div className="octa-card-sm w-13 h-13 bg-slate-900 text-white flex items-center justify-center shadow-sm">
                <Terminal className="w-6.5 h-6.5" />
              </div>
              <h3 className="font-black text-xl text-slate-950">3. Master System Prompt</h3>
              <p className="text-base text-slate-600 leading-relaxed font-normal">
                A comprehensive context prompt ready to feed into AI Coding Assistants without hallucination.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Bottom CTA Card */}
      <section className="w-full text-center">
        <div className="floating-shadow-lg">
          <div className="octa-card-lg bg-white p-10 sm:p-16 space-y-6">
            <h2 className="text-3xl sm:text-5xl font-black text-slate-950">Ready to Vibe Code with Guardrails?</h2>
            <p className="text-base sm:text-lg text-slate-600 max-w-xl mx-auto leading-relaxed font-medium">
              Bring your product vision. Let Before Vibe Code scaffold your architecture.
            </p>
            <div className="pt-2">
              <Link
                to="/studio"
                className="octa-btn inline-flex items-center gap-2 px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-black text-base shadow-md shadow-orange-500/25 transition-all duration-200 hover:scale-105 cursor-pointer"
              >
                Launch Setup Prompt <ArrowRight className="w-5 h-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
