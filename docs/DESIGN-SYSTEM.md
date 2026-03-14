# CropFolio Design System — Premium UI Specification

## Design Philosophy: Restrained Luxury

Every visual decision is deliberate. Whitespace is generous. Typography is distinctive.
Data visualizations feel like curated art pieces, not chart library defaults.

Inspired by: Apple product pages, Bloomberg Terminal, Financial Times data viz, Balenciaga editorial.

---

## Typography

| Token       | Size   | Weight | Font             | Usage                      |
| ----------- | ------ | ------ | ---------------- | -------------------------- |
| `display`   | 36px   | 400    | DM Serif Display | Page titles                |
| `heading-1` | 28px   | 400    | DM Serif Display | Section headings           |
| `heading-2` | 22px   | 400    | DM Serif Display | Card titles                |
| `heading-3` | 16px   | 500    | DM Sans          | Subsection headings        |
| `body`      | 15px   | 400    | DM Sans          | Default body text          |
| `caption`   | 13px   | 400    | DM Sans          | Secondary text, labels     |
| `overline`  | 11px   | 500    | DM Sans          | Category labels, uppercase |
| `data`      | varies | 500    | JetBrains Mono   | Numbers, metrics, axes     |

Myanmar script: `Padauk` (unchanged)

---

## Color Palette

### Core

| Token              | Hex       | Usage                            |
| ------------------ | --------- | -------------------------------- |
| `surface`          | `#FAFAF8` | Page background (warm off-white) |
| `surface-elevated` | `#FFFFFF` | Cards                            |
| `surface-subtle`   | `#F5F4F0` | Subtle backgrounds               |
| `border`           | `#E8E6E1` | Card borders (warm gray)         |
| `border-subtle`    | `#F0EEEA` | Very subtle separators           |
| `text-primary`     | `#1A1A18` | Headlines                        |
| `text-secondary`   | `#6B6A65` | Body text                        |
| `text-tertiary`    | `#A3A29D` | Captions, placeholders           |
| `primary`          | `#1B7A4A` | Primary actions (deep green)     |
| `primary-hover`    | `#15613B` | Hover state                      |
| `primary-subtle`   | `#E8F5EE` | Primary light background         |
| `accent`           | `#B8860B` | Gold highlight                   |
| `danger`           | `#C43B3B` | Risk, monocrop (muted red)       |
| `warning`          | `#D4940A` | Moderate risk (rich amber)       |

### Crop Colors (muted, same saturation band)

| Crop       | Hex       | Name           |
| ---------- | --------- | -------------- |
| Rice       | `#3A8F5C` | Deep sage      |
| Black Gram | `#C4923A` | Antique gold   |
| Green Gram | `#4A8B9E` | Muted teal     |
| Chickpea   | `#7B6BA5` | Dusty lavender |
| Sesame     | `#B85A5A` | Terracotta     |
| Groundnut  | `#A67B5B` | Warm umber     |

---

## Animation Tokens

| Property            | Value                            |
| ------------------- | -------------------------------- |
| `--ease-out`        | `cubic-bezier(0.16, 1, 0.3, 1)`  |
| `--ease-in-out`     | `cubic-bezier(0.65, 0, 0.35, 1)` |
| `--duration-fast`   | `150ms`                          |
| `--duration-normal` | `300ms`                          |
| `--duration-slow`   | `600ms`                          |

---

## Component Patterns

- **Cards**: No shadows. Border + whitespace for hierarchy. `rounded-xl`, `p-8`.
- **Buttons**: Solid bg, no gradients. Uppercase DM Sans, `tracking-wide`.
- **Inputs**: Bottom-border only. No box borders.
- **Badges**: Minimal — border-only for info, colored for risk levels.
- **Metrics**: JetBrains Mono values, uppercase DM Sans labels.
- **Charts**: Donut (not pie). JetBrains Mono axes. Muted palette.

---

## The Monte Carlo Gallery Piece

- Settle-bounce easing (`d3.easeBackOut.overshoot(0.3)`)
- JetBrains Mono axes, horizontal labels
- Mean line as floating tag (dark bg, white text)
- Monocrop as smooth curve overlay (`d3.curveBasis`)
- Subtle grid lines, P5/P95 markers
- Chart background: `#F5F4F0`
