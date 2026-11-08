import { ThemePreset } from '../types';

export const THEME_PRESETS: ThemePreset[] = [
  {
    id: 'linear-pro',
    name: 'Linear Pro Max',
    universe: 'Silicon Valley "Pro Max"',
    tagline: 'Dark Minimalist, Ambient Glow & Micro-interactions',
    description: 'The sleek minimalist style of Linear.app, Raycast, Vercel and Supabase for engineer tools and premium SaaS.',
    tokens: {
      containerClass: 'bg-[#09090b] text-zinc-100 p-6 rounded-2xl border border-white/10 shadow-2xl relative overflow-hidden',
      cardClass: 'bg-[#121316]/80 backdrop-blur-md border border-white/[0.08] rounded-xl p-5 shadow-lg relative',
      headerClass: 'border-b border-white/[0.08] pb-4 mb-4 flex items-center justify-between',
      titleClass: 'text-lg font-semibold tracking-tight text-zinc-100 flex items-center gap-2',
      subtitleClass: 'text-xs text-zinc-400 mt-1',
      primaryButtonClass: 'bg-white text-zinc-900 hover:bg-zinc-200 text-xs font-medium px-4 py-2 rounded-lg transition-colors shadow-[inset_0_1px_0_rgba(255,255,255,0.2)] flex items-center gap-1.5',
      secondaryButtonClass: 'bg-zinc-800/80 hover:bg-zinc-800 text-zinc-300 text-xs font-medium px-3 py-2 rounded-lg border border-white/10 transition-colors',
      badgeClass: 'bg-zinc-800 text-zinc-300 border border-white/10 text-[11px] px-2.5 py-0.5 rounded-full font-medium',
      inputClass: 'bg-zinc-900 border border-white/10 rounded-lg px-3 py-2 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-indigo-500/80 w-full',
      accentTextClass: 'text-indigo-400 font-mono text-xs',
    },
    aiPromptSnippet: `Apply the Linear Pro Max style:
- Deep black background (#09090b), child cards use #121316/80.
- Ultra-fine borders: border border-white/10.
- Typography: tracking-tight, text-zinc-100/text-zinc-400.
- Buttons: sleek white background with black text, or bg-zinc-800. Always include a <kbd> shortcut.`,
    openSourceRefs: ['Linear.app', 'Raycast', 'shadcn/ui'],
  },
  {
    id: 'ios-glass',
    name: 'Apple Cupertino iOS',
    universe: 'Mobile OS & Human Interface',
    tagline: 'Frosted Glassmorphism, Squircles & Smooth Elevation',
    description: 'Designed to Apple HIG standards: frosted glass, soft rounded corners and subtly layered shadows.',
    tokens: {
      containerClass: 'bg-gradient-to-br from-slate-100 to-sky-50 text-slate-900 p-6 rounded-3xl border border-white/60 shadow-[0_20px_50px_rgba(0,0,0,0.06)] backdrop-blur-2xl',
      cardClass: 'bg-white/70 backdrop-blur-xl border border-white/80 rounded-2xl p-5 shadow-[0_8px_30px_rgba(0,0,0,0.04)]',
      headerClass: 'border-b border-slate-200/50 pb-3 mb-4 flex items-center justify-between',
      titleClass: 'text-xl font-bold tracking-tight text-slate-900',
      subtitleClass: 'text-xs text-slate-500 font-normal',
      primaryButtonClass: 'bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2 rounded-full shadow-sm transition-all',
      secondaryButtonClass: 'bg-slate-200/60 hover:bg-slate-200 text-slate-700 text-xs font-medium px-3 py-2 rounded-full transition-all',
      badgeClass: 'bg-blue-50 text-blue-700 border border-blue-200/50 text-[11px] px-3 py-0.5 rounded-full font-semibold',
      inputClass: 'bg-slate-100/80 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/30 w-full',
      accentTextClass: 'text-blue-600 font-medium text-xs',
    },
    aiPromptSnippet: `Apply the Apple iOS Glassmorphism style:
- Frosted glass background: bg-white/70 backdrop-blur-xl border border-white/80.
- Squircle corners: rounded-2xl / rounded-3xl for cards, rounded-full for buttons.
- Light layered shadow: shadow-[0_8px_30px_rgba(0,0,0,0.04)].
- Accent color: Apple Blue, clean San Francisco font.`,
    openSourceRefs: ['Apple HIG', 'Framework7'],
  },
  {
    id: 'neobrutalism',
    name: 'Neubrutalism',
    universe: 'Anti-Design & Creator Economy',
    tagline: 'Hard Black Borders, Zero-Blur Shadows & Vibrant Pastels',
    description: 'The bold style of Gumroad and FigJam: thick black borders, absolutely hard unblurred shadows and bursting pastel colors.',
    tokens: {
      containerClass: 'bg-[#fff5ea] text-black p-6 rounded-xl border-[3px] border-black shadow-[6px_6px_0px_#000]',
      cardClass: 'bg-[#fffa8a] border-[3px] border-black rounded-lg p-5 shadow-[4px_4px_0px_#000]',
      headerClass: 'border-b-[3px] border-black pb-3 mb-4 flex items-center justify-between',
      titleClass: 'text-lg font-black uppercase tracking-wider text-black',
      subtitleClass: 'text-xs font-bold text-zinc-800',
      primaryButtonClass: 'bg-[#ff90e8] hover:bg-[#ff75e3] text-black text-xs font-black uppercase px-4 py-2 rounded-md border-[2.5px] border-black shadow-[3px_3px_0px_#000] hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_#000] active:translate-x-[3px] active:translate-y-[3px] active:shadow-none transition-all',
      secondaryButtonClass: 'bg-white hover:bg-zinc-100 text-black text-xs font-bold px-3 py-2 rounded-md border-[2.5px] border-black shadow-[2px_2px_0px_#000]',
      badgeClass: 'bg-[#a6f4c5] text-black border-2 border-black text-[11px] px-2.5 py-0.5 rounded-md font-black uppercase',
      inputClass: 'bg-white border-[2.5px] border-black rounded-md px-3 py-2 text-xs text-black placeholder-zinc-500 font-bold focus:outline-none focus:bg-[#f0fdf4] shadow-[2px_2px_0px_#000] w-full',
      accentTextClass: 'text-black font-black uppercase text-xs',
    },
    aiPromptSnippet: `Apply the Neubrutalism style:
- Every element has a raw black border: border-[3px] border-black.
- Hard shadow with 0 blur: shadow-[4px_4px_0px_#000].
- Pastel colors: #fffa8a (yellow), #ff90e8 (pink), #a6f4c5 (mint).
- Buttons on click: active:translate-x-[3px] active:translate-y-[3px] active:shadow-none.`,
    openSourceRefs: ['neobrutalism-components', 'Gumroad'],
  },
  {
    id: 'cyberpunk-hud',
    name: 'Cyberpunk Sci-Fi HUD',
    universe: 'Futuristic & Sci-Fi',
    tagline: 'Neon Glow, 45° Chamfered Edges & CRT Scanlines',
    description: 'A spaceship control screen and futuristic security station in the Arwes Framework style, with beveled edges and bright Neon light.',
    tokens: {
      containerClass: 'bg-[#030712] text-cyan-100 p-6 rounded-none border border-cyan-500/50 shadow-[0_0_20px_rgba(6,182,212,0.25)] relative overflow-hidden font-mono',
      cardClass: 'bg-cyan-950/20 border border-cyan-400/40 p-5 relative shadow-[inset_0_0_12px_rgba(6,182,212,0.15)] [clip-path:polygon(0_0,calc(100%-12px)_0,100%_12px,100%_100%,12px_100%,0_calc(100%-12px))]',
      headerClass: 'border-b border-cyan-500/30 pb-3 mb-4 flex items-center justify-between',
      titleClass: 'text-base font-bold uppercase tracking-widest text-cyan-300 flex items-center gap-2',
      subtitleClass: 'text-[10px] text-cyan-600 uppercase tracking-wider',
      primaryButtonClass: 'bg-cyan-500 hover:bg-cyan-400 text-black text-xs font-bold uppercase px-4 py-2 transition-all shadow-[0_0_10px_rgba(6,182,212,0.6)] [clip-path:polygon(0_0,calc(100%-8px)_0,100%_8px,100%_100%,8px_100%,0_calc(100%-8px))]',
      secondaryButtonClass: 'bg-transparent hover:bg-cyan-950/60 text-cyan-300 border border-cyan-500/60 text-xs font-medium uppercase px-3 py-2 transition-all',
      badgeClass: 'bg-cyan-950 text-cyan-300 border border-cyan-400/80 text-[10px] px-2 py-0.5 uppercase tracking-wider font-mono animate-pulse',
      inputClass: 'bg-black/80 border border-cyan-500/60 px-3 py-2 text-xs text-cyan-200 placeholder-cyan-800 font-mono focus:outline-none focus:border-cyan-300 focus:shadow-[0_0_10px_rgba(6,182,212,0.5)] w-full',
      accentTextClass: 'text-cyan-400 font-mono text-xs tracking-wider',
    },
    aiPromptSnippet: `Apply the Cyberpunk Sci-Fi HUD style:
- Space-black background #030712, cards with 45-degree clipped corners via clip-path polygon.
- Neon light: cyan border shadow-[0_0_15px_rgba(6,182,212,0.4)].
- Typography: 100% uppercase font-mono, showing telemetry labels [ONLINE].
- Buttons: clipped corners, glowing light on hover.`,
    openSourceRefs: ['Arwes', 'Cyberpunk 2077 HUD'],
  },
  {
    id: 'win-xp',
    name: 'Windows XP Retro',
    universe: 'Platform & OS Emulation',
    tagline: 'Luna Blue Gradient, 3D Bevel & Red [X] Button',
    description: 'Recreates the legendary 2001 Windows XP desktop with Bevel effects and the signature gradient title bar.',
    tokens: {
      containerClass: 'bg-[#ece9d8] text-black p-4 rounded-t-lg border-2 border-[#0055ea] shadow-xl font-sans',
      cardClass: 'bg-[#ece9d8] border-t-2 border-l-2 border-white border-b-2 border-r-2 border-[#808080] p-4',
      headerClass: 'bg-gradient-to-r from-[#0058e6] via-[#3a95ff] to-[#0058e6] text-white px-3 py-1.5 -m-4 mb-4 rounded-t-sm flex items-center justify-between shadow-sm',
      titleClass: 'text-xs font-bold text-white tracking-wide flex items-center gap-1.5',
      subtitleClass: 'text-[11px] text-slate-700',
      primaryButtonClass: 'border-t-2 border-l-2 border-white border-b-2 border-r-2 border-[#808080] bg-[#ece9d8] hover:bg-[#f5f3e9] active:border-t-[#808080] active:border-l-[#808080] active:border-b-white active:border-r-white text-xs font-normal px-4 py-1 text-black shadow-sm',
      secondaryButtonClass: 'border-t-2 border-l-2 border-white border-b-2 border-r-2 border-[#808080] bg-[#ece9d8] text-xs px-3 py-1 text-black',
      badgeClass: 'bg-white border-t border-l border-[#808080] border-b border-r border-white text-[11px] px-2 py-0.5 text-black font-normal',
      inputClass: 'bg-white border-t-2 border-l-2 border-[#808080] border-b-2 border-r-2 border-white px-2 py-1 text-xs text-black focus:outline-none w-full',
      accentTextClass: 'text-[#0055ea] font-bold text-xs',
    },
    aiPromptSnippet: `Apply the Windows XP Luna Blue style:
- Title bar: bg-gradient-to-r from-[#0058e6] via-[#3a95ff] to-[#0058e6] text-white.
- Close button: bright red #e81123 with a white X.
- 3D Bevel effect: border-t-2 border-l-2 border-white border-b-2 border-r-2 border-[#808080].
- Window background: silver gray #ece9d8, Tahoma text-xs.`,
    openSourceRefs: ['XP.css', '98.css'],
  },
  {
    id: 'terminal-tui',
    name: 'Hacker Terminal (TUI)',
    universe: 'Retro Gaming & Geek Culture',
    tagline: 'Monochrome Phosphor Green, Blinking Cursor & ASCII Borders',
    description: 'The matrix-like command-line interface of hackers and Linux sysadmins: pure black background, glowing green text and not a single wasted pixel.',
    tokens: {
      containerClass: 'bg-black text-[#00ff66] p-6 rounded-none border border-[#00ff66]/60 shadow-[0_0_15px_rgba(0,255,102,0.15)] font-mono',
      cardClass: 'bg-black/90 border border-[#00ff66]/40 p-4 relative',
      headerClass: 'border-b border-dashed border-[#00ff66]/40 pb-3 mb-4 flex items-center justify-between',
      titleClass: 'text-sm font-bold uppercase tracking-wider text-[#00ff66] flex items-center gap-2',
      subtitleClass: 'text-xs text-[#00ff66]/60',
      primaryButtonClass: 'bg-[#00ff66] hover:bg-[#00cc52] text-black text-xs font-bold uppercase px-3 py-1.5 transition-colors font-mono',
      secondaryButtonClass: 'bg-transparent hover:bg-[#00ff66]/20 text-[#00ff66] border border-[#00ff66] text-xs font-mono px-3 py-1.5 transition-colors',
      badgeClass: 'bg-black text-[#00ff66] border border-[#00ff66] text-[10px] px-2 py-0.5 font-mono uppercase',
      inputClass: 'bg-black border border-[#00ff66]/60 px-3 py-1.5 text-xs text-[#00ff66] placeholder-[#00ff66]/40 font-mono focus:outline-none focus:border-[#00ff66] focus:ring-1 focus:ring-[#00ff66] w-full',
      accentTextClass: 'text-[#00ff66] font-mono text-xs',
    },
    aiPromptSnippet: `Apply the Hacker Terminal style:
- Black background #000000, phosphor green text #00ff66.
- Typography: 100% font-mono.
- Command prompt: start with 'user@starter-kit:~$ ' and a blinking cursor.
- Text-style buttons [ EXECUTE ] or a green background with black text.`,
    openSourceRefs: ['Terminal.css'],
  },
  {
    id: 'hand-drawn',
    name: 'Hand-Drawn Paper',
    universe: 'Tactile & Handcrafted',
    tagline: 'Sketchy Irregular Borders, Kraft Paper & Notebook Feel',
    description: 'A natural sketched feel on a coffee-shop scratch-paper page, with wobbly hand-drawn borders and a friendly, warm manner.',
    tokens: {
      containerClass: 'bg-[#faf6ee] text-zinc-900 p-6 rounded-[255px_15px_225px_15px/15px_225px_15px_255px] border-2 border-zinc-800 shadow-md',
      cardClass: 'bg-white rounded-[15px_255px_15px_225px/225px_15px_255px_15px] border-2 border-zinc-800 p-5 shadow-sm',
      headerClass: 'border-b-2 border-dashed border-zinc-400 pb-3 mb-4 flex items-center justify-between',
      titleClass: 'text-lg font-bold text-zinc-900 tracking-tight',
      subtitleClass: 'text-xs text-zinc-600 italic',
      primaryButtonClass: 'bg-[#fffae0] hover:bg-[#fff5c0] text-zinc-900 text-xs font-bold px-4 py-2 rounded-[255px_15px_225px_15px/15px_225px_15px_255px] border-2 border-zinc-800 hover:rotate-1 transition-transform shadow-sm',
      secondaryButtonClass: 'bg-white hover:bg-zinc-50 text-zinc-700 text-xs font-medium px-3 py-2 rounded-lg border border-dashed border-zinc-400',
      badgeClass: 'bg-amber-100 text-amber-900 border border-amber-800/40 text-[11px] px-2.5 py-0.5 rounded-full font-medium',
      inputClass: 'bg-white border-2 border-zinc-700 rounded-[255px_15px_225px_15px/15px_225px_15px_255px] px-3.5 py-2 text-xs text-zinc-800 placeholder-zinc-400 focus:outline-none w-full',
      accentTextClass: 'text-amber-800 font-bold text-xs',
    },
    aiPromptSnippet: `Apply the Hand-Drawn Paper style:
- Scratch-paper background: bg-[#faf6ee] or kraft paper.
- Uneven hand-drawn borders: border-radius: 255px 15px 225px 15px/15px 225px 15px 255px.
- Black ink outline: border-2 border-zinc-800.
- Buttons look like stuck-on sticky notes, tilting slightly on hover.`,
    openSourceRefs: ['PaperCSS', 'Wired Elements'],
  },
];
