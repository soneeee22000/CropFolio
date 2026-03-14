# CropFolio

**Portfolio Theory for Climate-Resilient Farming in Myanmar**

CropFolio applies Modern Portfolio Theory (Markowitz optimization) to crop selection — treating a farmer's land allocation like an investment portfolio. It optimizes crop mix to maximize expected income while minimizing climate risk.

## The Problem

Myanmar smallholder farmers lose 20-40% of potential income because they concentrate on a single crop (rice), plant based on tradition instead of climate data, and sell at harvest when prices are lowest.

## The Insight

Rice is flood-tolerant but drought-sensitive. Pulses and oilseeds are drought-tolerant but flood-sensitive. These **negatively correlated risk profiles** create a natural diversification opportunity — the same principle that drives investment portfolio optimization.

## Features

- **Climate Risk Dashboard** — Township-level drought/flood probability using NASA POWER + Open-Meteo data
- **Portfolio Optimizer** — AI-optimized crop allocation that maximizes income while minimizing climate risk
- **Monte Carlo Simulator** — Visualize 1,000 simulated seasons to demonstrate diversification benefits
- **Crop Comparison** — Side-by-side crop profiles with yield, price trends, and climate sensitivity
- **Burmese Reports** — Exportable, jargon-free recommendations for farmer communities

## Tech Stack

| Layer           | Technology                                          |
| --------------- | --------------------------------------------------- |
| Backend         | Python 3.12, FastAPI                                |
| ML/Optimization | scipy, numpy, pandas, scikit-learn                  |
| Frontend        | React 18, TypeScript, Tailwind CSS, Recharts, D3.js |
| Data Sources    | NASA POWER, Open-Meteo, FAO GAEZ, WFP               |
| Deployment      | Vercel + Railway                                    |

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- npm 10+

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### Docker (Full Stack)

```bash
docker-compose up --build
```

Open http://localhost:5173 in your browser.

## Data Sources

| Source                                     | What It Provides                         | Coverage                |
| ------------------------------------------ | ---------------------------------------- | ----------------------- |
| [NASA POWER](https://power.larc.nasa.gov/) | Historical climate data, solar radiation | Global, 0.5° resolution |
| [Open-Meteo](https://open-meteo.com/)      | Weather forecasts (7-16 days)            | Global, 11km resolution |
| [FAO GAEZ](https://gaez.fao.org/)          | Crop yield potential by region           | Global, gridded         |
| [WFP VAM](https://dataviz.vam.wfp.org/)    | Food commodity prices                    | Myanmar, 70+ townships  |

## Target Users

- Agricultural extension workers
- Agri-cooperative managers
- NGO program officers
- Microfinance loan officers

## License

MIT

---

Built for the **AI for Climate-Resilient Agriculture Hackathon 2026** (Impact Hub Yangon x UNDP Myanmar)
