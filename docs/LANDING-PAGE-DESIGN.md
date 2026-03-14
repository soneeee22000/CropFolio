# CropFolio Landing Page — Design Specification

## Design Direction: "Financial Times meets Apple Keynote"

Not a SaaS template. Not a startup landing page. An **editorial data story** that builds tension, reveals an insight, and invites action. Every scroll reveals one more piece of the puzzle until the visitor understands — viscerally, not intellectually — why diversification matters.

---

## Page Structure (Single Page, Scroll-Driven)

### Section 1: Hero — "The Problem in One Number"

**Layout:** Full viewport height. Dark background (`#1A1A18`). Centered.

**Content:**

```
[overline: small, uppercase, tracked]
MODERN PORTFOLIO THEORY FOR AGRICULTURE

[hero stat: massive, animated counter]
40%
[subtext]
of Myanmar's rice farmers face catastrophic income loss
in any given season.

[second line, after 1s delay]
CropFolio reduces that to 10%.

[CTA button]
Try CropFolio →

[secondary link]
See how it works ↓
```

**Animation:** The "40%" counter animates from 0 to 40 on scroll-into-view (1.5s, ease-out). Then after 1s pause, a line strikes through "40%" and "10%" fades in beside it in gold (`#B8860B`). This is the entire pitch in 3 seconds.

**Typography:** The number is 120px+ `DM Serif Display`. The subtext is 20px `DM Sans`. The overline is 11px uppercase `DM Sans` with wide letter-spacing.

---

### Section 2: The Insight — "Why Rice Farmers Lose"

**Layout:** Two-column on desktop. Left: text. Right: animated visualization.

**Background:** Warm off-white (`#FAFAF8`).

**Left column:**

```
[overline] THE PROBLEM
[heading] One Crop. One Risk.
[body] 70% of Myanmar's farmers grow rice as their only crop.
When the monsoon fails, they lose everything. When it floods,
they lose everything. There is no hedge.

But rice isn't the only option.
```

**Right column:** An animated SVG showing:

- A single green bar (rice) that fluctuates with a sine wave (income volatility)
- Below it, 3 smaller bars (rice + pulse + oilseed) that fluctuate with lower amplitude
- The diversified bars' combined height matches the rice bar but with visibly less wobble
- Loop animation, 4 seconds total

---

### Section 3: The Cross-Domain Insight — "What Wall Street Knows"

**Layout:** Full-width. Dark section (`#1A1A18`).

**Content:**

```
[overline] THE INSIGHT
[heading] Portfolio Theory for Farms

[two cards side by side]

Card 1: "In Finance"
- Stocks have different risk profiles
- Negatively correlated assets reduce portfolio risk
- Markowitz won a Nobel Prize for proving this in 1952

Card 2: "In Agriculture"
- Crops have different climate tolerances
- Rice survives floods; sesame survives drought
- CropFolio applies the same math to crop selection
```

**Visual:** Between the two cards, a subtle animated line connects them — a visual metaphor for the cross-domain bridge.

---

### Section 4: How It Works — "Four Steps"

**Layout:** Horizontal scroll or vertical stack with sticky numbers.

**Background:** Off-white.

```
1. SELECT TOWNSHIP
   Choose from 25 Myanmar agricultural townships

2. ASSESS CLIMATE RISK
   Real-time drought and flood probability from NASA satellite data

3. OPTIMIZE PORTFOLIO
   Markowitz optimization finds the ideal crop mix

4. SIMULATE 1,000 SEASONS
   Monte Carlo simulation proves the diversification benefit
```

Each step has a screenshot/mockup of the actual app UI for that step.

---

### Section 5: The Demo Moment — Live Stats

**Layout:** Full-width, centered.

**Background:** Subtle gradient from off-white to light sage.

**Content:** Three large metric cards in a row, animated counters:

```
51.3%          1.5M MMK        10%
Risk Reduction  Expected Income  Catastrophic Loss
vs Monocrop     per Hectare      Probability
```

Below: "Based on Magway township, monsoon season, rice + black gram + sesame portfolio"

---

### Section 6: Tech Credibility

**Layout:** Minimal. Logos/icons row.

```
[overline] BUILT WITH
[row of tech badges/icons]
Python · FastAPI · React · D3.js · scipy · NASA POWER · Open-Meteo

63 automated tests · 88% backend coverage · Zero external AI costs
```

---

### Section 7: CTA Footer

**Layout:** Dark background. Centered.

```
[heading] See it for yourself.

[large CTA button] Launch CropFolio →

[small text]
Built for the AI for Climate-Resilient Agriculture Hackathon 2026
Impact Hub Yangon × UNDP Myanmar
```

---

## Admin Dashboard Mock

**Route:** `/admin` with login gate

**Login page:** Minimal. DM Serif Display "CropFolio Admin". Email + password fields. Login button. Hardcoded: admin / 12345.

**Dashboard (after login):** Simple mockup showing:

- Header: "CropFolio Admin" with logout button
- Cards: "25 Townships", "6 Crops", "1,247 Optimizations Run", "892 Reports Generated"
- Recent activity table (mock data)
- This is a MOCK — no real backend. Just static React components.

---

## Technical Approach

- Add `react-router-dom` for routing: `/` (landing), `/app` (wizard), `/admin` (dashboard)
- Landing page is a single component with scroll-triggered animations
- Use `IntersectionObserver` for scroll animations (no heavy library)
- Counter animation with `requestAnimationFrame`
- Admin uses localStorage for mock auth state

---

## Color Palette (Landing Page Specific)

The landing page uses a **darker** palette than the app to create contrast:

| Element             | Color                     |
| ------------------- | ------------------------- |
| Dark sections bg    | `#1A1A18`                 |
| Dark sections text  | `#FAFAF8`                 |
| Light sections bg   | `#FAFAF8`                 |
| Light sections text | `#1A1A18`                 |
| Hero stat           | `#FFFFFF` at 120px        |
| Gold accent         | `#B8860B`                 |
| CTA button          | `#1B7A4A` (primary green) |
| Overlines           | `#A3A29D` (text-tertiary) |

---

## Animation Inventory

| Element                            | Type               | Trigger        | Duration       |
| ---------------------------------- | ------------------ | -------------- | -------------- |
| Hero "40%" counter                 | Count up from 0    | Page load      | 1.5s           |
| "40%" strikethrough + "10%" reveal | Sequential         | After counter  | 1s + 0.5s      |
| Income volatility bars             | Looping sine wave  | Viewport entry | 4s loop        |
| Step numbers                       | Fade in + slide up | Viewport entry | 0.4s staggered |
| Metric counters                    | Count up           | Viewport entry | 1s             |
| Cards                              | Fade in up         | Viewport entry | 0.4s staggered |

---

## Success Criteria

- [ ] Landing page loads in < 2 seconds
- [ ] Hero animation plays on first visit
- [ ] Scroll animations trigger correctly
- [ ] "Try CropFolio →" navigates to the app wizard
- [ ] Admin login works with admin / 12345
- [ ] Admin dashboard shows mock metrics
- [ ] Mobile responsive (stacks vertically)
- [ ] No layout shift during animations
- [ ] DM Serif Display + DM Sans + JetBrains Mono typography consistent with app
