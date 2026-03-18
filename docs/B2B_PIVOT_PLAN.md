# CropFolio Pro — B2B Pivot Plan

## Context

Field research from co-founder surveying Myanmar farmers revealed that **distributors and fertilizer companies (not farmers) are the real decision-makers** in Myanmar agriculture. Farmers are tradition-bound and follow distributor recommendations blindly. Distributors bear the financial risk — they grow demo crops at their own expense and reimburse farmers when recommendations fail. Big companies like **Awba Myanmar** spend millions on this trial-and-error process.

**Goal:** Pivot CropFolio from farmer-facing crop optimizer to a B2B decision-support platform for distributors/fertilizer companies. Build a demo-ready product in 2-3 weeks for co-founder to pitch to Awba Myanmar before leaving the country in April 2026.

**Core value prop:** Reduce distributor risk and maximize profit when recommending crop-fertilizer combinations by replacing guesswork with data-driven optimization backed by 12 years of FAOSTAT yield data, WFP prices, NASA climate data, and soil science.

---

## What We Keep (80% of existing engine)

The Markowitz optimizer, Monte Carlo simulator, climate risk engine, FAOSTAT/WFP correlations, and multi-township comparison are **domain-agnostic portfolio math**. They work identically for distributors. We reframe, not rebuild:

| Current (Farmer)                | New (Distributor)                                     |
| ------------------------------- | ----------------------------------------------------- |
| "What should I plant?"          | "What should I recommend & stock?"                    |
| Crop allocation % by land       | Product recommendation by region                      |
| Expected income/ha              | Expected farmer outcome + distributor margin          |
| Risk tolerance slider           | Portfolio strategy (conservative/balanced/aggressive) |
| Monte Carlo income distribution | Recommendation confidence distribution                |
| Catastrophic loss probability   | Reimbursement risk probability                        |

---

## What We Build New

### 1. Fertilizer Data Layer (Static JSON + Domain Logic)

**New files:**

- `backend/data/fertilizers.json` — 8 common Myanmar fertilizers (Urea 46-0-0, DAP 18-46-0, MOP 0-0-60, Compound 15-15-15, TSP 0-46-0, AS 21-0-0-24S, plus 2 more)
- `backend/data/soil_profiles.json` — Pre-downloaded SoilGrids data for all 25 townships (pH, nitrogen, organic carbon, clay/sand/silt, CEC)
- `backend/data/crop_nutrient_requirements.json` — NPK requirements per crop from FAO/IRRI (Rice: 60-30-30, Black Gram: 20-45-35, etc.)
- `backend/data/crop_fertilizer_matrix.json` — Effectiveness scores for each crop-fertilizer pair

**New domain modules:**

- `backend/app/domain/fertilizers.py` — `FertilizerProfile` dataclass, `SoilProfile` dataclass, `CropNutrientRequirement` dataclass
- `backend/app/domain/fertilizer_matcher.py` — Scoring algorithm: `score = crop_need_match * 0.4 + soil_deficiency_match * 0.3 + cost_efficiency * 0.2 + compatibility * 0.1`

**Extend existing:**

- `backend/app/domain/crops.py` — Add `nitrogen_requirement`, `phosphorus_requirement`, `potassium_requirement` fields to `CropProfile`

### 2. Recommendation Engine (New Core Endpoint)

**Pipeline:**

```
optimize_portfolio() --> crop weights (existing)
    |
get_soil_profile(township_id) --> soil nutrient status (new, static data)
    |
match_fertilizers(crops, soil, weights) --> ranked fertilizer recommendations (new)
    |
run_monte_carlo() with yield_boost from proper fertilization --> confidence scores (existing, extended)
    |
RegionRecommendation with crop + fertilizer + confidence + cost
```

**New API endpoints:**

- `GET /api/v1/fertilizers` — List fertilizer catalog
- `POST /api/v1/recommend` — Full recommendation: crops + fertilizers + confidence for one or more townships
- `POST /api/v1/demo-roi` — Demo crop ROI calculator (cost, success probability, reimbursement risk, alternatives)
- `GET /api/v1/soil/{township_id}` — Soil profile for a township

**New service:**

- `backend/app/services/recommendation_service.py` — Orchestrates optimize -> soil -> fertilizer match -> Monte Carlo -> AI advisory

### 3. Frontend: Wizard to Dashboard

**Replace** the linear 4-step wizard with a sidebar dashboard using `react-router-dom`:

```
/dashboard          — Overview: KPI cards + risk alerts (reuse MetricCard)
/recommend          — Recommendation engine: multi-township select -> crop select -> results
/recommend/:id      — Region detail: climate + soil + crop-fertilizer cards + Monte Carlo
/demo-calculator    — Demo crop ROI calculator
/reports            — AI-generated distributor advisory briefs (extend existing PDF/Gemini)
```

**New components:**

- `DashboardLayout.tsx` — Sidebar + topbar + router outlet
- `RecommendationCard.tsx` — Crop + fertilizer pairing + confidence gauge
- `FertilizerBadge.tsx` — NPK formulation display with color coding
- `SoilProfileCard.tsx` — Township soil summary (pH, nutrients, texture)
- `DemoROICalculator.tsx` — Form: select township + crop + area -> see cost/risk/alternatives
- `ConfidenceGauge.tsx` — Reuse SVG gauge pattern from climate dashboard

**Reuse directly:**

- `Card`, `MetricCard`, `Badge`, `LoadingSpinner`, `ErrorBoundary` — No changes
- `MonteCarloHistogram` — Relabel as "Confidence Distribution"
- `ClimateRiskDashboard` — Embed in recommendation detail (remove wizard navigation)
- Design system (colors, fonts, dark/light theme) — Keep as-is

**Retire:**

- Landing page sections (replace with B2B landing or skip for demo)
- 4-step wizard flow in App.tsx

### 4. AI Advisory for Distributors

**Extend** `backend/app/domain/ai_prompts.py` with distributor-oriented prompt:

- Business-focused insights (ROI, inventory, timing)
- Fertilizer application guidance in plain language
- Risk warnings specific to distributor's regions
- Bilingual output (English for executives, Burmese for field agents)

**Extend** `backend/app/services/ai_service.py`:

- `generate_distributor_advisory()` — New method using distributor prompt template
- `explain_fertilizer_recommendation()` — Plain-language fertilizer guidance

### 5. Soil Data Pre-Download Script

One-time script to query ISRIC SoilGrids API for all 25 townships:

- `backend/scripts/fetch_soil_data.py` — Queries `https://rest.isric.org/soilgrids/v2.0/properties/query` for pH, nitrogen, SOC, clay, sand, CEC at 0-30cm depth
- Stores results in `backend/data/soil_profiles.json`
- Build `SoilGridsClient` in `backend/app/infrastructure/soilgrids.py` with API-first + static fallback (same pattern as NASA POWER client)

---

## Implementation Schedule

### Week 1: Data + Backend (Days 1-5)

**Day 1-2: Fertilizer data layer**

- Create `FertilizerProfile`, `SoilProfile`, `CropNutrientRequirement` dataclasses
- Hardcode 8 fertilizer formulations in `fertilizers.json`
- Add NPK requirements for 6 crops from FAO/IRRI data
- Run SoilGrids pre-download script for 25 townships
- Add nutrient requirement fields to `CropProfile`

**Day 3-4: Recommendation engine**

- Build `fertilizer_matcher.py` with scoring algorithm
- Build `recommendation_service.py` orchestrating the full pipeline
- Build API endpoints: `/recommend`, `/demo-roi`, `/fertilizers`, `/soil/{township_id}`
- Add Pydantic schemas for new endpoints

**Day 5: AI prompts + integration tests**

- Add distributor advisory prompt templates
- Add `generate_distributor_advisory()` to AI service
- Integration tests for the full recommend pipeline
- Ensure `/recommend` responds under 3 seconds

### Week 2: Frontend Transformation (Days 6-10)

**Day 6-7: Dashboard shell**

- Add `react-router-dom`, build `DashboardLayout` with sidebar
- Build `/dashboard` overview page with KPI MetricCards
- Migrate from wizard to router-based navigation

**Day 8-9: Recommendation flow**

- Build `/recommend` page: multi-township selector + crop filter + "Generate Recommendations"
- Build `RecommendationCard` (crop + fertilizer + confidence)
- Build `FertilizerBadge`, `SoilProfileCard`, `ConfidenceGauge`
- Integrate existing Monte Carlo histogram as confidence distribution

**Day 10: Demo ROI + Reports**

- Build `/demo-calculator` page
- Extend report generation for distributor audience
- Polish responsive design, loading states, error handling

### Week 3: Demo Prep (Days 11-14)

**Day 11-12: Integration + polish**

- End-to-end flow testing
- Curate demo data for Mandalay + Magway (Awba's likely strong markets)
- Performance optimization

**Day 13: B2B landing page**

- Replace farmer-facing hero with B2B messaging
- "Request Demo" CTA
- Brand as "CropFolio Pro"

**Day 14: Pitch materials**

- Prepare 2-3 demo scenarios showing clear ROI
- One-page pitch document for Awba
- Demo script for co-founder

---

## Pitch Strategy for Awba Myanmar

### The Hook

"Your field agents recommend crops based on experience. CropFolio Pro runs 1,000 climate simulations in 3 seconds using 12 years of real FAOSTAT data. It tells you WHICH crops will thrive WHERE, WHICH fertilizer to pair, and the EXACT probability of success — before you spend a single kyat on demo farms."

### Demo Flow (5 minutes, on laptop)

1. Select a township Awba operates in -> Show climate risk from NASA satellite data
2. Run optimization -> Show optimized crop mix with 51% risk reduction vs. monocrop
3. Show fertilizer-crop matching -> "Rice in Meiktila needs Urea at 150 kg/ha, soil pH 7.8 confirms nitrogen priority"
4. Monte Carlo -> 1,000 simulations, point to catastrophic loss probability dropping from 40% to 10%
5. Demo ROI calculator -> "Before committing to a demo farm, here's the probability it succeeds and your reimbursement exposure"

### Business Model

- **Phase 1:** Free 3-month pilot with 2-3 townships. Awba provides field data, we provide optimized recommendations.
- **Phase 2:** SaaS subscription 50-300 lakh MMK/year tiered by region count and features.
- **ROI pitch:** "If you lose 15M MMK/season on failed demos and this reduces failures by 40%, it pays for itself in one season."

### Key Objection Handlers

- "Our agents already know this" -> "CropFolio amplifies their intuition with quantitative data they can't compute mentally"
- "Data isn't accurate enough" -> "That's exactly why we want your field data — it becomes the ground truth that makes the model unbeatable for YOUR regions"
- "It's just a prototype" -> "The math is production-grade. The partnership is what makes it enterprise-ready."

---

## Critical Files to Modify

### Backend (modify)

- `backend/app/domain/crops.py` — Add NPK requirement fields
- `backend/app/domain/ai_prompts.py` — Add distributor advisory prompts
- `backend/app/services/ai_service.py` — Add distributor advisory method
- `backend/app/api/v1/__init__.py` — Register new routes

### Backend (create new)

- `backend/data/fertilizers.json` — Fertilizer catalog
- `backend/data/soil_profiles.json` — Pre-downloaded SoilGrids data
- `backend/data/crop_nutrient_requirements.json` — FAO/IRRI NPK data
- `backend/data/crop_fertilizer_matrix.json` — Crop-fertilizer effectiveness scores
- `backend/app/domain/fertilizers.py` — Dataclasses
- `backend/app/domain/fertilizer_matcher.py` — Matching algorithm
- `backend/app/infrastructure/soilgrids.py` — SoilGrids client
- `backend/app/services/recommendation_service.py` — Orchestration
- `backend/app/api/v1/routes/recommend.py` — New endpoints
- `backend/app/api/v1/routes/fertilizers.py` — Fertilizer catalog endpoints
- `backend/app/api/v1/schemas/recommend.py` — Pydantic models
- `backend/app/api/v1/schemas/fertilizers.py` — Pydantic models
- `backend/scripts/fetch_soil_data.py` — One-time SoilGrids download

### Frontend (modify)

- `frontend/src/App.tsx` — Replace wizard with router
- `frontend/package.json` — Add react-router-dom

### Frontend (create new)

- `frontend/src/components/layout/DashboardLayout.tsx`
- `frontend/src/components/layout/Sidebar.tsx`
- `frontend/src/components/dashboard/DashboardOverview.tsx`
- `frontend/src/components/recommend/RecommendPage.tsx`
- `frontend/src/components/recommend/RecommendationCard.tsx`
- `frontend/src/components/recommend/FertilizerBadge.tsx`
- `frontend/src/components/recommend/SoilProfileCard.tsx`
- `frontend/src/components/recommend/ConfidenceGauge.tsx`
- `frontend/src/components/demo/DemoROICalculator.tsx`
- `frontend/src/api/recommend.ts`
- `frontend/src/api/fertilizers.ts`
- `frontend/src/hooks/useRecommend.ts`
- `frontend/src/types/recommend.ts`
- `frontend/src/types/fertilizer.ts`

---

## Verification

1. **Backend:** `pytest` passes, `/recommend` endpoint returns crop + fertilizer recommendations with confidence scores in <3s
2. **Frontend:** `npm run build` succeeds, dashboard renders with real data from backend
3. **E2E:** Select township -> Get recommendation -> View Monte Carlo confidence -> Generate PDF report
4. **Demo scenarios:** Mandalay dry season and Magway dry season produce compelling, differentiated recommendations
5. **Pitch readiness:** Co-founder can run the demo flow in 5 minutes without technical assistance

---

## Data Sources

| Source                          | Data Type                   | Access                         |
| ------------------------------- | --------------------------- | ------------------------------ |
| SoilGrids (ISRIC)               | pH, N, SOC, texture, CEC    | Free REST API, 250m resolution |
| FAO Bulletin 16                 | NPK guidelines per crop     | PDF, hardcode                  |
| IRRI Rice Knowledge Bank        | Rice nutrient calculator    | Web reference                  |
| Myanmar DoA Fertilizer Practice | Actual vs recommended rates | Published paper (MDPI)         |
| Awba Group                      | Product line info           | Public website                 |
| FAOSTAT (existing)              | Yield data 2010-2021        | Already integrated             |
| WFP (existing)                  | Price data 2022-2025        | Already integrated             |
| NASA POWER (existing)           | Historical rainfall         | Already integrated             |
| Open-Meteo (existing)           | Weather forecasts           | Already integrated             |
