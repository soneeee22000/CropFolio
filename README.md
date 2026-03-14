<p align="center">
  <h1 align="center">CropFolio</h1>
  <p align="center">
    <strong>Portfolio Theory for Climate-Resilient Farming in Myanmar</strong>
  </p>
  <p align="center">
    <a href="#live-demo">Live Demo</a> &middot;
    <a href="#the-problem">Problem</a> &middot;
    <a href="#the-solution">Solution</a> &middot;
    <a href="#how-it-works">How It Works</a> &middot;
    <a href="#tech-stack">Tech Stack</a> &middot;
    <a href="#quick-start">Quick Start</a>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black" alt="React" />
    <img src="https://img.shields.io/badge/TypeScript-strict-3178C6?logo=typescript&logoColor=white" alt="TypeScript" />
    <img src="https://img.shields.io/badge/D3.js-7-F9A03C?logo=d3dotjs&logoColor=white" alt="D3.js" />
    <img src="https://img.shields.io/badge/tests-89%20passing-brightgreen" alt="Tests" />
  </p>
</p>

---

## Live Demo

> **Frontend:** https://crop-folio.vercel.app
> **Backend API:** https://cropfolio-production.up.railway.app
> **API Docs:** https://cropfolio-production.up.railway.app/docs (Swagger UI)

---

## The Problem

Myanmar's **10 million smallholder farmers** face a devastating reality:

```
                    70% of farmers grow RICE ONLY
                              |
                    One bad monsoon season
                              |
                 +-------------+-------------+
                 |                           |
            Drought                      Flooding
          (Dry Zone)                (Ayeyarwady Delta)
                 |                           |
          Crop failure                 Crop failure
                 |                           |
         TOTAL INCOME LOSS           TOTAL INCOME LOSS
```

- Farmers lose **20-40% of potential income** planting based on tradition, not data
- **Climate change** is making monsoons increasingly unpredictable
- **No tools exist** to help smallholders manage agricultural climate risk
- **Information asymmetry** between farmers and markets perpetuates poverty cycles

---

## The Solution

**CropFolio** applies **Modern Portfolio Theory** (Markowitz optimization) to crop selection — treating a farmer's land allocation like an investment portfolio.

> "What if farmers could manage climate risk the same way investors manage market risk?"

### The Core Insight — Validated by Real Data

We computed **actual yield correlations** from 12 years of FAOSTAT data (2010-2021, Myanmar, element 5419 yield hg/ha). The results contradicted our initial assumptions:

| Crop Pair         | Correlation      | What It Means                                               |
| ----------------- | ---------------- | ----------------------------------------------------------- |
| Rice vs Sesame    | **-0.49**        | Strong negative — the ONE real diversification hedge        |
| Rice vs Groundnut | **-0.05**        | Near zero — mild diversification benefit                    |
| Rice vs Chickpea  | **+0.13**        | Slightly positive — NOT a hedge as we originally assumed    |
| Pulses vs Pulses  | **+0.5 to +0.9** | Highly correlated — diversifying within pulses doesn't help |

The key finding: **only sesame genuinely hedges rice yield risk.** Diversifying among pulses alone provides almost no risk reduction because pulse yields move together. This is the kind of insight you can only get from real data — not from reasoning about drought/flood tolerance.

| Finance Concept        | CropFolio Equivalent                                  |
| ---------------------- | ----------------------------------------------------- |
| Stocks                 | Crops (rice, black gram, sesame, chickpea, groundnut) |
| Market Risk            | Climate Risk (drought, flood, temperature anomaly)    |
| Expected Returns       | Expected Income per Hectare                           |
| Correlation Matrix     | FAOSTAT 2010-2021 Yield Correlations (real data)      |
| Efficient Frontier     | Optimal Crop Mix for Risk/Return Tradeoff             |
| Monte Carlo Simulation | 1,000 Simulated Climate Seasons                       |

---

## How It Works

### 4-Step Wizard Flow

```mermaid
flowchart LR
    A["1. Select\nTownship"] --> B["2. Climate\nRisk Assessment"]
    B --> C["3. Portfolio\nOptimization"]
    C --> D["4. Monte Carlo\nSimulation"]

    style A fill:#f0fdf4,stroke:#16a34a,stroke-width:2px
    style B fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style C fill:#eff6ff,stroke:#3b82f6,stroke-width:2px
    style D fill:#fdf2f8,stroke:#ec4899,stroke-width:2px
```

#### Step 1: Select Township

Choose from **25 Myanmar agricultural townships** across 8 regions (Mandalay, Sagaing, Magway, Bago, Ayeyarwady, Yangon, Nay Pyi Taw, Shan). Select monsoon or dry season.

#### Step 2: Climate Risk Assessment

Real-time risk analysis using **NASA POWER** satellite data + **Open-Meteo** weather forecasts:

- Drought probability (%)
- Flood probability (%)
- Temperature anomaly vs. historical average
- Rainfall forecast vs. historical average
- Overall risk level (low / moderate / high / critical)

#### Step 3: Portfolio Optimization

**Markowitz mean-variance optimization** finds the crop allocation that maximizes expected income for a given level of risk:

- Select from 6 Myanmar crops with real agronomic profiles
- Adjust risk tolerance (conservative ↔ aggressive)
- See **monocrop vs. optimized** side-by-side with pie charts
- View metrics: expected income, Sharpe ratio, risk reduction %

#### Step 4: Monte Carlo Simulation

**1,000 simulated climate seasons** reveal the income distribution:

- Animated D3.js histogram (the demo "wow" moment)
- Monocrop (rice) overlay shows the wider, riskier spread
- Statistical summary: mean, median, 5th/95th percentile, VaR
- **Catastrophic loss probability** comparison (monocrop vs. diversified)

### Key Result

> **Diversification reduces catastrophic loss probability from ~40% to ~10%**
> That's a 75% reduction in the chance of financial ruin for a farming family.

---

## Architecture

```mermaid
graph TB
    subgraph Frontend["Frontend (React + TypeScript)"]
        UI["Wizard UI\n4 Steps"]
        Charts["Recharts\nPie Charts"]
        D3["D3.js\nMonte Carlo Histogram"]
    end

    subgraph Backend["Backend (FastAPI + Python)"]
        API["REST API\n10 Endpoints"]
        subgraph Domain["Domain Layer"]
            OPT["Markowitz\nOptimizer"]
            SIM["Monte Carlo\nSimulator"]
            CLM["Climate Risk\nEngine"]
        end
        subgraph Infra["Infrastructure"]
            NASA["NASA POWER\nClient"]
            METEO["Open-Meteo\nClient"]
        end
    end

    subgraph Data["External Data Sources"]
        NP["NASA POWER\nSatellite Climate"]
        OM["Open-Meteo\nWeather Forecast"]
        FAO["FAOSTAT\nCrop Yields 2010-2021"]
        WFP["WFP VAM\nFood Prices"]
    end

    UI --> API
    Charts --> API
    D3 --> API
    API --> OPT
    API --> SIM
    API --> CLM
    CLM --> NASA
    CLM --> METEO
    NASA --> NP
    METEO --> OM

    style Frontend fill:#f0fdf4,stroke:#16a34a
    style Backend fill:#eff6ff,stroke:#3b82f6
    style Data fill:#fef3c7,stroke:#d97706
```

### API Endpoints

| Method | Endpoint                             | Description                                |
| ------ | ------------------------------------ | ------------------------------------------ |
| `GET`  | `/api/v1/townships`                  | List 25 Myanmar townships with coordinates |
| `GET`  | `/api/v1/townships/{id}`             | Single township detail                     |
| `GET`  | `/api/v1/crops`                      | List 6 crop profiles with tolerance data   |
| `GET`  | `/api/v1/crops/{id}`                 | Single crop detail                         |
| `GET`  | `/api/v1/climate-risk/{township_id}` | Climate risk assessment (live + fallback)  |
| `POST` | `/api/v1/optimize`                   | Markowitz portfolio optimization           |
| `POST` | `/api/v1/simulate`                   | Monte Carlo simulation (histogram + stats) |
| `GET`  | `/api/v1/report/pdf`                 | Generate PDF report for portfolio          |
| `POST` | `/api/v1/report/analyze`             | AI-powered portfolio analysis (Gemini)     |
| `POST` | `/api/v1/compare`                    | Multi-township portfolio comparison        |

Full interactive API docs available at `/docs` (Swagger UI).

### Routes

| Route    | Description                                                        |
| -------- | ------------------------------------------------------------------ |
| `/`      | Landing page with animated hero and scroll-driven story            |
| `/app`   | 4-step portfolio wizard (township → climate → optimize → simulate) |
| `/admin` | Mock admin dashboard (login: admin / 12345)                        |

---

## The 6 Myanmar Crops

| Crop         | Burmese   | Category | Drought              | Flood          | Season  |
| ------------ | --------- | -------- | -------------------- | -------------- | ------- |
| Rice (Paddy) | စပါး      | Cereal   | Low (0.3)            | **High (0.7)** | Monsoon |
| Black Gram   | မတ်ပဲ     | Pulse    | **High (0.7)**       | Low (0.2)      | Dry     |
| Green Gram   | ပဲတီစိမ်း | Pulse    | **High (0.65)**      | Low (0.25)     | Dry     |
| Chickpea     | ကုလားပဲ   | Pulse    | **Very High (0.85)** | Very Low (0.1) | Dry     |
| Sesame       | နှမ်း     | Oilseed  | **Very High (0.8)**  | Very Low (0.1) | Dry     |
| Groundnut    | မြေပဲ     | Oilseed  | Moderate (0.55)      | Low (0.2)      | Dry     |

Sources: FAOSTAT 2010-2021 (yield means + variance), FAO GAEZ, IRRI, Myanmar Department of Agriculture

---

## Tech Stack

| Layer             | Technology                            | Why                                             |
| ----------------- | ------------------------------------- | ----------------------------------------------- |
| **Backend**       | Python 3.10, FastAPI                  | Best ecosystem for scientific computing + API   |
| **Optimization**  | scipy.optimize (SLSQP)                | Markowitz mean-variance optimization            |
| **Simulation**    | numpy                                 | Monte Carlo with multivariate normal sampling   |
| **Frontend**      | React 18, TypeScript (strict)         | Component-driven, type-safe UI                  |
| **AI/ML**         | Google Gemini 2.0 Flash               | AI-powered analysis and recommendations         |
| **Visualization** | D3.js + Recharts                      | Custom animated histogram + standard charts     |
| **Styling**       | Tailwind CSS v4                       | Utility-first, rapid prototyping                |
| **Data**          | NASA POWER, Open-Meteo, FAOSTAT, WFP  | All open, all verified for Myanmar coverage     |
| **Deployment**    | Railway (backend) + Vercel (frontend) | Zero-config, instant deploys                    |
| **Testing**       | pytest (83 tests), vitest (6 tests)   | 89 total tests, 80%+ coverage on critical paths |

---

## Data Sources

| Source                                     | What It Provides                    | Myanmar Coverage               |
| ------------------------------------------ | ----------------------------------- | ------------------------------ |
| [NASA POWER](https://power.larc.nasa.gov/) | Historical climate data (10+ years) | Global, 0.5 degree resolution  |
| [Open-Meteo](https://open-meteo.com/)      | Weather forecasts (7-16 days)       | Global, 11km resolution        |
| [FAOSTAT](https://data.un.org/)            | Historical crop yields (2010-2021)  | Myanmar, 5 crops, annual       |
| [FAO GAEZ](https://gaez.fao.org/)          | Crop yield potential by region      | Global, gridded                |
| [WFP VAM](https://dataviz.vam.wfp.org/)    | Food commodity prices               | Myanmar, 70+ townships, weekly |

FAOSTAT data (element code 5419 — yield hg/ha, country code 28 — Myanmar) provides the **real yield covariance matrix** behind the portfolio optimizer. 12 annual observations (2010-2021) for Rice, Groundnut, Sesame, Chickpea, and Beans dry (proxy for Black Gram + Green Gram). WFP price data (2022-2025, monthly) provides the **price correlation matrix** for all 6 crops. The optimizer uses a dual revenue covariance matrix (0.6 yield + 0.4 price) — because yield hedging (rice-sesame = -0.49) is partially offset by price co-movement (rice-sesame = +0.74).

All data sources are **open access** with confirmed Myanmar coverage. Climate data includes graceful fallback to regional averages when external APIs are unavailable.

---

## Business Model

```mermaid
timeline
    title CropFolio Growth Strategy
    section Phase 1 (0-12 months)
        Free for NGOs and cooperatives : Build data moat
        : Prove accuracy with real outcomes
        : Onboard 50+ extension workers
    section Phase 2 (12-24 months)
        License risk engine to crop insurers : Parametric insurance pricing
        : Agricultural credit risk scoring
        : Microfinance integration
    section Phase 3 (24+ months)
        Commodity supply intelligence : Production forecasting
        : Trade flow prediction
        : Scale beyond Myanmar
```

| Market                 | Size                             | Our Position                 |
| ---------------------- | -------------------------------- | ---------------------------- |
| Myanmar agri-insurance | Growing (UNDP/ADB-funded pilots) | Risk engine provider         |
| Myanmar microfinance   | ~$2B outstanding loans           | Agricultural credit scoring  |
| Global crop insurance  | **$40B+/year**                   | Climate-adjusted risk models |

---

## Target Users

```mermaid
graph TD
    A["Agricultural Extension Workers"] -->|"Advise farmer groups\non optimal crop allocation"| F["500+ Farmers\nper Extension Worker"]
    B["Agri-Cooperative Managers"] -->|"Plan collective planting\nacross member farms"| F
    C["NGO Program Officers"] -->|"Design climate-resilient\nagriculture programs"| F
    D["Microfinance Loan Officers"] -->|"Assess agricultural\ncredit risk"| F

    style A fill:#dcfce7,stroke:#16a34a
    style B fill:#dbeafe,stroke:#3b82f6
    style C fill:#fef3c7,stroke:#d97706
    style D fill:#fdf2f8,stroke:#ec4899
    style F fill:#f1f5f9,stroke:#64748b
```

We target **intermediaries**, not individual farmers. Extension workers and cooperatives have the reach, digital literacy, and mandate to act on portfolio recommendations.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 20+

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
# API running at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# App running at http://localhost:5173
```

### Run Tests

```bash
# Backend (83 tests)
cd backend && pytest -v

# Frontend
cd frontend && npm run test
```

---

## Project Structure

```
cropfolio/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── routes/          # Route handlers (thin)
│   │   │   └── schemas/         # Pydantic request/response models
│   │   ├── core/                # Config, constants
│   │   ├── domain/              # Pure business logic
│   │   │   ├── climate.py       # Climate risk engine
│   │   │   ├── optimizer.py     # Markowitz portfolio optimizer
│   │   │   ├── simulator.py     # Monte Carlo simulation
│   │   │   └── crops.py         # 6 Myanmar crop profiles
│   │   ├── infrastructure/      # External API clients
│   │   │   ├── nasa_power.py    # NASA POWER satellite data
│   │   │   └── open_meteo.py    # Open-Meteo weather forecasts
│   │   └── services/            # Orchestration layer
│   ├── data/                    # Static data (townships, prices)
│   ├── tests/                   # 83 tests (unit + integration)
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/                 # Typed API client layer
│   │   ├── components/
│   │   │   ├── township/        # Step 1: Township selector
│   │   │   ├── climate/         # Step 2: Risk dashboard
│   │   │   ├── optimizer/       # Step 3: Portfolio optimizer
│   │   │   ├── simulator/       # Step 4: Monte Carlo viz
│   │   │   ├── common/          # Shared UI components
│   │   │   └── layout/          # App shell, header
│   │   ├── hooks/               # 5 custom data hooks
│   │   ├── types/               # TypeScript interfaces
│   │   ├── constants/           # Named constants (no magic numbers)
│   │   └── utils/               # Formatters, color maps
│   └── vercel.json
├── docs/
│   └── PRD.md                   # Product Requirements Document
├── PITCH.md                     # Hackathon pitch outline
└── README.md
```

---

## The Math Behind CropFolio

### Markowitz Mean-Variance Optimization

For `n` crops with expected returns vector `r` and covariance matrix `Sigma`:

```
Minimize:    w^T * Sigma * w          (portfolio variance)
Subject to:  w^T * r >= R_target      (minimum return)
             sum(w) = 1               (fully invested)
             w_i >= 0                 (no short selling)
```

Solved using **Sequential Least Squares Programming** (SLSQP) via `scipy.optimize.minimize`.

### Climate-Adjusted Returns

Expected income is adjusted for climate risk:

```
adjusted_income = base_income * (1 - drought_prob * (1 - drought_tolerance)
                                  - flood_prob * (1 - flood_tolerance))
```

### Monte Carlo Simulation

Income scenarios sampled from multivariate normal distribution:

```
scenarios ~ N(expected_returns, covariance_matrix)
portfolio_income = scenarios @ weights
```

1,000 scenarios generate the income distribution, from which we compute VaR, catastrophic loss probability, and percentile ranges.

**Why is it fast?** Monte Carlo simulation completes in ~50ms because sampling 1,000 scenarios from a 6-crop multivariate normal distribution is a single `(1000, 6)` matrix operation — trivial for numpy. This is not machine learning. There are no training loops, no gradient descent, no parameter optimization across epochs. The computational value is in the **statistical insight** (stress-testing portfolios across 1,000 climate scenarios), not in compute time. The Markowitz optimizer (scipy SLSQP) also converges in milliseconds because it's a convex optimization with 6 variables — not a neural network with millions of parameters.

---

## Testing

```
89 tests | 0 failures (83 backend + 6 frontend)

Unit Tests (32):
  - Climate risk engine: 8 tests
  - Portfolio optimizer: 12 tests (weights sum to 1, PSD correction, convergence check, risk reduction > 0)
  - Monte Carlo simulator: 8 tests (reproducible, bounded, convergent)
  - Diversification proof: monocrop vs diversified catastrophic loss

Integration Tests (31):
  - All 10 API endpoints tested
  - Error handling: 400, 404, 422 responses
  - External API fallback behavior
  - Schema validation

Data Pipeline Tests (9):
  - NASA POWER mm/day to mm/month conversion
  - Open-Meteo seasonal scaling
  - WFP price data loading and validation

AI & Comparison Tests (11):
  - Gemini AI analysis endpoint
  - Multi-township comparison endpoint
  - AI-enhanced PDF report generation

Frontend Tests (6):
  - Component rendering tests
  - Hook tests
```

---

## AI Features

CropFolio integrates **Google Gemini 2.0 Flash** (free tier) for intelligent analysis:

- **AI Analysis Button** — one-click AI-powered portfolio recommendations with actionable insights tailored to the selected township and climate conditions
- **AI-Enhanced PDF Reports** — generated reports include Gemini-powered narrative analysis alongside the standard portfolio metrics
- **Multi-Township Comparison** — compare optimized portfolios across multiple townships side-by-side to identify regional patterns

AI features are **optional** — the app works fully without a Gemini API key. When available, AI adds a layer of contextual interpretation on top of the mathematical optimization.

---

## What Makes This Different

| Other Hackathon Projects      | CropFolio                                                                    |
| ----------------------------- | ---------------------------------------------------------------------------- |
| Crop disease image classifier | **Cross-domain insight**: finance theory applied to agriculture              |
| Weather dashboard             | **Actionable optimization**: not just data, but decisions                    |
| Chatbot for farmers           | **Mathematical proof**: Monte Carlo shows WHY diversification works          |
| Price prediction app          | **Compound value**: climate + market + risk in one model                     |
| Projects with heuristic data  | **Data-driven correlations**: real FAOSTAT 2010-2021 covariance, not assumed |

---

## Limitations (Honest)

This is a proof of concept. Here's what's real and what's not:

| What                            | Status                                                                         |
| ------------------------------- | ------------------------------------------------------------------------------ |
| The Markowitz optimization math | Real and correct (PSD correction + convergence check added)                    |
| The Monte Carlo simulation      | Real and correct                                                               |
| The crop risk profiles          | Cited — yields updated to 2019-2021 FAOSTAT means, variance from FAOSTAT CV    |
| The covariance matrix           | **Real** — computed from FAOSTAT 2010-2021 yield data (12 annual observations) |
| The climate data pipeline       | Working — NASA POWER mm/day→mm/month fixed, Open-Meteo seasonal scaling fixed  |
| WFP price data                  | Real — 6 WFP price CSVs loaded for Myanmar crops                               |
| WFP price correlations          | **Real** — computed from WFP monthly prices (2022-2025), all 6 crops           |
| Revenue covariance matrix       | **Real** — dual yield (0.6) + price (0.4) weighted covariance                  |
| The Burmese translations        | AI-generated, not reviewed by a native speaker                                 |
| The business model              | Speculative — zero customer validation                                         |
| AI features                     | Optional — require GEMINI_API_KEY (free tier). App works fully without it      |
| **Post-2021 economic crisis**   | **NOT modeled** — see below                                                    |

### What We Don't Model (Post-2021 Myanmar)

CropFolio optimizes for **climate risk**. It does NOT model the political and economic disruptions following Myanmar's 2021 military coup:

- **Currency devaluation** (~60% MMK decline) — our prices are in nominal MMK
- **Supply chain collapse** — fertilizer, fuel, transport disruptions
- **Banking system failure** — farmers can't access credit for inputs
- **Conflict zones** — some townships have active fighting during planting season
- **Export restrictions** — government controls on pulse/sesame trade
- **Input cost inflation** — fertilizer and fuel costs have tripled

The FAOSTAT yield data (2010-2021) is essentially pre-coup. The yield correlations remain physically valid (drought still affects rice more than sesame), but the economic context has fundamentally changed. Income projections should be treated as directional, not precise.

**What needs to happen for production:** Native Burmese speaker review. User testing with actual extension workers. Customer interviews with insurers/cooperatives.

The core insight — that sesame is the one genuine hedge against rice yield risk (r = -0.49) — is now backed by real FAOSTAT data. The architecture supports iterating toward production quality. The bones are good.

---

## License

MIT

---

<p align="center">
  Built for the <strong>AI for Climate-Resilient Agriculture Hackathon 2026</strong><br/>
  Impact Hub Yangon x UNDP Myanmar
</p>
