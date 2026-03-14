# CropFolio — Product Requirements Document

## Status: COMPLETE — All Phases Delivered

---

## 1. Problem Statement

Myanmar smallholder farmers lose 20-40% of potential income because they:

1. **Plant based on tradition, not data** — ignoring shifting climate patterns
2. **Concentrate on a single crop (rice)** — exposing 100% of income to one climate risk
3. **Sell at harvest** — when prices are at seasonal lows
4. **Have zero access to risk modeling tools** — while insurers and traders use sophisticated models

The information asymmetry between farmers and the market is the root cause of rural poverty cycles in Myanmar's agricultural economy.

---

## 2. Solution

**CropFolio** applies Modern Portfolio Theory (Markowitz optimization) to crop selection — treating a farmer's land allocation like an investment portfolio. It optimizes crop mix to maximize expected income while minimizing climate risk.

### Core Insight

Real FAOSTAT yield data (2010-2021, Myanmar) confirms the diversification opportunity: Rice vs Sesame has a **-0.49 correlation** — the strongest hedge available. However, pulse-pulse correlations are high (+0.5 to +0.9), meaning diversifying within pulses alone provides minimal risk reduction. The covariance matrix driving the optimizer is computed from 12 years of real yield data, not heuristic assumptions.

### Target Users

| User                                        | How They Use CropFolio                                       |
| ------------------------------------------- | ------------------------------------------------------------ |
| **Primary: Agricultural extension workers** | Advise farmer groups on optimal crop allocation per township |
| **Primary: Agri-cooperative managers**      | Plan collective planting across member farms                 |
| **Secondary: NGO program officers**         | Design climate-resilient agriculture programs                |
| **Tertiary: Microfinance loan officers**    | Assess agricultural credit risk                              |

### One-Line Value Prop

> "The same risk management tools Wall Street uses — adapted for Myanmar's farms."

---

## 3. User Stories

### Story 1: Climate Risk Assessment

**As** an extension worker,
**I want** to see the climate risk profile for a specific township and season,
**So that** I can understand what risks farmers in my area face this season.

**Acceptance Criteria:**

- Given a selected township and season (monsoon/dry)
- When I view the risk dashboard
- Then I see: drought probability (%), flood probability (%), temperature anomaly forecast, historical rainfall pattern vs. forecast
- And the data sources are cited (NASA POWER, Open-Meteo)

### Story 2: Crop Portfolio Optimization

**As** a cooperative manager,
**I want** to get an AI-optimized crop allocation for my area,
**So that** I can recommend a diversified planting plan that reduces collective risk.

**Acceptance Criteria:**

- Given a selected township, available crops, total land area, and risk tolerance
- When I request optimization
- Then I see: current typical allocation vs. optimized allocation (pie charts)
- And I see: expected income comparison, risk reduction percentage
- And the recommendation includes specific crop ratios (e.g., 60% rice, 25% black gram, 15% sesame)

### Story 3: Monte Carlo Simulation

**As** an extension worker,
**I want** to see simulated outcomes across many possible climate scenarios,
**So that** I can demonstrate to farmers WHY diversification protects their income.

**Acceptance Criteria:**

- Given a crop portfolio (current or optimized)
- When I run the Monte Carlo simulation
- Then I see an animated visualization of 1,000 simulated seasons
- And I see the income distribution curve for both monocrop vs. diversified
- And I see the probability of catastrophic loss (>50% income drop) for each

### Story 4: Crop Comparison

**As** a program officer,
**I want** to compare individual crop profiles (yield, price trend, climate sensitivity),
**So that** I can understand the building blocks of the portfolio.

**Acceptance Criteria:**

- Given the crop database
- When I select 2-3 crops
- Then I see side-by-side: historical yield, price trend (12-month), drought tolerance rating, flood tolerance rating, growing season
- And data is Myanmar-specific

### Story 5: Actionable Report Export

**As** a cooperative manager,
**I want** to export the recommendation as a simple Burmese-language report,
**So that** I can share it with farmer members who don't use computers.

**Acceptance Criteria:**

- Given an optimized portfolio
- When I click "Export Report"
- Then I get a printable PDF with: crop allocation visual, plain-language explanation in Burmese, seasonal calendar
- And no technical jargon (no "Markowitz", no "standard deviation")

---

## 4. Technical Architecture

### Stack

| Layer               | Technology                                                          | Justification                                                    |
| ------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **Frontend**        | React 18 + TypeScript + Tailwind CSS                                | Fast to build, component-driven, great charting ecosystem        |
| **Charts**          | Recharts + D3.js (for Monte Carlo animation)                        | Recharts for standard charts, D3 for the custom simulation viz   |
| **Backend**         | Python 3.10 + FastAPI                                               | Best ecosystem for data science + API in one codebase            |
| **ML/Optimization** | scikit-learn, scipy.optimize, numpy, pandas                         | Markowitz optimization, Monte Carlo simulation, data processing  |
| **AI**              | Google Gemini 2.0 Flash (free tier)                                 | AI-powered analysis and recommendations (optional)               |
| **Data Sources**    | NASA POWER API, Open-Meteo API, FAOSTAT 2010-2021, WFP HDX (static) | All confirmed to cover Myanmar. FAOSTAT provides real covariance |
| **Database**        | SQLite (hackathon) → PostgreSQL (production)                        | Zero setup for MVP, easy migration path                          |
| **Deployment**      | Vercel (frontend) + Railway (backend)                               | Free tier, instant deploys, no DevOps overhead                   |

### Architecture Diagram

```
┌─────────────────────────────────────────────────┐
│                   Frontend (React)                │
│  ┌───────────┐ ┌───────────┐ ┌────────────────┐  │
│  │ Risk      │ │ Portfolio │ │ Monte Carlo    │  │
│  │ Dashboard │ │ Optimizer │ │ Simulator      │  │
│  └─────┬─────┘ └─────┬─────┘ └───────┬────────┘  │
│        │              │               │            │
│        └──────────────┼───────────────┘            │
│                       │ REST API                   │
└───────────────────────┼───────────────────────────┘
                        │
┌───────────────────────┼───────────────────────────┐
│                  Backend (FastAPI)                  │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │ Climate Risk │ │ Portfolio    │ │ Monte Carlo│ │
│  │ Engine       │ │ Optimizer    │ │ Engine     │ │
│  └──────┬───────┘ └──────┬───────┘ └─────┬──────┘ │
│         │                │               │         │
│  ┌──────┴────────────────┴───────────────┴──────┐  │
│  │              Data Layer                       │  │
│  │  NASA POWER │ Open-Meteo │ FAOSTAT  │ WFP   │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

### API Endpoints

| Method | Endpoint                             | Description                             |
| ------ | ------------------------------------ | --------------------------------------- |
| GET    | `/api/v1/townships`                  | List Myanmar townships with coordinates |
| GET    | `/api/v1/climate-risk/{township_id}` | Climate risk profile for township       |
| GET    | `/api/v1/crops`                      | List available crops with profiles      |
| GET    | `/api/v1/crops/{id}`                 | Single crop detail                      |
| POST   | `/api/v1/optimize`                   | Run portfolio optimization              |
| POST   | `/api/v1/simulate`                   | Run Monte Carlo simulation              |
| GET    | `/api/v1/report/pdf`                 | Generate PDF report                     |
| POST   | `/api/v1/report/analyze`             | AI-powered portfolio analysis (Gemini)  |
| POST   | `/api/v1/compare`                    | Multi-township portfolio comparison     |

---

## 5. Data Model

### Crop Profile

```python
class CropProfile:
    id: str
    name_en: str
    name_mm: str  # Burmese
    category: str  # cereal, pulse, oilseed
    growing_season: str  # monsoon, dry, both
    drought_tolerance: float  # 0.0 - 1.0
    flood_tolerance: float  # 0.0 - 1.0
    avg_yield_kg_per_ha: float   # Source: FAOSTAT 2019-2021 mean
    yield_variance: float        # Source: FAOSTAT 2010-2021 CV
    avg_price_mmk_per_kg: float
    price_variance: float
```

Yield means and variance are sourced from FAOSTAT (element 5419 — yield hg/ha, country code 28 — Myanmar). The covariance matrix is computed from 12 annual yield observations (2010-2021).

### Climate Risk Profile

```python
class ClimateRisk:
    township_id: str
    season: str
    drought_probability: float
    flood_probability: float
    temp_anomaly_celsius: float
    rainfall_forecast_mm: float
    rainfall_historical_avg_mm: float
    confidence: float
```

### Portfolio Allocation

```python
class PortfolioAllocation:
    crops: list[CropWeight]  # crop_id + weight (0.0-1.0)
    expected_income_mmk: float
    income_std_dev: float
    sharpe_ratio: float
    prob_catastrophic_loss: float  # P(income drop > 50%)
    var_95: float  # Value at Risk, 95th percentile
```

---

## 6. Edge Cases

| Scenario                                   | Handling                                                                  |
| ------------------------------------------ | ------------------------------------------------------------------------- |
| Township with no climate data              | Fallback to nearest available grid point; show confidence warning         |
| Only one crop viable in region             | Skip optimization, show single-crop analysis with risk warning            |
| Extreme climate event (cyclone)            | All crops affected — show "hedge with off-season timing" advice           |
| Price data gaps (post-2021 disruptions)    | Use last available WFP data + inflation adjustment; flag data age         |
| User selects incompatible crops for season | Validate crop-season compatibility; reject with explanation               |
| Monte Carlo produces unrealistic outliers  | Cap simulations at ±3 standard deviations; remove outliers                |
| Very small farm (<1 acre)                  | Minimum 2-crop portfolio; acknowledge practical limits of diversification |

---

## 7. Testing Strategy

| Level                 | Tool                                | Coverage Target                                               |
| --------------------- | ----------------------------------- | ------------------------------------------------------------- |
| **Unit tests**        | pytest (backend), vitest (frontend) | 80% on optimization engine, risk calculations                 |
| **Integration tests** | pytest + httpx                      | All API endpoints, data pipeline                              |
| **Component tests**   | vitest + React Testing Library      | All chart components, form inputs                             |
| **E2E tests**         | Playwright                          | Critical flow: select township → optimize → simulate → export |

### Critical Test Scenarios

1. Optimization produces valid weights (sum to 1.0, all ≥ 0)
2. Monte Carlo results converge with sufficient iterations
3. Climate data fetch handles API timeout gracefully
4. Portfolio with negatively correlated crops shows lower risk than monocrop
5. Burmese text renders correctly in charts and exports

---

## 8. Build Milestones (Solo Developer — No Deadline Pressure)

### Phase 1: Core Engine (Focus: Get the Math Right) — COMPLETE

**Deliverables:**

- Crop profile database (6 Myanmar crops with FAOSTAT-backed yields and real covariance matrix)
- Climate data pipeline (NASA POWER + Open-Meteo integration)
- WFP price data loader (historical prices for key crops)
- Markowitz portfolio optimization engine (scipy.optimize)
- Monte Carlo simulation engine (numpy-based, 1,000 scenarios)
- Comprehensive unit tests for all calculations

**Quality Gate:** All optimization tests pass. Given sample input, produces valid diversified portfolio with demonstrably lower risk than monocrop. Math is verified against manual calculations.

### Phase 2: API Layer (Focus: Clean Architecture) — COMPLETE

**Deliverables:**

- FastAPI backend with all 10 endpoints
- Pydantic schemas for all request/response models
- Service layer separating business logic from routes
- Integration tests for all endpoints
- Error handling with meaningful messages
- API documentation auto-generated (FastAPI /docs)

**Quality Gate:** All endpoints return correct data. API docs are complete. Error cases handled gracefully.

### Phase 3: Frontend (Focus: The Wow Demo) — COMPLETE

**Deliverables:**

- React frontend with TypeScript + Tailwind
- Township selector (Myanmar map or searchable dropdown)
- Climate risk dashboard (visual risk indicators)
- Portfolio optimizer UI (current vs. optimized — pie charts + comparison)
- Monte Carlo visualization (THE wow moment — animated D3.js)
- Crop comparison view (side-by-side profiles)
- Component tests for all views

**Quality Gate:** Full user flow works end-to-end. The Monte Carlo animation makes people lean forward.

### Phase 4: Polish + Pitch Ready — COMPLETE

**Deliverables:**

- Burmese localization (UI strings + report export)
- PDF report export (printable, jargon-free)
- Performance optimization (Monte Carlo < 3 seconds)
- Edge case handling (all scenarios from Section 6)
- Deploy to Railway + Vercel (live demo URL)
- Pitch deck
- Demo script rehearsed

**Quality Gate:** Non-technical person can use the app and understand the output. Demo runs flawlessly 10 times in a row.

---

## 9. Out of Scope (Explicitly)

- Real-time SMS delivery to farmers (pitch as future feature)
- Satellite imagery analysis
- Individual farm-level soil data
- Weather station integration
- Mobile app (web-responsive is sufficient)
- User authentication / accounts (unnecessary for hackathon demo)
- Multi-language beyond English + Burmese
- Real financial transactions or insurance products
- Actual farmer onboarding

---

## 10. Business Model (For Pitch)

| Phase       | Revenue Model                                                      | Timeline     |
| ----------- | ------------------------------------------------------------------ | ------------ |
| **Phase 1** | Free for NGOs/cooperatives — build data moat, prove accuracy       | 0-12 months  |
| **Phase 2** | License risk engine to crop insurers and microfinance institutions | 12-24 months |
| **Phase 3** | Commodity supply intelligence for traders                          | 24+ months   |

**Total Addressable Market:**

- Myanmar agri-insurance: Growing (ADB/UNDP-funded pilots)
- Myanmar microfinance: ~$2B outstanding loans
- Global crop insurance: $40B+/year

---

## 11. Success Metrics (Hackathon)

| Metric                                                 | Target          |
| ------------------------------------------------------ | --------------- |
| Demo runs without errors                               | 100%            |
| Time from township selection to recommendation         | < 5 seconds     |
| Monte Carlo simulation completes                       | < 3 seconds     |
| Judges ask follow-up questions (engagement)            | 3+ questions    |
| Risk reduction demonstrated (monocrop vs. diversified) | > 20% reduction |
