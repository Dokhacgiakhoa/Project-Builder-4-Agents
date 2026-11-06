---
id: D-006
type: playbook
when: "When translating screenshots or UI references into code without falling into visual doom loops"
---

# PLAYBOOK: SCREENSHOT-TO-CODE & VISUAL REVERSE ENGINEERING

> **For AI Agents**: When a Vibe Coder uploads a screenshot, Figma mock, or reference URL asking to reproduce an interface, naive agents fall into a disastrous **UI Doom Loop**: guessing random Tailwind classes, breaking layouts with every fix attempt, and generating cheap, unpolished knock-offs. This playbook enforces a rigorous 5-step engineering protocol to achieve pixel-accurate replication on the first pass.

---

## 1. The Fundamental Trap: Generative vs. Replicative Mode

* **Generative Skills (e.g., `taste-skill`, `ui-ux-pro-max`)**: These toolkits exist to generate novel designs from scratch when no visual reference exists. They inject intentional variance (`DESIGN_VARIANCE`), opinionated palettes, and procedural layout dials.
* **Replicative Mode (When an Image is Provided)**:
  * **MANDATORY**: **Suppress Generative Variance.**
  * Do NOT let generative skills overwrite colors, font families, or geometries present in the screenshot.
  * Your task is **faithful structural reverse engineering**, not artistic improvisation.

---

## 2. The 5-Step Visual Reverse-Engineering Protocol

```
[User Screenshot / Mockup]
          │
          ▼
[STEP 1: EXTRACT DESIGN TOKENS]      ──► Hex colors, Spacing scale (4px/8px), Radius, Typography
          │
          ▼
[STEP 2: WIREFRAME SKELETON LAYOUT]  ──► Macro Grid / Flexbox containers (Zero styling)
          │
          ▼
[STEP 3: COMPONENT ASSEMBLY]         ──► 1px subtle borders, 4-state completeness, micro-details
          │
          ▼
[STEP 4: THE MIRROR TEST (SELF-DIFF)]──► Headless browser screenshot $\to$ Compare $\to$ Self-correct
          │
          ▼
[STEP 5: TOKENS-ONLY ADJUSTMENTS]    ──► Modify root variables, NEVER hack arbitrary component classes
```

### Step 1: Extract Design Tokens Before Writing Any Code
Never jump straight to writing JSX or HTML. First, inspect the screenshot and declare a strict Token Dictionary:
1. **Background & Canvas**:
   * Canvas (deepest background): Exact hex (e.g., `#090D16` Dark or `#F8FAFC` Light).
   * Surface (card/panel container): Exact hex (e.g., `#111827` or `#FFFFFF`).
   * Subtle Border: Alpha-blended border (e.g., `rgba(255, 255, 255, 0.08)` or `border-zinc-800`).
2. **Typography Hierarchy**:
   * Font Family: Modern clean sans-serif (Inter, Geist, SF Pro).
   * Primary Text: 100% contrast (`text-white` or `text-zinc-900`).
   * Secondary Text: 60% contrast (`text-zinc-400` or `text-zinc-500`).
   * Letter Spacing: Enforce tight tracking on headings (`tracking-tight` or `-0.02em`).
3. **Geometry & Cadence**:
   * Border Radius: Pick ONE uniform scale (e.g., `rounded-xl` = 12px for cards, `rounded-lg` = 8px for buttons).
   * Spacing Cadence: Strictly multiples of 4px/8px (`p-2`, `p-4`, `p-6`, `gap-4`). Zero random arbitrary values (`p-[13px]`).

Write these tokens into `tailwind.config.js` or `globals.css` variables **first**.

---

### Step 2: Wireframe & Skeleton Layout (Zero Component Styling)
Scaffold macro-layout layout containers first:
* Use standard CSS Grid (`grid grid-cols-12`) or Flexbox (`flex flex-col md:flex-row`).
* Verify responsiveness: Mobile column stack $\rightarrow$ Desktop multi-column grid.
* Do not attach colors, hover effects, or typography until the layout skeleton matches the screenshot's proportions.

---

### Step 3: Component Assembly & The 4 Golden Micro-Details
High-end UI aesthetics (Linear, Stripe, Apple, Raycast) depend entirely on micro-details that naive LLMs overlook:
1. **Subtle 1px Borders**: Modern cards do not use heavy drop shadows. They use a crisp 1px border with a soft inner glow:
   ```html
   <div class="border border-white/10 bg-zinc-900/60 backdrop-blur-md shadow-sm">
   ```
2. **Multi-Layered Soft Elevation**: Replace blurry black shadows with layered ambient diffusion:
   ```css
   box-shadow: 0 1px 2px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.08);
   ```
3. **4-State Completeness**: Every interactive element (button, tab, row, input) MUST define 4 states:
   * **Default**: Clean, readable baseline.
   * **Hover**: Subtle brightness increase (`hover:bg-white/5` or `hover:border-white/20`) with `transition-colors duration-150`.
   * **Active / Press**: Micro-compression (`active:scale-[0.98]`).
   * **Disabled / Focus**: Explicit focus rings (`focus-visible:ring-2 focus-visible:ring-primary`).
4. **Visual Density**: Match information density to screenshot (do not artificially inflate whitespace).

---

### Step 4: The Mirror Test (Self-Visual Diff via Headless Browser)
**The Blind-Coding Gap**: Agents fail because they cannot see their own output after generating code.
* If browser automation tools are available (Playwright MCP, Chrome DevTools MCP):
  1. Boot the local development server (`npm run dev`).
  2. Navigate to the rendered page and take a screenshot via headless browser.
  3. Compare the generated screenshot side-by-side with the user's reference image.
  4. Check: Are margins aligned? Are contrast ratios sufficient? Are font sizes balanced?
  5. **Self-correct deviations autonomously** before presenting the code to the user.

---

### Step 5: Anti-UI-Doom-Loop Protocol (How to Handle User Feedback)
When the Vibe Coder provides subjective feedback (e.g., *"Make it look cleaner"*, *"The button looks off"*, *"Darken the theme"*):
1. **Never hack individual components with ad-hoc utility classes**: Modifying one component directly causes visual fragmentation and breaks layout symmetry.
2. **Adjust at the Token Layer**:
   * Want darker theme? $\rightarrow$ Update `--background` in `globals.css`.
   * Cards feel too round? $\rightarrow$ Update `--radius` token from `1rem` to `0.75rem`.
   * Text feels cramped? $\rightarrow$ Adjust `line-height` and `gap` scales.
3. **2-Attempt Circuit Breaker**: If two iterations fail to satisfy the user, STOP. Ask for explicit clarification:
   * *"Do you prefer higher contrast or softer borders?"*
   * *"Should the cards be more compact (higher density) or spacious?"*
