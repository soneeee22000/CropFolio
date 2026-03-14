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

Key insight: We didn't just assume correlations — we **computed them from 12 years of FAOSTAT data**. And the data surprised us:

- Rice vs Sesame: **-0.49** — the one genuine diversification hedge
- Rice vs Chickpea: **+0.13** — NOT a hedge (we originally assumed it was)
- Pulses vs Pulses: **+0.5 to +0.9** — diversifying within pulses doesn't help

"We went in assuming all pulses hedge rice. The data told us only sesame does. That's why you need real correlations, not intuition."

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
- **Real data** — FAOSTAT 2010-2021 yield correlations + WFP 2022-2025 price correlations + NASA POWER climate data
- **Revenue covariance** — yield hedging (rice-sesame = -0.49) is offset by price co-movement (+0.74), giving near-zero revenue correlation. Our dual model captures both dimensions
- **Free for cooperatives** — no cost barrier for the people who need it most

## 5. Tech (30s)

- **Backend:** Python, FastAPI, scipy (Markowitz optimization), numpy (Monte Carlo)
- **AI:** Google Gemini 2.0 Flash — intelligent portfolio analysis and recommendations
- **Frontend:** React, TypeScript, D3.js (animated histogram)
- **Data:** FAOSTAT 2010-2021 (covariance matrix), NASA POWER API, Open-Meteo API, WFP food prices
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
- When judges ask "is the data real?" → "The covariance matrix is computed from 12 years of FAOSTAT yield data — real Myanmar crop yields from 2010 to 2021. Crop yield means are 2019-2021 FAOSTAT averages. Price correlations computed from WFP monthly data 2022-2025. Climate from NASA POWER. Both yield AND price risk are data-driven."
- When judges ask "where's the historical data?" → This is now a STRENGTH: "We downloaded FAOSTAT yield data for Myanmar, element 5419, 12 annual observations. We computed the actual correlation matrix. The data surprised us — only sesame genuinely hedges rice risk. Pulse-pulse correlations are too high for within-pulse diversification to help."
- Don't claim 90% confidence — if asked about data quality, be honest about limitations
- Don't bluff. Honesty about what's real and what's next is more credible than pretending it's finished.
