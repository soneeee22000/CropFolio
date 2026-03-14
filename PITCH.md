# CropFolio — Pitch Outline (3-5 minutes)

## 1. Problem (30s)

Myanmar's 10 million smallholder farmers face a devastating reality:

- 70% grow rice as a monocrop — one bad monsoon means financial ruin
- Climate change is making monsoons unpredictable — droughts in the dry zone, flooding in the delta
- Farmers lose 20-40% of potential income because they plant based on tradition, not data
- No tools exist to help farmers manage climate risk through diversification

**Hook:** "What if farmers could manage climate risk the same way investors manage market risk?"

## 2. Solution (45s)

**CropFolio** applies Modern Portfolio Theory (Markowitz optimization) to crop selection.

Just like an investor diversifies stocks to reduce portfolio risk, CropFolio diversifies crops to reduce climate risk.

Key insight: Rice is flood-tolerant but drought-sensitive. Pulses and oilseeds are drought-tolerant but flood-sensitive. These **negatively correlated risk profiles** are exactly what portfolio theory exploits.

**Target users:** Agricultural extension workers, agri-cooperatives, NGO program officers — not individual farmers directly.

## 3. Live Demo (90s)

Start on the **landing page** (/) — show the animated 40% → 10% hero stat. Click "Try CropFolio" to enter the wizard.

Walk through the 4 steps:

1. **Select Township** — pick Magway (dry zone, high drought risk)
2. **Climate Risk** — show 95% drought probability, critical risk level
3. **Optimize** — select Rice + Black Gram + Sesame → show 51% risk reduction
4. **Monte Carlo** — run 1,000 simulations → show the histogram

**Demo highlight:** Point to the monocrop red spike near zero income vs. the diversified green distribution. "40% catastrophic loss probability drops to 10%. That's the power of diversification."

Toggle to Burmese to show localization. Click the **AI Analysis** button to show Gemini-powered recommendations. Download the AI-enhanced PDF report.

Optionally show the **admin dashboard** (/admin, login: admin / 12345) to demonstrate the B2B platform vision. Show the **multi-township comparison** to demonstrate regional planning capability.

## 4. Impact (30s)

- **40-60% risk reduction** through crop diversification
- **Printable reports** for cooperatives without internet access
- **Burmese language** for actual Myanmar users
- **Real data** — NASA POWER climate data (mm/day→mm/month fixed) + 6 WFP price CSVs + cited crop profiles
- **Free for cooperatives** — no cost barrier for the people who need it most

## 5. Tech (30s)

- **Backend:** Python, FastAPI, scipy (Markowitz optimization), numpy (Monte Carlo)
- **AI:** Google Gemini 2.0 Flash — intelligent portfolio analysis and recommendations
- **Frontend:** React, TypeScript, D3.js (animated histogram)
- **Data:** NASA POWER API, Open-Meteo API, FAO GAEZ, WFP food prices
- **AI costs:** Zero — Gemini free tier. Core math runs without AI; AI adds contextual analysis
- **89 automated tests** (83 backend + 6 frontend) — production-grade engineering

## 6. Business Model (30s)

| Phase             | Model                                                        |
| ----------------- | ------------------------------------------------------------ |
| Phase 1 (0-12mo)  | Free for NGOs/cooperatives — build data moat, prove accuracy |
| Phase 2 (12-24mo) | License risk engine to parametric crop insurers              |
| Phase 3 (24mo+)   | Commodity supply intelligence for traders                    |

TAM: Global crop insurance market = $40B+/year

## 7. Ask (15s)

- Scale to all 330 Myanmar townships with localized data
- Partner with UNDP/FAO for distribution through existing extension networks
- 3-month incubation to build the B2B insurance risk engine

---

## Pitch Tips

- Open the app 2 minutes before the pitch to warm up the server
- Have the Magway township pre-searched in the search box
- Always use rice + black gram + sesame (tested safe combination)
- Practice the Monte Carlo reveal — pause when the histogram animates
- When judges ask "can farmers use this?" → "Extension workers and cooperatives are our users. They advise 500+ farmers each."
- When judges ask "is the data real?" → "Crop profiles are cited from FAO/IRRI. Climate uses NASA POWER with correct mm/day→mm/month conversion. WFP price data for all 6 crops. The covariance model is heuristic — our next phase is integrating actual historical time series."
- When judges ask "where's the historical data?" → Own it: "This is a proof of concept. The optimization math is correct. The inputs use heuristic correlations based on agronomic research. Phase 2 is real data integration."
- Don't claim 90% confidence — if asked about data quality, be honest about limitations
- Don't bluff. Honesty about what's real and what's next is more credible than pretending it's finished.
