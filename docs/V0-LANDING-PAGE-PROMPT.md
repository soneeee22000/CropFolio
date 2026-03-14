# CropFolio Landing Page — v0 Generation Prompt

Copy everything below the line into v0.dev as a single prompt.

---

Build a stunning, premium landing page for "CropFolio" — a web app that applies Modern Portfolio Theory (Markowitz optimization) to crop selection for Myanmar smallholder farmers. It optimizes crop mix to maximize expected income while minimizing climate risk.

## Design Direction

**Aesthetic:** "Financial Times data visualization meets Apple keynote." Restrained luxury — not flashy, not startup-y. Every pixel intentional. Dark/light alternating sections. Editorial typography.

**Typography:**

- Headlines: `DM Serif Display` (Google Font) — elegant serif
- Body: `DM Sans` (Google Font) — clean geometric sans
- Data/Numbers: `JetBrains Mono` (Google Font) — tabular monospace
- Import all three from Google Fonts

**Color Palette:**

- Dark sections: `#1A1A18` bg, `#FAFAF8` text
- Light sections: `#FAFAF8` bg, `#1A1A18` text
- Primary green: `#1B7A4A`
- Gold accent: `#B8860B` (for the "10%" hero number)
- Text secondary: `#6B6A65`
- Text tertiary: `#A3A29D`
- Border: `#E8E6E1`

**NO gradient backgrounds on buttons. Solid colors only.**
**NO Inter, Roboto, or system fonts.**

## Page Sections

### 1. HERO (Full viewport, dark background #1A1A18)

Center-aligned. Generous whitespace.

```
[overline — 11px, uppercase, tracking-[0.2em], #A3A29D]
MODERN PORTFOLIO THEORY FOR AGRICULTURE

[hero number — 120px+, DM Serif Display, white, animated counter from 0→40]
40%

[subtext — 20px, DM Sans, #A3A29D]
of Myanmar's rice farmers face catastrophic income loss
in any given season.

[after animation: line-through on 40%, then reveal:]
→ 10%  [in gold #B8860B, DM Serif Display]

[CTA button — solid #1B7A4A, white text, uppercase, tracking-wide, rounded-lg, py-4 px-8]
Try CropFolio →

[secondary link — small, text-tertiary, underline]
See how it works ↓
```

The hero animation sequence:

1. "40%" counts up from 0 (1.5s)
2. Pause 1s
3. "40%" gets line-through decoration
4. "10%" fades in next to it in gold
5. Subtitle text: "CropFolio reduces that to 10%."

### 2. THE PROBLEM (Light bg #FAFAF8, two columns)

Left column (text):

```
[overline] THE PROBLEM
[heading — DM Serif Display, 36px] One Crop. One Risk.
[body] 70% of Myanmar's farmers grow rice as their only crop.
When the monsoon fails — Loss. When it floods — Loss.
No hedge. No safety net. No diversification.

But what if crops could be managed like a financial portfolio?
```

Right column: An animated SVG visualization showing income volatility:

- One tall bar labeled "Rice Only" that wobbles dramatically (high amplitude sine wave)
- Three shorter bars labeled "Rice + Pulses + Oilseeds" that wobble gently (low amplitude)
- Loop animation demonstrating stability through diversification

### 3. THE INSIGHT (Dark bg #1A1A18, full width)

```
[overline] THE INSIGHT
[heading — DM Serif Display, 36px, white] Portfolio Theory for Farms
```

Two cards side by side on dark background:

- Card 1 (border only, no fill): **"In Finance"** — "Diversify stocks to reduce portfolio risk. Negatively correlated assets cancel out volatility. Nobel Prize, 1952."
- Card 2 (border only, no fill): **"In Agriculture"** — "Diversify crops to reduce climate risk. Rice survives floods. Sesame survives drought. Same math. Different asset class."

Between the cards, a subtle animated connecting line or arrow showing the cross-domain bridge.

### 4. HOW IT WORKS (Light bg, 4 steps)

```
[overline] HOW IT WORKS
[heading — DM Serif Display] Four Steps to Climate Resilience
```

4 steps in a horizontal row (stack on mobile):

1. **Select Township** — "Choose from 25 Myanmar agricultural townships"
2. **Assess Climate Risk** — "NASA satellite data for drought and flood probability"
3. **Optimize Portfolio** — "Markowitz optimization finds the ideal crop mix"
4. **Simulate 1,000 Seasons** — "Monte Carlo proves the diversification benefit"

Each step has a large number (1-4) in DM Serif Display at 48px, muted color, with the title below in bold DM Sans and description in regular.

Animate: steps fade in + slide up with stagger on scroll.

### 5. KEY METRICS (Light bg, centered)

Three large metric cards in a row:

```
51.3%              1.5M MMK           10%
[JetBrains Mono]   [JetBrains Mono]   [JetBrains Mono]
Risk Reduction     Expected Income    Catastrophic Loss
vs Monocrop        per Hectare        Probability
```

The middle card should have a gold accent border (the accent color #B8860B).
Animate: numbers count up from 0 on viewport entry.

Small caption below: "Based on Magway township, monsoon season, rice + black gram + sesame portfolio"

### 6. TECH CREDIBILITY (Light bg, minimal)

```
[overline] BUILT WITH

[row of text badges, no icons needed]
Python · FastAPI · React · TypeScript · D3.js · scipy

[stats row below]
63 Tests · 88% Coverage · 8 API Endpoints · Zero AI Costs
```

### 7. CTA FOOTER (Dark bg #1A1A18, centered, generous padding)

```
[heading — DM Serif Display, 36px, white]
See it for yourself.

[CTA button — same style as hero]
Launch CropFolio →

[small text — #A3A29D]
AI for Climate-Resilient Agriculture Hackathon 2026
Impact Hub Yangon × UNDP Myanmar
```

### 8. STICKY NAV (optional)

Minimal nav bar at top:

- Left: "CropFolio" in DM Serif Display
- Right: "How It Works" · "Try App" · "Admin" links
- Transparent on hero, solid white on scroll with backdrop blur

## Technical Requirements

- React + TypeScript + Tailwind CSS
- Scroll-triggered animations using IntersectionObserver (no framer-motion or heavy libs)
- requestAnimationFrame for the counter animation
- Responsive: desktop (1280px+), tablet (768px), mobile (375px)
- Import Google Fonts: DM Serif Display, DM Sans, JetBrains Mono
- NO gradient backgrounds on any element
- The "Try CropFolio →" button should link to `/app`
- The "Admin" nav link should link to `/admin`

## What Makes This Landing Page Different

This is NOT a generic SaaS landing page. It's a **data story**. The hero doesn't say "Welcome to CropFolio." It says "40%" — a devastating number — and then shows how CropFolio changes it. Every section builds on the previous one. By the time the visitor reaches the CTA, they understand the problem, the insight, and the proof. The design reflects this narrative arc through alternating dark/light sections that create rhythm and pacing.
