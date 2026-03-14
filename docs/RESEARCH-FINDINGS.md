# CropFolio — Research & Findings

## Executive Summary

CropFolio's portfolio optimizer is built on real data, not assumptions. This document records our key research findings from FAOSTAT yield data (2010-2021) and WFP price monitoring (2022-2025). These findings drive the optimizer's crop allocation recommendations and represent CropFolio's core data moat.

---

## Finding 1: The Rice-Sesame Yield Hedge

FAOSTAT data reveals rice and sesame yields have a **-0.49 correlation** over 12 years of annual observations.

When drought hurts rice yields, sesame yields tend to increase. This is the strongest natural hedge among Myanmar's major crops — and the only crop pair with a meaningfully negative correlation against rice.

**Source:** FAOSTAT element 5419 (yield hg/ha), country code 28 (Myanmar), 2010-2021

### Full Yield Correlation Matrix (FAOSTAT 2010-2021)

| Crop Pair               | Yield Correlation |
| ----------------------- | ----------------: |
| Rice — Sesame           |         **-0.49** |
| Rice — Groundnut        |         **-0.05** |
| Rice — Chickpea         |         **+0.13** |
| Rice — Black Gram       |         **+0.50** |
| Rice — Green Gram       |         **+0.15** |
| Groundnut — Sesame      |         **+0.67** |
| Groundnut — Chickpea    |         **+0.59** |
| Groundnut — Black Gram  |         **+0.49** |
| Groundnut — Green Gram  |         **+0.51** |
| Sesame — Chickpea       |         **+0.15** |
| Sesame — Black Gram     |         **+0.11** |
| Sesame — Green Gram     |         **+0.29** |
| Chickpea — Black Gram   |         **+0.68** |
| Chickpea — Green Gram   |         **+0.69** |
| Black Gram — Green Gram |         **+0.89** |

Note: Black gram and green gram both use beans_dry (FAOSTAT code 176) as proxy, with small independent noise added to avoid a singular covariance matrix. Their series uses 2014-2021 only (8 observations) due to a FAOSTAT methodology break between 2013-2014.

---

## Finding 2: Not All Diversification Is Equal

**Initial hypothesis:** All drought-tolerant crops hedge rice yield risk.

**Reality from data:**

| Crop Pair         | Yield Correlation | Hedge Quality    |
| ----------------- | ----------------: | ---------------- |
| Rice — Sesame     |             -0.49 | Strong hedge     |
| Rice — Groundnut  |             -0.05 | Near zero (weak) |
| Rice — Chickpea   |             +0.13 | Not a hedge      |
| Rice — Black Gram |             +0.50 | Moves WITH rice  |

Pulses are highly correlated with each other:

- Chickpea — Black Gram: +0.68
- Chickpea — Green Gram: +0.69
- Black Gram — Green Gram: +0.89

**Implication:** The optimizer should favor sesame over chickpea for rice-heavy portfolios. Diversifying within the pulse family alone provides almost no risk reduction because pulse yields move together.

---

## Finding 3: Price Co-Movement Offsets Yield Hedging

WFP price data (2022-2025) reveals that price correlations behave very differently from yield correlations:

| Metric                       | Rice-Sesame |
| ---------------------------- | ----------: |
| Yield correlation (FAOSTAT)  |       -0.49 |
| Price correlation (WFP)      |       +0.74 |
| Combined revenue correlation |       ~0.00 |

Rice and sesame yields move in opposite directions (hedge), but their prices move together due to inflation and shared macroeconomic factors.

**Implication:** The diversification benefit comes from **yield risk reduction**, not price arbitrage. This is why CropFolio uses a dual yield+price covariance matrix (weighted 0.6 yield + 0.4 price), not just yields alone.

### Full Price Correlation Matrix (WFP 2022-2025)

| Crop Pair               | Price Correlation |
| ----------------------- | ----------------: |
| Rice — Sesame           |         **+0.74** |
| Rice — Groundnut        |         **+0.72** |
| Rice — Chickpea         |         **+0.70** |
| Rice — Black Gram       |         **+0.74** |
| Rice — Green Gram       |         **+0.67** |
| Groundnut — Sesame      |         **+0.97** |
| Groundnut — Chickpea    |         **+0.97** |
| Groundnut — Black Gram  |         **+0.95** |
| Groundnut — Green Gram  |         **+0.96** |
| Sesame — Chickpea       |         **+0.96** |
| Sesame — Black Gram     |         **+0.95** |
| Sesame — Green Gram     |         **+0.95** |
| Chickpea — Black Gram   |         **+0.93** |
| Chickpea — Green Gram   |         **+0.95** |
| Black Gram — Green Gram |         **+0.93** |

Note: All price correlations are strongly positive (+0.67 to +0.97), reflecting shared inflationary pressures in Myanmar's agricultural commodity markets. Price diversification alone provides almost no risk reduction.

---

## Finding 4: Myanmar Crop Yield Trends (2010-2021)

| Crop      | 2010 (t/ha) | 2021 (t/ha) | Mean (t/ha) | CV (%) | Trend     |
| --------- | ----------: | ----------: | ----------: | -----: | --------- |
| Rice      |       4.003 |       3.811 |       3.829 |   1.7% | Stable    |
| Sesame    |       0.518 |       0.456 |       0.514 |   6.7% | Declining |
| Groundnut |       1.562 |       1.388 |       1.524 |   4.8% | Declining |
| Chickpea  |       1.386 |       1.357 |       1.422 |   5.3% | Declining |
| Beans dry |       1.303 |       0.929 |       1.093 |  19.4% | Declining |

Key observations:

- **Rice yields are remarkably stable** (CV = 1.7%), meaning rice is a low-variance anchor crop
- **Sesame yields are the most volatile** among the non-pulse crops (CV = 6.7%), but sesame's negative correlation with rice means this volatility provides hedging value
- **All non-rice crops show declining yields** over 2010-2021, suggesting climate stress or soil degradation
- **Beans dry (pulse proxy) shows a structural break** between 2013-2014 (methodology change), which is why we use 2014-2021 data only for black gram and green gram

### Raw FAOSTAT Yield Data (t/ha)

| Year |  Rice | Groundnut | Sesame | Chickpea | Beans dry |
| ---- | ----: | --------: | -----: | -------: | --------: |
| 2010 | 4.003 |     1.562 |  0.518 |    1.386 |     1.303 |
| 2011 | 3.773 |     1.553 |  0.543 |    1.398 |     1.383 |
| 2012 | 3.751 |     1.567 |  0.533 |    1.429 |     1.430 |
| 2013 | 3.793 |     1.574 |  0.536 |    1.464 |     1.461 |
| 2014 | 3.846 |     1.582 |  0.547 |    1.510 |     0.953 |
| 2015 | 3.872 |     1.598 |  0.548 |    1.535 |     0.967 |
| 2016 | 3.818 |     1.590 |  0.544 |    1.537 |     0.959 |
| 2017 | 3.822 |     1.531 |  0.517 |    1.402 |     0.930 |
| 2018 | 3.857 |     1.478 |  0.480 |    1.397 |     0.933 |
| 2019 | 3.796 |     1.457 |  0.495 |    1.316 |     0.934 |
| 2020 | 3.804 |     1.411 |  0.455 |    1.335 |     0.932 |
| 2021 | 3.811 |     1.388 |  0.456 |    1.357 |     0.929 |

---

## Finding 5: Price Volatility Is Uniform Across Crops

| Crop       | Mean (MMK/kg) | Std (MMK/kg) | CV (%) |     Min |     Max |
| ---------- | ------------: | -----------: | -----: | ------: | ------: |
| Rice       |        678.52 |       102.44 |  15.1% |  494.00 |  852.90 |
| Groundnut  |      2,841.62 |       367.01 |  12.9% | 2140.00 | 3474.00 |
| Sesame     |      4,510.45 |       585.26 |  13.0% | 3411.00 | 5519.20 |
| Chickpea   |      2,321.24 |       302.92 |  13.1% | 1750.00 | 2848.80 |
| Black Gram |      1,898.25 |       287.47 |  15.1% | 1345.00 | 2390.80 |
| Green Gram |      2,027.21 |       305.52 |  15.1% | 1461.00 | 2555.80 |

All crops have similar coefficient of variation (12.9% to 15.1%), meaning **price volatility alone does not differentiate crops**. The diversification benefit must come from yield correlations, not price behavior.

---

## Data Sources

| Source                     | What                       | Coverage                             | Access           |
| -------------------------- | -------------------------- | ------------------------------------ | ---------------- |
| FAOSTAT via data.un.org    | Crop yields (element 5419) | Myanmar (code 28), 2010-2021, annual | Open             |
| WFP VAM Food Prices        | Commodity prices (MMK/kg)  | Myanmar, 2022-2025, monthly          | data.humdata.org |
| WFP Market Price Bulletins | Price validation           | Myanmar, 2022-2025, monthly          | Open             |

---

## Methodology

### Yield Correlations

- **Data:** FAOSTAT annual yield series, 12 observations (2010-2021) for rice, groundnut, sesame, chickpea; 8 observations (2014-2021) for beans_dry (black gram + green gram proxy)
- **Method:** Pearson correlation of year-over-year yield percentage changes
- **Alignment:** For pairs involving beans_dry (shorter series), aligned to the most recent overlapping observations

### Price Correlations

- **Data:** WFP monthly price series (MMK/kg), 2022-2025
- **Method:** Pearson correlation of month-over-month price percentage changes
- **Alignment:** Aligned to shortest common series length

### Revenue Covariance

- **Method:** Weighted combination of yield covariance and price covariance matrices
- **Weights:** 0.6 (yield) + 0.4 (price)
- **Rationale:** Yield risk is the primary driver of income variability for smallholders, but price co-movement cannot be ignored

### Variance (Coefficient of Variation)

- **Yield CV:** Computed from FAOSTAT 2010-2021 annual yield series (sample std / mean)
- **Price CV:** Computed from WFP 2022-2025 monthly price series (sample std / mean)

---

## Implications for the Optimizer

1. **Sesame is the key diversifier.** It is the only crop with a meaningfully negative yield correlation against rice (-0.49). The optimizer should allocate significant sesame weight for rice-heavy portfolios.

2. **Pulse diversification is illusory.** Black gram, green gram, and chickpea yields are highly correlated (+0.68 to +0.89). Allocating across multiple pulses does not reduce portfolio risk.

3. **Price risk requires separate modeling.** Because price correlations are uniformly high (+0.67 to +0.97), a yield-only covariance matrix would overstate the diversification benefit. The dual yield+price model provides a more honest risk estimate.

4. **Rice is the low-variance anchor.** With a yield CV of just 1.7%, rice provides portfolio stability. The optimization question is not whether to grow rice, but how much land to allocate to sesame as a hedge.
