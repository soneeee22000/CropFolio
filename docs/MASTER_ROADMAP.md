# CropFolio Pro -- Master Strategic Roadmap

**Version:** 1.0
**Date:** March 19, 2026
**Authors:** Pyae Sone (Technical Lead) + Co-founder (Field Operations, Myanmar)
**Status:** Active -- governing document for all decisions through June 2026

---

## How to Use This Document

This is THE decision-making document for CropFolio Pro. Every feature request, partnership conversation, and engineering sprint should be checked against this roadmap. If an activity does not appear here, it does not get done.

**Source documents synthesized:** STRATEGIC_ANALYSIS.md, awba_research_findings.txt, data_moat_findings.txt, moat_research_notes.txt, Strategic Roadmap, Irreplaceability Blueprint, B2B_PIVOT_PLAN.md, README.md

---

## 1. WHERE WE ARE -- Honest Current State

| Dimension | Score | Reality |
|---|---|---|
| Code Quality | **8/10** | 83 tests, clean architecture, FastAPI + React/TS, deployed Railway + Vercel |
| Data Quality | **3/10** | FAOSTAT 2010-2021 (stale), fabricated sesame price, fertilizer prices 30-50% below market, 6 crops, 25 townships |
| Technical Depth | **5/10** | Textbook Markowitz + Monte Carlo. Not a moat. |
| Market Fit | **2/10** | Zero customer validation. Wrong form factor (web vs Android/Viber) |
| Revenue Potential | **1/10** | No SaaS payment infrastructure in Myanmar |
| Competitive Moat | **1/10** | All-public data, textbook algorithms |
| Htwet Toe Integration Angle | **7/10** | Awba already has farmer app. We complement as backend intelligence |

**Overall: 3.7/10 as B2B product. 7/10 as hackathon project.**

**What is dangerously wrong:** Fabricated data, national-level yields for township recommendations, pre-coup economics, wrong form factor, zero customer conversations.

---

## 2. WHERE WE NEED TO BE -- The 10/10 Vision

CropFolio becomes the **Risk Intelligence Layer** for Myanmar agriculture. Not a dashboard -- the foundational data infrastructure distributors, MFIs, and insurers cannot operate without.

**The 10/10 Moat (4 layers):**
1. **Hyper-Local Real-Time Prices** -- Township daily prices from distributor network
2. **Sentinel-1 SAR Pipeline** -- Cloud-penetrating radar for planting/flood monitoring
3. **Credit-Yield Correlation Engine** -- Fusing MFI loans with SAR-verified planting
4. **Bayesian Belief Network Core** -- Adaptive model that learns from every recommendation

**Revenue targets by customer segment:**

| Segment | Value Prop | Year 1 Potential |
|---|---|---|
| International Orgs (UNDP/FAO/WB) | Climate resilience assessments (USD contracts) | $10K-80K |
| Distributors (Awba) | Backend API for Htwet Toe + demo farm ROI | $0-6K (pilot) |
| MFIs (Proximity Finance) | Agricultural loan risk scoring | $0-20K |

---

## 3. 90-DAY SPRINT PLAN

### Phase 1: Customer Discovery + Data Collection (Days 1-14)

**Co-founder tasks (Myanmar, in-person):**
- Interview 5-10 distributors (use structured interview script)
- Collect current market prices for 10 crops in 3 townships
- Collect current fertilizer prices from 3 distributors
- Get 1 distributor to review a CropFolio recommendation
- Validate Burmese translations with native speakers

**Engineering tasks (remote):**
- Remove all fabricated/synthetic data
- Build one-page Burmese PDF generator (the actual MVP)
- Add 5 new crops (corn, sugarcane, onion, chili, potato)
- Expand to 50 townships
- Prepare Awba pitch deck (10 slides, bilingual)

**Exit criteria:** 5+ interviews, go/no-go decision on Awba pitch.

### Phase 2: Data Quality + Htwet Toe Strategy (Days 15-45)

- Integrate field-collected prices
- Add post-coup MMK inflation adjustment
- Source sub-national yield data
- Reverse-engineer Htwet Toe app
- Design API integration proposal for Awba
- Initiate 2+ international org conversations

**Exit criteria:** Data quality 5/10+, Htwet Toe assessment complete, pilot partner identified.

### Phase 3: Bayesian Engine + SAR + Pilot (Days 46-90)

- BBN prototype (pgmpy) for 3 crops
- Sentinel-1 SAR proof-of-concept for rice detection
- Deliver first recommendations to pilot partner
- Establish feedback collection mechanism
- At least 1 revenue conversation active

---

## 4. AWBA PITCH STRATEGY

### The Discovery: Htwet Toe Is Our Entry Point

**Old pitch (wrong):** "Buy our SaaS dashboard."
**New pitch (right):** "We make Htwet Toe smarter. For free. In exchange for field data."

### 10-Slide Pitch Deck

1. The problem Awba already knows (demo farm costs)
2. What data reveals (rice-sesame -0.49 correlation)
3. CropFolio: Risk Intelligence Engine
4. Live demo: pick a township
5. The Htwet Toe integration
6. The data flywheel
7. Pilot proposal (3 townships, 1 season, zero cost)
8. What we need from Awba
9. Business case (if 20% fewer demo failures, pilot pays for itself)
10. Team

### Key Objection Handlers

| Objection | Response |
|---|---|
| "Our agents know this" | "CropFolio gives every agent the confidence of your best one" |
| "Data isn't accurate" | "That's why we want YOUR data -- partnership makes it unbeatable for YOUR regions" |
| "We don't pay for software" | "Pilot is free. We're proposing a data partnership, not selling software" |
| "We already have Htwet Toe" | "We make Htwet Toe smarter. Complementary, not competitive" |

---

## 5. TECHNICAL EVOLUTION

```
TODAY (Moat: 1/10)        6 MONTHS (4/10)          12-18 MONTHS (8/10)
Monte Carlo + Public Data -> Hybrid MC+BBN+Expert -> Full Bayesian+SAR+RTP
6 crops, 25 townships       10-15 crops, 50+ twp    20+ crops, 100+ twp
```

**Key decisions:** BBN library = pgmpy, SAR processing = Google Earth Engine, Mobile delivery = Viber Bot + PDF, API pattern = REST with webhooks for Htwet Toe.

---

## 6. DATA MOAT BUILDING BLOCKS (Ranked)

**Tier 1 (Do First):** Distributor-sourced prices, field feedback on recommendations, expert knowledge encoding
**Tier 2 (Do Second):** Sub-national yield data, Sentinel-1 SAR, seasonal planting calendar
**Tier 3 (Plan For):** Credit-yield correlation, logistics/conflict index, per-plot yield measurements

**Compounding effect:** Season 1 = 1/10 moat -> Season 5 = 9/10 moat. Each season of data collection makes competitors 2+ years behind.

---

## 7. SUCCESS METRICS

**30 days:** 5+ interviews, real prices collected, fabricated data removed, Burmese PDF working, go/no-go on Awba
**60 days:** Data quality 5/10+, pilot partner identified, 2+ intl org conversations, Htwet Toe assessed
**90 days:** BBN prototype, SAR proof-of-concept, first recommendations delivered, 1+ revenue conversation

**The ultimate win condition:** A single sentence from a customer -- "This recommendation was correct, and I would not have made this decision without CropFolio."

---

*This document governs all CropFolio decisions through June 2026. If reality diverges from this plan, update the plan -- do not pretend reality matches the plan.*
