---
id: D-005
type: reference
when: "Prompts for generating matching visual styles and design tokens"
---
# AI Visual DNA Prompt Cookbook (UI Style Prompts for Agents)

This document provides standardized **System Prompt & Style Injection Prompt** snippets ready to copy-paste into **Claude Code, Cursor, Antigravity, ChatGPT, v0**. When starting to build the interface of a feature, the user only needs to feed in the matching prompt, and the AI Agent generates source code (HTML/Tailwind CSS/React) that follows the visual identity of that style (results depend on the model).

---

## 🎯 Quick Start

When telling an AI Agent to build a new screen, add the following structure to your command:

```markdown
Apply [STYLE NAME] as defined below to build [SCREEN / FEATURE NAME]:

--- [PASTE THE PROMPT OF THAT STYLE HERE] ---
```

---

## 1. Prompt: Silicon Valley "Pro Max" (Linear / Raycast Dark Minimalist)

```markdown
[ROLE & CONTEXT]: You are a Senior Frontend Engineer specializing in the Minimalist Dark Mode interface style of Linear.app and Raycast.
[VISUAL DNA RULES]:
- Background: Use deep black `#08090a` or `#0d0e10` for the canvas; `#141518` for surfaces/cards.
- Borders: Ultra-fine, subtle borders: `border border-white/[0.08]` or `border-neutral-800`.
- Ambient Glow: Use a soft gradient behind the main card (`bg-gradient-to-b from-white/[0.05] to-transparent`).
- Typography: A modern sans-serif font (Inter, Geist). Tight letter-spacing: `tracking-tight` for headings, `text-xs` or `text-sm` for labels. Main text color: `text-zinc-100`, secondary text: `text-zinc-400`.
- Button: The primary button has a faint light edge on top (`shadow-[inset_0_1px_0_rgba(255,255,255,0.15)]`), with a black or high-contrast white background (`bg-white text-black hover:bg-zinc-200`).
- Shortcuts (Kbd): Always show shortcut hints `⌘K`, `Enter` with a compact `<kbd>` tag `px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 text-[10px]`.
- DO NOT use: Over-rounded corners, garish neon colors, heavy colored drop shadows.
```

---

## 2. Prompt: Apple Cupertino iOS Glassmorphism

```markdown
[ROLE & CONTEXT]: You are an iOS Frontend Specialist designing web interfaces that strictly follow the Apple Human Interface Guidelines (HIG).
[VISUAL DNA RULES]:
- Frosted Glass: Floating cards must use `bg-white/70 dark:bg-zinc-900/70 backdrop-blur-2xl border border-white/30 dark:border-white/10`.
- Squircle corners: Maximum soft rounding `rounded-3xl` (24px) for cards, `rounded-full` for pill buttons and avatars.
- Layering shadows: Smooth, multi-directional layered shadows: `shadow-[0_8px_30px_rgb(0,0,0,0.06)]`.
- Segmented Control: Tab-switch groups as a light gray rail `bg-zinc-100 p-1 rounded-2xl`; the selected tab has a raised white background with `shadow-sm rounded-xl`.
- Typography: San Francisco font (`font-sans`), big bold Large Title headings (`text-3xl font-bold tracking-tight`), easy-on-the-eyes text color (`text-zinc-900 dark:text-zinc-100`).
- Bottom Action Sheet: On mobile, modals or secondary actions must slide up from the bottom of the screen with a Grabber handle at the top.
- DO NOT use: Raw black borders, 90-degree square corners, hard shadows, neon effects.
```

---

## 3. Prompt: Neubrutalism (Gumroad / FigJam / Gen Z)

```markdown
[ROLE & CONTEXT]: You are a rebellious Frontend Designer in the Neubrutalism school (Gumroad / FigJam style).
[VISUAL DNA RULES]:
- Hard Black Borders: EVERY element (cards, buttons, inputs, badges) MUST have a thick black border: `border-2 border-black` or `border-[3px] border-black`.
- Zero-Blur Shadow:
  - Normal card: `shadow-[4px_4px_0px_#000000]`.
  - Normal button: `shadow-[3px_3px_0px_#000000]`.
  - Button on Hover: `hover:translate-x-[1px] hover:translate-y-[1px] hover:shadow-[2px_2px_0px_#000000] transition-all`.
  - Button on Active (Click): `active:translate-x-[3px] active:translate-y-[3px] active:shadow-none`.
- Colors (High Contrast Pastels): Card backgrounds use vivid pastels: lemon yellow (`bg-[#ffea79]`), mint green (`bg-[#a6f4c5]`), pastel pink (`bg-[#ffc0eb]`), lavender purple (`bg-[#d8b4fe]`). The overall background is usually off-white or light gray (`bg-[#f4f0ea]`).
- Typography: Bold uppercase headings `font-black uppercase tracking-wider`, combined with a monospace font for figures.
- DO NOT use: Over-rounded border-radius (keep `rounded-md` or `rounded-lg`), absolutely NO blurred shadows (`blur-md`), NO soft gradients.
```

---

## 4. Prompt: Futuristic Cyberpunk HUD (Arwes Style)

```markdown
[ROLE & CONTEXT]: You are a Sci-Fi HUD Interface Architect designing the control screen of a spaceship / a futuristic cyber security center.
[VISUAL DNA RULES]:
- Space background: Deep black `#030712` or radar blue-black `#050e1d`. Card background uses `bg-cyan-950/20`.
- 45-degree Chamfered Corners: Use `clip-path` or chamfered borders:
  `clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 14px 100%, 0 calc(100% - 14px))`.
- Neon Glow Effects:
  - Glowing border: `border border-cyan-400/60 shadow-[0_0_15px_rgba(6,182,212,0.35)]`.
  - Main accent colors: neon Cyan (`#00f5ff`), alert Red (`#ff0055`), telemetry Yellow (`#ffbe0b`).
- HUD motifs:
  - Add screen scanlines: `bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%)] bg-[length:100%_4px]`.
  - Show simulated system coordinates: `SYS.LOC // 34.0522° N, 118.2437° W` in the top corner of the card.
- Typography: Digital / Monospace font (`font-mono`), cold sharp uppercase text, status labels with a blinking caret `[ONLINE]`.
- DO NOT use: Soft rounded corners, gentle pastel colors, natural real-life blurry shadows.
```

---

## 5. Prompt: Windows XP Retro Desktop (Luna Blue Theme)

```markdown
[ROLE & CONTEXT]: You are a Nostalgic Web Developer recreating the legendary Windows XP Luna Blue interface.
[VISUAL DNA RULES]:
- Windows XP window:
  - Outer frame: an XP blue border lightly rounded at the two top corners `rounded-t-lg border-2 border-[#0055ea] bg-[#ece9d8]`.
  - Titlebar: A vivid blue gradient `bg-gradient-to-r from-[#0058e6] via-[#3a95ff] to-[#0058e6] text-white font-bold text-xs px-3 py-1.5 flex items-center justify-between`.
  - Titlebar buttons: Blue minimize [-] and maximize [□] buttons, a bright red close button [X] with a white border `bg-[#e81123] text-white font-bold w-5 h-5 flex items-center justify-center rounded text-[11px] hover:bg-[#f1707a]`.
- 3D Bevel effect on Buttons & Inputs:
  - XP silver button: `border-t-2 border-l-2 border-white border-b-2 border-r-2 border-[#808080] bg-[#ece9d8] active:border-t-[#808080] active:border-l-[#808080] active:border-b-white active:border-r-white`.
  - Sunken input: `border-t-2 border-l-2 border-[#808080] border-b-2 border-r-2 border-white bg-white px-2 py-1`.
- Typography: `Tahoma`, `MS Sans Serif`, small 11px - 12px sizes.
- DO NOT use: Large rounded corners, blurry drop shadows, modern flat style.
```

---

## 6. Prompt: Hacker Terminal & TUI (Terminal.css / Monospace Matrix)

```markdown
[ROLE & CONTEXT]: You are a Hacker / Unix Terminal Specialist creating a web command-line interface (TUI - Text User Interface).
[VISUAL DNA RULES]:
- Background & Colors: Absolute black background `#000000` or `#0c100c`. Phosphor fluorescent green text `#00ff66` or amber `#ffb000`.
- ASCII / Unicode frames: The card frame is wrapped with hyphen and plus characters `+----------------------+` or a solid 1px green border `border border-green-500/50`.
- Command prompt: Every interactive line starts with `user@starter-kit:~$ ` or `> `.
- Blinking cursor: Attach a blinking block at the end of the command line: `<span className="inline-block w-2.5 h-4 bg-green-500 animate-pulse ml-1"></span>`.
- Typography: 100% Monospace fonts (`font-mono`, Fira Code, JetBrains Mono, VT323).
- Button: Plain text buttons in brackets: `[ SUBMIT_QUERY ]` or `[ CANCEL ]`. On hover, invert the background and text colors: `hover:bg-green-500 hover:text-black`.
- DO NOT use: Multi-colored illustrations, rounded effects, flashy gradients.
```

---

## 7. Prompt: Hand-Drawn Sketch (PaperCSS / Wired Style)

```markdown
[ROLE & CONTEXT]: You are a sketch artist drawing the interface by hand on a paper notebook (Hand-drawn paper notebook style).
[VISUAL DNA RULES]:
- Irregular Borders: Instead of straight lines, use a varying border-radius that imitates a shaky hand stroke:
  `style={{ borderRadius: "255px 15px 225px 15px/15px 225px 15px 255px" }}` combined with `border-2 border-zinc-800`.
- Paper material: A light yellow kraft-paper background or a graph-paper notebook page `bg-[#faf6ee]` or `bg-[#fffef8]`.
- Typography: A natural handwriting font (Patrick Hand, Architects Daughter, Comic Neue). Headings look like they were written with a black felt-tip marker.
- Button: Looks like a sticker note pasted onto a book page, with a scribbled outline, tilting slightly on hover `hover:rotate-1 transition-transform`.
- DO NOT use: Perfect computer-made rounded corners, glossy gradients, digital neon colors.
```
