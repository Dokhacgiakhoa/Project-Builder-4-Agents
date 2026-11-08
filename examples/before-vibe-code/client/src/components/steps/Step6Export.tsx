import React, { useState } from 'react';
import { Download, Copy, Check, FileText, Code2, Sparkles, RefreshCw, Layers } from 'lucide-react';
import confetti from 'canvas-confetti';

interface Step6Props {
  projectName: string;
  description: string;
  targetAudience: string;
  features: { title: string; priority: string }[];
  frontendStack: string;
  backendStack: string;
  databaseStack: string;
  nonFunctionalReqs: string[];
  onRestart: () => void;
}

export const Step6Export: React.FC<Step6Props> = ({
  projectName,
  description,
  targetAudience,
  features,
  frontendStack,
  backendStack,
  databaseStack,
  nonFunctionalReqs,
  onRestart
}) => {
  const [activeTab, setActiveTab] = useState<'prompt' | 'srs' | 'arch'>('prompt');
  const [isCopied, setIsCopied] = useState(false);

  // Trigger confetti on mount
  React.useEffect(() => {
    try {
      confetti({
        particleCount: 90,
        spread: 80,
        origin: { y: 0.6 }
      });
    } catch {
      // ignore
    }
  }, []);

  // 1. Generate Master Prompt (Adaptive to any selected Tech Stack)
  const masterPrompt = `# SYSTEM PROMPT FOR AI CODING AGENT (VIBE CODE - MULTI-STACK ARCHITECTURE)
**Role:** You are a Senior Fullstack Software Engineer & Solution Architect.
**Task:** Implement full codebase for "${projectName}" with Backend **${backendStack.split('(')[0].trim()}**, Database **${databaseStack.split('(')[0].trim()}**, and Frontend **${frontendStack.split('(')[0].trim()}**.

## 1. PROJECT OVERVIEW & GOALS
- **Project Name:** ${projectName}
- **Business Description:** ${description}
- **Target Audience:** ${targetAudience}

## 2. SPECIFIED TECH STACK
- **Backend Core:** ${backendStack}
- **Database & ORM:** ${databaseStack}
- **Frontend Client:** ${frontendStack}

## 3. CORE FUNCTIONAL REQUIREMENTS
${features.map((f, i) => `${i + 1}. **${f.title}** (Priority: ${f.priority})`).join('\n')}

## 4. QUALITY STANDARDS & NON-FUNCTIONAL REQUIREMENTS
${nonFunctionalReqs.map(n => `- ${n}`).join('\n')}

## 5. ENGINEERING BEST PRACTICES & IMPLEMENTATION PHASES
1. **Clean Architecture:** Strictly isolate Controllers/Routers, Business Services/Use Cases, Repositories/Data Access, and Models/Entities.
2. **Async & Performance:** Use \`async/await\` throughout, paginate list queries, and validate all inputs with strict DTOs/schemas.
3. **Security & Resilience:** Guard boundary operations, hash passwords securely, and configure global error handling middleware.
4. **Clean Code:** Adhere to SOLID principles, use meaningful domain terminology, and document complex business logic.
`;

  // 2. Generate SRS Markdown
  const srsMarkdown = `# Software Requirements Specification (SRS)
**Project Name:** ${projectName}
**Tech Stack:** ${backendStack.split('(')[0].trim()} + ${databaseStack.split('(')[0].trim()} + ${frontendStack.split('(')[0].trim()}
**Date:** ${new Date().toLocaleDateString('vi-VN')}

## 1. Product Objectives
${description}

## 2. Target Audience
${targetAudience}

## 3. Functional Requirements
${features.map((f, i) => `### FR-${(i + 1).toString().padStart(2, '0')}: ${f.title}
- **Priority:** ${f.priority}
- **Description:** Users can execute ${f.title.toLowerCase()} with clear validations and feedback.
`).join('\n')}

## 4. Non-Functional Requirements & Constraints (NFR)
${nonFunctionalReqs.map(n => `- ${n}`).join('\n')}
`;

  // 3. Generate Architecture Markdown
  const archMarkdown = `# System Architecture & Design
**Project Name:** ${projectName}

## 1. Technology Structure
- **Server:** ${backendStack}
- **Database:** ${databaseStack}
- **Client:** ${frontendStack}

## 2. System Architecture Diagram (Mermaid.js)

\`\`\`mermaid
graph TD
    Client["${frontendStack.split('(')[0].trim()}"] -->|RESTful API / JSON / GraphQL| API["${backendStack.split('(')[0].trim()}"]
    
    subgraph Application Server Architecture
        API --> Controllers["API Endpoints / Routers"]
        Controllers --> Services["Services Layer (Business Logic)"]
        Services --> Repositories["Repositories / Data Access Layer"]
        Repositories --> DBContext["Database Engine / ORM"]
    end

    DBContext --> DB[("${databaseStack.split('(')[0].trim()}")]
\`\`\`
`;

  const handleCopyPrompt = () => {
    navigator.clipboard.writeText(masterPrompt);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 2000);
  };

  const handleDownloadFile = (filename: string, content: string) => {
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleDownloadAll = () => {
    handleDownloadFile('MASTER_PROMPT.md', masterPrompt);
    setTimeout(() => handleDownloadFile('REQUIREMENTS.md', srsMarkdown), 200);
    setTimeout(() => handleDownloadFile('ARCHITECTURE.md', archMarkdown), 400);
  };

  return (
    <div className="space-y-6">
      {/* Header Banner (Border-free) */}
      <div className="octa-card floating-shadow-sm p-6 sm:p-8 bg-blue-50 flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
        <div className="space-y-1.5">
          <div className="inline-flex items-center gap-2 text-blue-900 text-sm font-black uppercase tracking-wider">
            <Sparkles className="w-4.5 h-4.5 text-orange-600" /> Architectural Context Ready!
          </div>
          <h2 className="text-2xl sm:text-3xl font-black text-slate-950">Artifacts & Master System Prompt Generated</h2>
          <p className="text-base text-slate-700 font-semibold">
            Customized specifically for your selected Tech Stack ({backendStack.split('(')[0].trim()} + {frontendStack.split('(')[0].trim()})!
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={handleCopyPrompt}
            className="octa-btn floating-shadow-orange inline-flex items-center gap-2 px-7 py-3.5 bg-orange-600 hover:bg-orange-700 text-white font-black text-sm sm:text-base transition-transform cursor-pointer hover:-translate-y-0.5"
          >
            {isCopied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
            {isCopied ? 'Master Prompt Copied!' : 'Copy Master Prompt (1-Click)'}
          </button>
          <button
            type="button"
            onClick={handleDownloadAll}
            className="octa-btn inline-flex items-center gap-2 px-6 py-3.5 bg-blue-100 hover:bg-blue-200 text-blue-950 font-black text-sm sm:text-base shadow-xs transition-colors cursor-pointer"
          >
            <Download className="w-5 h-5 text-blue-800" /> Download All (.md)
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-3">
        <button
          type="button"
          onClick={() => setActiveTab('prompt')}
          className={`octa-btn py-3 px-5 text-sm sm:text-base transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'prompt'
              ? 'floating-shadow-blue bg-blue-700 text-white font-black'
              : 'bg-blue-100 text-blue-950 font-bold hover:bg-blue-200'
          }`}
        >
          <Sparkles className="w-4 h-4" /> MASTER_PROMPT.md
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('srs')}
          className={`octa-btn py-3 px-5 text-sm sm:text-base transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'srs'
              ? 'floating-shadow-blue bg-blue-700 text-white font-black'
              : 'bg-blue-100 text-blue-950 font-bold hover:bg-blue-200'
          }`}
        >
          <FileText className="w-4 h-4" /> REQUIREMENTS.md (SRS)
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('arch')}
          className={`octa-btn py-3 px-5 text-sm sm:text-base transition-all cursor-pointer flex items-center gap-2 ${
            activeTab === 'arch'
              ? 'floating-shadow-blue bg-blue-700 text-white font-black'
              : 'bg-blue-100 text-blue-950 font-bold hover:bg-blue-200'
          }`}
        >
          <Code2 className="w-4 h-4" /> ARCHITECTURE.md (Diagram)
        </button>
      </div>

      {/* Preview Content (Border-free) */}
      <div className="octa-card floating-shadow relative bg-slate-950 p-6 font-mono text-sm sm:text-base text-slate-100 max-h-96 overflow-y-auto leading-relaxed">
        <pre className="whitespace-pre-wrap font-mono">
          {activeTab === 'prompt' && masterPrompt}
          {activeTab === 'srs' && srsMarkdown}
          {activeTab === 'arch' && archMarkdown}
        </pre>
      </div>

      {/* Instructions */}
      <div className="octa-card floating-shadow-sm p-5 sm:p-6 bg-blue-50 flex items-start gap-4">
        <Layers className="w-6 h-6 text-blue-700 shrink-0 mt-0.5" />
        <div className="text-sm sm:text-base text-slate-800 space-y-1.5">
          <div className="font-black text-slate-950 text-base sm:text-lg">How to start vibe coding with AI?</div>
          <p className="text-slate-700 leading-relaxed font-semibold">
            1. Click <strong>Copy Master Prompt</strong> above. <br />
            2. Open your AI agent environment (Cursor IDE, Claude Code, Windsurf) in your project workspace. <br />
            3. Paste prompt into chat and instruct: <em>"Scaffold and implement the project according to this architecture design!"</em>.
          </p>
        </div>
      </div>

      <div className="flex justify-between items-center pt-2">
        <button
          type="button"
          onClick={onRestart}
          className="octa-btn inline-flex items-center gap-2 px-6 py-3 bg-blue-100 hover:bg-blue-200 text-blue-950 font-black text-sm sm:text-base shadow-xs transition-colors cursor-pointer"
        >
          <RefreshCw className="w-4 h-4" /> Create Another Project
        </button>
      </div>
    </div>
  );
};
