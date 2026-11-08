# 🎨 UNIVERSAL FRONTEND STARTER KIT (BULLETPROOF REACT)

Frontend skeleton standardized on the **Feature-Driven (Bulletproof React)** architecture, optimized for smooth collaboration between technology engineers and AI Coding Agents.

---

## 🏛️ 1. STANDARD FOLDER STRUCTURE

```text
frontend/src/
├── app/                  # Application Layer (AppProviders, Global Router)
├── assets/               # Global static assets (Images, SVG, Icons)
├── components/           # Shared UI Components (Button, Card, Layouts)
│   ├── layouts/          # MainLayout, Sidebar, Navbar
│   └── ui/               # Shared UI atoms (Buttons, Cards, Inputs)
├── config/               # Environment variables & configuration validated through Zod
├── features/             # INDEPENDENT BUSINESS MODULES (Feature-Driven)
│   ├── auth/             # User authentication (Login, Register, Session)
│   ├── dashboard/        # Dashboard & statistics
│   └── ai-chat/          # AI Agent interaction module
│       ├── api/          # The feature's API calls & React Query hooks
│       ├── components/   # The feature's internal UI components
│       ├── types/        # The feature's TypeScript types
│       └── index.ts      # Public API Export (the single point of contact)
├── hooks/                # Shared custom React Hooks
├── lib/                  # Library configuration (Axios api-client, TanStack Query)
├── stores/               # Global Client State management through Zustand
└── types/                # Generic API response & common types
```

---

## ⚡ 2. THE INVARIANT PRINCIPLES

1. **Feature Isolation**: Every component, hook or type that serves only one specific feature MUST live in that feature's folder.
2. **Public API Pattern (`index.ts`)**: Each feature exports only what the outside needs through `index.ts`. Never import directly into another feature's internal files.
3. **The Anti-Crash Standard**:
   - Data from the API is always checked with Optional Chaining (`?.`) and Safe Fallbacks (`?? []`).
   - Every form submission and async fetch is wrapped in `try...catch` or React Query Error Boundaries.

---

## 🚀 3. GETTING STARTED

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Configure the environment file:
   ```bash
   cp .env.example .env
   ```
3. Start the dev server:
   ```bash
   npm run dev
   ```
   The app will be available at: `http://localhost:3000`.
