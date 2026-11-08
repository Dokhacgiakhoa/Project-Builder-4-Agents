---
id: D-004
type: reference
when: "Browsing UI aesthetic archetype catalog"
---
# UI/UX Design Archetypes & Open-Source Libraries Catalog

This document defines in detail the most common **7 Aesthetic Universes** and **14 Design Archetypes** in software development and digital design. It serves as a "Visual DNA Specification" that helps Product Managers, Designers, human developers and AI Agents (Claude Code, Cursor, Antigravity, v0) choose and implement a consistent interface with ease.

---

## 📑 Table of Contents: the 7 Aesthetic Universes

1. [Universe 1: Platform & OS Emulation](#1-platform--os-emulation-universe)
   - 1.1. Windows XP / 98 / 7 Retro Desktop
   - 1.2. Apple Cupertino iOS Glassmorphism
   - 1.3. Google Material You (Material Design 3)
2. [Universe 2: Futuristic & Sci-Fi](#2-futuristic--sci-fi-universe)
   - 2.1. Cyberpunk / Sci-Fi HUD (Arwes Style)
   - 2.2. Frutiger Aero (Glossy Skeuomorphic Optimism)
   - 2.3. Synthwave / Outrun 80s Neon
3. [Universe 3: Silicon Valley "Pro Max" & Modern SaaS](#3-silicon-valley-pro-max--modern-saas-universe)
   - 3.1. Linear / Raycast Dark Minimalist
   - 3.2. Apple Bento Grid Layout
   - 3.3. High-Motion SaaS (Magic UI & Aceternity)
4. [Universe 4: Rebellious & Rule-Breaking (Anti-Design & Gen Z)](#4-rebellious--rule-breaking-universe-anti-design--gen-z)
   - 4.1. Neubrutalism (Gumroad / Figma FigJam Style)
   - 4.2. Y2K Cyber Glitch & Hologram
5. [Universe 5: Nostalgic Games & Geek Culture (Retro Gaming & Geek)](#5-nostalgic-games--geek-culture-universe-retro-gaming--geek)
   - 5.1. 8-bit Console Pixel Art (NES.css)
   - 5.2. 16-bit RPG Video Game (RPGUI)
   - 5.3. Hacker Terminal & TUI (Terminal.css)
6. [Universe 6: Handcrafted & Organic Tactile](#6-handcrafted--organic-tactile-universe)
   - 6.1. Hand-Drawn Sketch (PaperCSS & Wired-Elements)
   - 6.2. Claymorphism (3D Soft Puffy Clay)
   - 6.3. Classic Skeuomorphism (Wood, Leather & Brass)
7. [Universe 7: Academic, Press & Magazine (Editorial & Bauhaus)](#7-academic-press--magazine-universe-editorial--bauhaus)
   - 7.1. Swiss / Bauhaus International Style
   - 7.2. Luxury Editorial & Newspaper

---

## 1. Platform & OS Emulation Universe

### 1.1. Windows XP / 98 / 7 Retro Desktop

- **Emotion & Context**: Nostalgia for the personal-computer era of the 1990s-2000s; it delights, feels unusual and breaks the stereotype of the modern web.
- **Representative open-source libraries**:
  - [98.css](https://github.com/jdan/98.css) — a pure CSS framework with no JS dependency that recreates Windows 98.
  - [XP.css](https://github.com/botoxparty/XP.css) — recreates the signature Luna theme of Windows XP.
  - [7.css](https://github.com/khang-nd/7.css) — recreates the Aero frosted-glass effect of Windows 7.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: a blue gradient title bar from `#0055ea` to `#3a93ff`, silver-gray background `#ece9d8`, bright red close button `#d93c2c`.
  - *Borders & Shadows*: the classic 3D Bevel emboss effect: `border-top: 2px solid #ffffff`, `border-left: 2px solid #ffffff`, `border-right: 2px solid #808080`, `border-bottom: 2px solid #808080`.
  - *Typography*: `Tahoma`, `MS Sans Serif`, `Segoe UI`, compact 11px - 12px sizes.
- **Best use cases**: Web3 portfolios, OS-simulation apps on the web, Easter egg marketing campaigns.

### 1.2. Apple Cupertino iOS Glassmorphism

- **Emotion & Context**: Luxurious and gentle, focused on visual content, a premium mobile standard.
- **Reference**: [Apple Human Interface Guidelines (HIG)](https://developer.apple.com/design/human-interface-guidelines/).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: frosted-glass background `rgba(255, 255, 255, 0.7)` (light) or `rgba(30, 30, 35, 0.75)` (dark), a softly glowing border `rgba(255, 255, 255, 0.2)`.
  - *Blur & Filter*: `backdrop-blur-xl`, `backdrop-saturate-150`.
  - *Border Radius*: ultra-round corners (Squircle) `rounded-3xl` (24px - 32px).
  - *Shadows*: smooth multi-directional layered shadows: `box-shadow: 0 20px 40px rgba(0,0,0,0.08)`.
  - *Typography*: `SF Pro Display`, `SF Pro Text`, `-apple-system`.
- **Best use cases**: Lifestyle apps, mobile-first web apps, personal FinTech, health-care dashboards.

### 1.3. Google Material You (Material Design 3)

- **Emotion & Context**: Friendly, flexible, deeply personalized, easy to use for all ages.
- **Open-source library**: [Material Web (@material/web)](https://github.com/material-components/material-web).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: Tonal Palettes — the dominant color automatically yields its tones (Primary, Secondary, Tertiary, Container, Surface Tint).
  - *Shape & Elements*: pill-shaped buttons (`rounded-full`), the Floating Action Button (FAB).
  - *State & Interaction*: a tactile ripple effect (Ink Ripple Effect) on click or touch.
  - *Typography*: `Roboto`, `Google Sans`.
- **Best use cases**: Enterprise SaaS, productivity apps (Docs, Spreadsheets, CRM), the Android ecosystem.

---

## 2. Futuristic & Sci-Fi Universe

### 2.1. Cyberpunk / Sci-Fi HUD (Arwes Style)

- **Emotion & Context**: A sci-fi future, spaceship interiors, AI laboratories, military cyber security.
- **Open-source library**: [Arwes Framework](https://github.com/arwes/arwes) (Futuristic Sci-Fi UI Web Framework).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: space-black background `#030712`, borders and Neon light in Cyan `#00f5ff`, Magenta `#ff007f`, Amber Warning `#ffb703`.
  - *Edges & Borders*: 45-degree chamfered corners (Chamfered Clip-path `polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 0 100%)`).
  - *Effects*: a glowing border `box-shadow: 0 0 15px rgba(0, 245, 255, 0.5)`, a Radar coordinate grid in the background, screen scan lines (CRT Scanlines).
  - *Typography*: `Orbitron`, `Share Tech Mono`, `Chakra Petch`.
- **Best use cases**: Server monitoring, SOC dashboards, Web3 crypto exchanges, gaming telemetry.

### 2.2. Frutiger Aero (the 2005 - 2012 era)

- **Emotion & Context**: Technological optimism, freshness, friendliness with nature (ecology combined with digital).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: clear sky blue, fresh lime green, pearl white, lemon yellow.
  - *Textures & Glass*: glossy water bubbles, rippling water surfaces, convex 3D lenses reflecting sunlight.
  - *Lighting*: an extremely bright top-edge highlight, smooth gradient shading from light to dark.
- **Best use cases**: Environmental and educational apps, recreating the nostalgic Web 2.0 aesthetic.

### 2.3. Synthwave / Outrun 80s Neon

- **Emotion & Context**: 80s nostalgia, speed, Miami neon nights.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: deep navy-purple `#12072b`, glowing pink `#ff007f`, lotus purple `#9d4edd`, sunset orange-yellow `#ff9e00`.
  - *Visual Elements*: a half sun cut by horizontal stripes, a 3D Perspective Grid running to infinity.
  - *Typography*: `Monoton`, `Press Start 2P`, speed-italicized bold display fonts.

---

## 3. Silicon Valley "Pro Max" & Modern SaaS Universe

### 3.1. Linear / Raycast Dark Minimalist

- **Emotion & Context**: The highest technical class, instant response, pixel-perfect precision, tools for top software engineers.
- **Real-world examples**: [Linear.app](https://linear.app), [Raycast](https://raycast.com), [Supabase](https://supabase.com).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: deep dark background `#08090a` / `#0f1011`, ultra-fine border `border border-white/10`, light purple accent `#5e6ad2` or cobalt blue.
  - *Ambient Glow*: a soft halo behind the card: `background: radial-gradient(circle, rgba(94,106,210,0.15) 0%, transparent 70%)`.
  - *Typography*: `Geist`, `Inter`, compact display sizes, letter-spacing `-0.02em`.
  - *Interactions*: shortcuts shown everywhere (Keyboard first), instant tooltips, no superfluous animation that slows operations.

### 3.2. Apple Bento Grid Layout

- **Emotion & Context**: Tidy information, smart compartments, a captivating visual that celebrates product features.
- **Real-world examples**: Apple's iPhone/MacBook pages, the GitHub Copilot landing page.
- **Visual DNA & Design Tokens**:
  - *Grid Layout*: an asymmetric grid `grid grid-cols-1 md:grid-cols-3 gap-4`, some cards spanning 2 columns or 2 rows (`col-span-2`, `row-span-2`).
  - *Card Styling*: soft rounded borders `rounded-2xl`, dark gradient background, with illustrations or charts placed directly inside each Bento compartment.

### 3.3. High-Motion SaaS (Magic UI & Aceternity)

- **Emotion & Context**: An impressive breakthrough that catches the eye in the first second, high conversion for landing pages.
- **Open-source libraries**:
  - [Magic UI](https://github.com/magicuidesign/magicui) — 150+ animated components integrated directly with shadcn/ui.
  - [Aceternity UI](https://github.com/aceternity/aceternity-ui) — 3D parallax cards, Canvas reveal, Particle canvas.
- **Visual DNA & Design Tokens**:
  - *Effects*: Border Beam (a light beam gliding around the border), Spotlight Card (a card reflecting light by the mouse pointer position), Meteor effect (a meteor-shower background).

---

## 4. Rebellious & Rule-Breaking Universe (Anti-Design & Gen Z)

### 4.1. Neubrutalism (Gumroad / Figma FigJam Style)

- **Emotion & Context**: Bold, playful, fearless, full of the energy of the independent maker (Indie Maker).
- **Open-source library**: [neobrutalism-components](https://github.com/ekmas/neobrutalism-components).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: vivid lemon yellow `#ffda59`, dreamy purple `#e0aaff`, pastel pink `#ff90e8`, mint green `#bbf7d0`.
  - *Borders*: thick solid black borders `border-3 border-black` (or `border-[2.5px]`).
  - *Box Shadow*: an absolutely hard shadow with no blur (0 blur): `box-shadow: 4px 4px 0px #000000`. On press (active state): the shadow disappears `translate-x-[2px] translate-y-[2px] shadow-none`.
  - *Typography*: `Lexend Mega`, `Space Grotesk`, uppercase bold `Public Sans`.

### 4.2. Y2K Cyber Glitch & Hologram

- **Emotion & Context**: The late 90s - early 2000s, the Millennium bug (Y2K bug) era, underground electronic music culture.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: metallic Chrome silver, fuchsia pink, fluorescent cyan.
  - *Visual Elements*: curvy fonts like inflated bubbles, virtual stickers, multi-directional Hologram rainbow bands, a text shake effect (text glitch).

---

## 5. Nostalgic Games & Geek Culture Universe (Retro Gaming & Geek)

### 5.1. 8-bit Console Pixel Art (NES.css)

- **Emotion & Context**: The 4-button Nintendo (NES) console, the classic Game Boy, fun and reminiscent of childhood.
- **Open-source library**: [NES.css](https://github.com/nostalgic-css/NES.css) (over 22,000 stars on GitHub).
- **Visual DNA & Design Tokens**:
  - *Borders*: borders built from multi-layer shadows to simulate pixel stair steps (no ordinary border).
  - *Elements*: speech balloons, segmented HP/MP bars, 8-bit heart icons.
  - *Typography*: `Press Start 2P`, a fixed-ratio pixel font.

### 5.2. 16-bit RPG Video Game (RPGUI)

- **Emotion & Context**: Legendary role-playing games such as Final Fantasy VI, Chrono Trigger, Diablo II.
- **Open-source library**: [RPGUI](https://github.com/RounArts/RPGUI).
- **Visual DNA & Design Tokens**:
  - *Borders & Frames*: frames carved from ancient gray stone or 16th-century oak.
  - *Elements*: grid-cell item chests (Inventory slots), a faux-leather book-page scrollbar, an iron knight gauntlet cursor.

### 5.3. Hacker Terminal & TUI (Terminal.css)

- **Emotion & Context**: The green screen of a movie-matrix hacker, a Linux admin console, absolute minimalism, resource-saving.
- **Open-source library**: [Terminal.css](https://github.com/panr/terminal-css).
- **Visual DNA & Design Tokens**:
  - *Color Palette*: pure black background `#000000`, phosphor fluorescent green text `#00ff66` or amber `#ffb000`.
  - *Elements*: a continuously blinking cursor `_` or `█`, frames built from ASCII/Unicode characters (`+---+`, `| |`).
  - *Typography*: `VT323`, `Fira Code`, `JetBrains Mono`.

---

## 6. Handcrafted & Organic Tactile Universe

### 6.1. Hand-Drawn Sketch (PaperCSS & Wired-Elements)

- **Emotion & Context**: A diagram sketched on a coffee-shop napkin, friendly, as if drawn by a human hand with a fountain pen.
- **Open-source libraries**:
  - [PaperCSS](https://github.com/papercss/papercss) — a rough frame like a drawing-paper page.
  - [Wired Elements](https://github.com/rough-stuff/wired-elements) — web components that generate random strokes with the Rough.js algorithm.
- **Visual DNA & Design Tokens**:
  - *Borders*: uneven wobbly borders: `border-radius: 255px 15px 225px 15px/15px 225px 15px 255px`.
  - *Typography*: `Patrick Hand`, `Architects Daughter`, `Kalam`.

### 6.2. Claymorphism (3D Soft Puffy Clay)

- **Emotion & Context**: Play-Doh modeling-clay toys, soft, safe, inviting touch and swipe.
- **Visual DNA & Design Tokens**:
  - *Shape*: maximum balloon-like corner radius `rounded-3xl`.
  - *Shadow*: a combination of 2 shadow layers (a soft outer shadow + an inner shadow reflecting light):
    `box-shadow: 16px 16px 32px #c8d0e7, -16px -16px 32px #ffffff, inset 4px 4px 8px rgba(255,255,255,0.6)`.

### 6.3. Classic Skeuomorphism

- **Emotion & Context**: Physically simulating real-world objects (a recording-studio mixing desk, a Swiss mechanical watch).
- **Visual DNA & Design Tokens**: brushed aluminum surfaces, chrome-plated toggle switches, rotary encoder knobs with precise graduation marks.

---

## 7. Academic, Press & Magazine Universe (Editorial & Bauhaus)

### 7.1. Swiss / Bauhaus International Style

- **Emotion & Context**: Absolute rational order, tight mathematical structure, modern European art.
- **Visual DNA & Design Tokens**:
  - *Color Palette*: cream-white background `#f7f7f5`, pure black `#111111`, accents in the 3 basic primary colors: flag Red `#e63946`, turmeric Yellow `#ffb703`, Blue `#1d3557`.
  - *Layout & Geometry*: a rigid asymmetric grid division, using basic geometric forms (circle, square, triangle) as architectural accents.
  - *Typography*: `Helvetica Neue`, `Arial`, large headings aligned absolutely to the left.

### 7.2. Luxury Editorial & Newspaper

- **Emotion & Context**: Luxury brand class, Vogue fashion magazine, The New York Times newspaper page.
- **Visual DNA & Design Tokens**:
  - *Typography*: prestigious Serif fonts: `Playfair Display`, `Cinzel`, `Merriweather`, headings with an ultra-thin 1px underline.
  - *Layout*: a multi-column newspaper layout (Multi-column layout), a large indented first letter (Drop Cap), generous padding for an airy feel.

---

## 8. Quick Selection Decision Matrix

| Archetype style | Recommended for (Best For) | Avoid for (Avoid For) | CSS implementation difficulty |
| :--- | :--- | :--- | :---: |
| **Linear Pro Max** | B2B SaaS, Devtools, AI products | Children's products, vintage fashion stores | Medium |
| **Cupertino iOS** | Mobile apps, FinTech, Lifestyle | Complex technical websites, gaming apps | Low |
| **Neubrutalism** | Creative landing pages, Gen Z, Web3 | Hospitals, traditional insurance, large banks | Very low |
| **Cyberpunk HUD** | SOC, security monitoring, Crypto, Games | News press, medical apps | High |
| **Windows XP / 98** | Personal portfolios, Easter eggs, Meme tools | Mass-market e-commerce | Medium |
| **Hacker Terminal** | Developer tools, CLI docs, personal blogs | Financial company sites for older audiences | Low |
| **Hand-Drawn Paper** | Children's education, mind-map tools, surveys | Bank payment systems, ERP dashboards | Medium |
