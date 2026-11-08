import { 
  ShieldCheck, Zap, Globe, Sparkles, 
  Rocket, Building2, BrainCircuit, Smartphone,
  FileText, Database
} from 'lucide-react';

export interface SolutionPack {
  id: string;
  icon: any;
  tag: string;
  title: string;
  desc: string;
  backend: string;
  database: string;
  frontend: string;
  nfrs: string[];
}

export const SOLUTION_PACKS: SolutionPack[] = [
  {
    id: 'startup',
    icon: Rocket,
    tag: 'Popular for Startups',
    title: 'Package 1: Startup Web & Rapid MVP',
    desc: 'Ideal for market validation, responsive web UI, and rapid feature turnaround.',
    backend: 'Node.js / Express.js (Lightweight REST API)',
    database: 'PostgreSQL + Prisma / Dapper / Hibernate',
    frontend: 'React 19 + TypeScript + Tailwind CSS (SPA Client)',
    nfrs: [
      'Instant response time (< 250ms)',
      'Seamless cross-platform mobile and desktop layout',
      'End-to-end setup and execution instructions'
    ]
  },
  {
    id: 'enterprise',
    icon: Building2,
    tag: 'Enterprise Standard',
    title: 'Package 2: Resilient Enterprise System',
    desc: 'Built for corporate portals, clinical records, and robust multi-tiered architectures.',
    backend: 'ASP.NET Core 10 Web API (Clean Architecture / Repository)',
    database: 'SQL Server + Entity Framework Core 10',
    frontend: 'React 19 + TypeScript + Tailwind CSS (SPA Client)',
    nfrs: [
      'Multi-factor auth & secure data encryption at rest',
      'Enterprise layered architecture (Maintainable & Clean)',
      'Optimized transactions and resilient data backups'
    ]
  },
  {
    id: 'ai_data',
    icon: BrainCircuit,
    tag: 'AI & Data Platforms',
    title: 'Package 3: AI Automation Platform',
    desc: 'Designed for AI chatbots, document processing pipelines, and data analytics.',
    backend: 'Python FastAPI (High Performance Async + Pydantic)',
    database: 'PostgreSQL + Prisma / Dapper / Hibernate',
    frontend: 'Next.js 15 (Fullstack SSR / App Router / RSC)',
    nfrs: [
      'Optimized high-throughput compute pipeline',
      'Preconfigured integrations for major AI model APIs',
      'End-to-end setup and execution instructions'
    ]
  },
  {
    id: 'mobile_first',
    icon: Smartphone,
    tag: 'Cross-Platform Mobile',
    title: 'Package 4: Cross-Platform Mobile & Web',
    desc: 'Targeted for unified web and mobile deployment across iOS and Android.',
    backend: 'Node.js / NestJS (TypeScript + Enterprise Modular)',
    database: 'MongoDB + Mongoose (NoSQL Document Store)',
    frontend: 'Flutter (Dart Cross-Platform Mobile / Web)',
    nfrs: [
      'Smooth 60 FPS UX across iOS & Android devices',
      'Secure token-based authentication',
      'Seamless cross-platform mobile and desktop layout'
    ]
  }
];

export const QUALITY_STANDARDS = [
  {
    id: "std_sec",
    icon: ShieldCheck,
    title: "Account Security & Hardening",
    desc: "Secure hashing algorithms and protection against unauthorized account access."
  },
  {
    id: "std_speed",
    icon: Zap,
    title: "Sub-second Page Load Speed",
    desc: "Instant rendering and asset caching even under concurrent user traffic."
  },
  {
    id: "std_mobile",
    icon: Globe,
    title: "Adaptive Responsive Layout",
    desc: "Clean viewport adaptation from mobile phones to high-resolution widescreen monitors."
  },
  {
    id: "std_clean",
    icon: Sparkles,
    title: "Clean & Extensible Codebase",
    desc: "Modular architecture allowing developers and AI agents to add features friction-free."
  },
  {
    id: "std_db",
    icon: Database,
    title: "Automated Persistence & Safety",
    desc: "Guaranteed state persistence protecting work in progress against accidental loss."
  },
  {
    id: "std_readme",
    icon: FileText,
    title: "Complete Onboarding Guide",
    desc: "Auto-generated step-by-step documentation for launching and testing the system."
  }
];
