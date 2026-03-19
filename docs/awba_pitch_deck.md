# CropFolio Pro x Awba — Pitch Deck Content

**Purpose:** 10-slide pitch for Myanma Awba Group partnership
**Audience:** Awba leadership, Htwet Toe product team
**Angle:** CropFolio as backend risk intelligence for Awba's distribution network

---

## Slide 1: Title

**CropFolio Pro**
သီးနှံ ရင်းနှီးမြှုပ်နှံမှု အကြံပေး စနစ်

_Data-Driven Crop-Fertilizer Intelligence for Myanmar Agriculture_

Presented to: Myanma Awba Group
Date: March 2026

---

## Slide 2: The Problem

**Myanmar's $12B agricultural sector runs on guesswork**

- 70% of farmers make planting decisions based on last year's results
- Fertilizer recommendations are generic — not soil or climate adjusted
- Distributors stock based on intuition → 15-25% annual overstock waste
- Climate volatility increasing: droughts +40% frequency since 2015

**Awba's 3.5M farmer reach is unmatched — but the advisory layer is missing**

ရာသီဥတုပြောင်းလဲမှုကြောင့် တောင်သူများ စွန့်စားရမှု ပိုများလာသည်

---

## Slide 3: Our Solution

**CropFolio Pro = Risk Intelligence API for Agricultural Distributors**

Three core capabilities:

1. **Crop Portfolio Optimization** — Markowitz theory applied to crop mix
   - Reduces income volatility by 25-40% through diversification
2. **Soil-Matched Fertilizer Recommendations** — SoilGrids + NPK matching
   - Right product, right rate, right place
3. **Monte Carlo Risk Simulation** — 1,000 scenario forecasting
   - Probability-based decision support, not single-point estimates

_Not a dashboard — a backend intelligence layer that feeds into YOUR systems_

---

## Slide 4: Why Awba + CropFolio

**Complement, not compete with Htwet Toe**

| Awba Has                          | CropFolio Adds                     |
| --------------------------------- | ---------------------------------- |
| 3.5M farmer network               | Risk modeling algorithms           |
| Field agent force                 | Soil-matched recommendations       |
| Fertilizer product catalog        | NPK optimization engine            |
| Htwet Toe farmer app              | Backend API intelligence           |
| Market presence in 300+ townships | Data from 50 townships (expanding) |

**Integration path:** CropFolio API → Htwet Toe advisory module

Htwet Toe တွင် ဒေတာအခြေခံ အကြံပြုချက်များ ထည့်သွင်းနိုင်ပါသည်

---

## Slide 5: How It Works

**Field Agent Workflow (3 steps)**

1. **Select** township + crops on Htwet Toe or CropFolio dashboard
2. **Generate** optimized crop-fertilizer pairing (10 seconds)
3. **Print** one-page Burmese PDF for the farmer

**Behind the scenes:**

- SoilGrids soil data (pH, NPK, CEC) for each township
- FAOSTAT yield history (2010-2021) for 11 crops
- WFP price data (2022-2025) for market volatility
- Markowitz portfolio optimization + 1,000 Monte Carlo sims

---

## Slide 6: Demo — Meiktila Township

**Meiktila dry season recommendation:**

- Rice 35% | Chickpea 25% | Sesame 20% | Groundnut 20%
- Expected income: 1,850,000 MMK/ha
- Risk reduction: 34.2% vs monocropping
- Catastrophic loss probability: 18.5% → 4.2%

**Top fertilizer match:**

- Rice → Urea (46-0-0) + Compound 20-10-10
- Chickpea → DAP (18-46-0) + TSP (0-46-0)

_[Screenshot: Dashboard + Burmese PDF side by side]_

---

## Slide 7: Demo Farm ROI Calculator

**Before committing to a demo farm, calculate the economics**

Example: 5 hectares in Magway, chickpea

- Input cost: 425,000 MMK (seed + DAP + labor)
- Expected revenue: 1,560,000 MMK
- Expected profit: 1,135,000 MMK
- Reimbursement risk: 8.3% (probability of loss)

**Awba benefit:** De-risk demo farms before deploying field resources

သရုပ်ပြခြံ မစတင်မီ စီးပွားရေးအရ အကဲဖြတ်နိုင်ပါသည်

---

## Slide 8: Data Coverage

**Current coverage (expanding weekly):**

| Metric        | Current           | Phase 2 Target        |
| ------------- | ----------------- | --------------------- |
| Crops         | 11                | 20+                   |
| Townships     | 50                | 100                   |
| Regions       | 14 states/regions | All 14                |
| Soil profiles | 50 townships      | 100                   |
| Fertilizers   | 8 formulations    | 15+ (Awba catalog)    |
| Price data    | 6 crops (WFP)     | 15+ (field collected) |

**Data confidence scoring:** Every data point marked high/medium/low

- Transparent about what we know vs. what we're estimating
- Awba field data can upgrade "low" confidence points to "high"

---

## Slide 9: Partnership Model

**Phase 1: Pilot (3 months, free)**

- Integrate CropFolio API with Htwet Toe backend
- 5 pilot townships in Awba's strongest markets
- Awba provides: field-collected prices, fertilizer catalog, farmer feedback
- CropFolio provides: API access, Burmese PDF generator, demo ROI calculator

**Phase 2: Scale (months 4-12)**

- Expand to 100+ townships
- Awba-specific fertilizer catalog integration
- Monthly intelligence reports for inventory planning
- Revenue share on premium advisory features

**Phase 3: Data Moat (year 2+)**

- Sentinel-1 SAR crop monitoring
- Credit-yield correlation for MFI partnerships
- Real-time price feeds from distributor network

---

## Slide 10: Ask

**What we need from Awba:**

1. **One meeting** with Htwet Toe product team (30 min)
2. **Fertilizer catalog** with current MMK prices (CSV/Excel)
3. **5 pilot townships** to validate recommendations
4. **Field agent feedback** on Burmese PDF format

**What we bring:**

- Working API (deployed, tested, 83+ test cases)
- Free pilot — no cost to Awba for Phase 1
- Open to white-labeling as "Powered by CropFolio" inside Htwet Toe

**Contact:**

- Technical: Pyae Sone (pyaesone@cropfolio.io)
- Field Operations: [Co-founder name] (Myanmar, +95...)

---

## Appendix: Technical Architecture

```
Htwet Toe App
     ↓ API call
CropFolio Pro API (FastAPI, Railway)
     ├── /recommend    → Crop-fertilizer optimization
     ├── /report/pdf   → Burmese PDF generator
     ├── /demo-roi     → Demo farm economics
     ├── /climate       → Risk assessment
     └── /crops         → 11 crop profiles with confidence
          ↓
    Data Layer
     ├── FAOSTAT yields (2010-2021)
     ├── WFP prices (2022-2025)
     ├── SoilGrids (50 townships)
     └── Awba fertilizer catalog
```
