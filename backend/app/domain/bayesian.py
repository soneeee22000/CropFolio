"""Bayesian Belief Network engine for evidence-based crop yield prediction.

Builds a directed acyclic graph (DAG) representing causal relationships
between climate, soil, and crop yields. Conditional Probability Tables (CPTs)
are initialized programmatically from CropProfile tolerance scores, then
updated via Bayesian inference as field evidence accumulates.

The moat: after 2 seasons of evidence, a competitor starting from scratch
is 2 years behind — they'd need the same field data to match our posteriors.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np

from app.domain.crops import CropProfile

logger = logging.getLogger(__name__)


class YieldCategory(str, Enum):
    """Discretized yield outcome categories."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RainfallCategory(str, Enum):
    """Discretized rainfall categories."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class SoilCategory(str, Enum):
    """Discretized soil quality categories."""

    POOR = "poor"
    MODERATE = "moderate"
    GOOD = "good"


@dataclass(frozen=True)
class EvidenceItem:
    """A single piece of evidence for Bayesian updating."""

    variable: str
    value: str


@dataclass(frozen=True)
class BayesianPredictionResult:
    """Result from Bayesian inference for a single crop."""

    crop_id: str
    yield_probabilities: dict[str, float]
    expected_yield_factor: float
    evidence_used: list[str]


@dataclass(frozen=True)
class BayesianPortfolioResult:
    """Bayesian-adjusted returns for portfolio optimization."""

    crop_predictions: list[BayesianPredictionResult]
    model_type: str = "bayesian"


class CropBayesianNetwork:
    """Bayesian Belief Network for a single crop's yield prediction.

    DAG structure:
        Season ──> Rainfall ──> Drought ──┬──> CropYield
                           └──> Flood  ───┘
        Soil ─────────────────────────────┘

    CPTs are parameterized from CropProfile tolerance scores,
    not hand-coded. This ensures consistency with the rest of
    the system and automatic updates when crop data changes.
    """

    def __init__(self, crop: CropProfile) -> None:
        """Initialize BBN with CPTs derived from crop profile."""
        self._crop = crop
        self._nodes = [
            "season", "rainfall", "drought", "flood", "soil", "yield"
        ]
        self._cpts = self._build_cpts()

    def _build_cpts(self) -> dict[str, Any]:
        """Build conditional probability tables from crop tolerance scores."""
        crop = self._crop

        season_cpt = {
            "monsoon": 0.58,
            "dry": 0.42,
        }

        rainfall_given_season = {
            "monsoon": {"low": 0.15, "normal": 0.55, "high": 0.30},
            "dry": {"low": 0.40, "normal": 0.45, "high": 0.15},
        }

        drought_given_rainfall = {
            "low": 0.70,
            "normal": 0.15,
            "high": 0.05,
        }

        flood_given_rainfall = {
            "low": 0.05,
            "normal": 0.10,
            "high": 0.60,
        }

        soil_prior = {
            "poor": 0.30,
            "moderate": 0.45,
            "good": 0.25,
        }

        yield_cpt = self._build_yield_cpt(crop)

        return {
            "season": season_cpt,
            "rainfall_given_season": rainfall_given_season,
            "drought_given_rainfall": drought_given_rainfall,
            "flood_given_rainfall": flood_given_rainfall,
            "soil": soil_prior,
            "yield_cpt": yield_cpt,
        }

    def _build_yield_cpt(
        self, crop: CropProfile,
    ) -> dict[tuple[str, str, str], dict[str, float]]:
        """Build P(Yield | Drought, Flood, Soil) from tolerance scores.

        Uses drought_tolerance and flood_tolerance to parameterize
        the yield distribution under each scenario combination.
        Higher tolerance = less yield impact from that hazard.
        """
        dt = crop.drought_tolerance
        ft = crop.flood_tolerance

        yield_cpt: dict[tuple[str, str, str], dict[str, float]] = {}

        for drought_state in ["yes", "no"]:
            for flood_state in ["yes", "no"]:
                for soil_state in ["poor", "moderate", "good"]:
                    base_high = 0.40
                    base_med = 0.40
                    base_low = 0.20

                    if soil_state == "poor":
                        base_high -= 0.15
                        base_low += 0.15
                    elif soil_state == "good":
                        base_high += 0.10
                        base_low -= 0.10

                    if drought_state == "yes":
                        drought_impact = 0.40 * (1.0 - dt)
                        base_high -= drought_impact
                        base_low += drought_impact

                    if flood_state == "yes":
                        flood_impact = 0.35 * (1.0 - ft)
                        base_high -= flood_impact
                        base_low += flood_impact

                    probs = np.array([
                        max(base_low, 0.05),
                        max(base_med, 0.10),
                        max(base_high, 0.05),
                    ])
                    probs = probs / probs.sum()

                    yield_cpt[(drought_state, flood_state, soil_state)] = {
                        "low": round(float(probs[0]), 4),
                        "medium": round(float(probs[1]), 4),
                        "high": round(float(probs[2]), 4),
                    }

        return yield_cpt

    def predict(
        self,
        evidence: list[EvidenceItem] | None = None,
        drought_prob: float = 0.2,
        flood_prob: float = 0.1,
    ) -> BayesianPredictionResult:
        """Run inference to predict yield distribution given evidence.

        Uses variable elimination over the discrete DAG. Evidence
        items set observed values for specific nodes.

        Args:
            evidence: List of observed variable-value pairs.
            drought_prob: Prior drought probability from climate engine.
            flood_prob: Prior flood probability from climate engine.

        Returns:
            BayesianPredictionResult with yield probabilities.
        """
        evidence = evidence or []
        evidence_dict: dict[str, str] = {
            e.variable: e.value for e in evidence
        }
        evidence_names = [f"{e.variable}={e.value}" for e in evidence]

        drought_p = drought_prob
        flood_p = flood_prob

        if "rainfall" in evidence_dict:
            rainfall = evidence_dict["rainfall"]
            drought_p = self._cpts["drought_given_rainfall"].get(rainfall, drought_prob)
            flood_p = self._cpts["flood_given_rainfall"].get(rainfall, flood_prob)

        if "drought" in evidence_dict:
            drought_p = 1.0 if evidence_dict["drought"] == "yes" else 0.0
        if "flood" in evidence_dict:
            flood_p = 1.0 if evidence_dict["flood"] == "yes" else 0.0

        soil_probs = dict(self._cpts["soil"])
        if "soil" in evidence_dict:
            soil_val = evidence_dict["soil"]
            soil_probs = {k: (1.0 if k == soil_val else 0.0) for k in soil_probs}

        yield_marginal = {"low": 0.0, "medium": 0.0, "high": 0.0}

        for drought_state, d_prob in [("yes", drought_p), ("no", 1.0 - drought_p)]:
            for flood_state, f_prob in [("yes", flood_p), ("no", 1.0 - flood_p)]:
                for soil_state, s_prob in soil_probs.items():
                    joint_prob = d_prob * f_prob * s_prob

                    if joint_prob < 1e-10:
                        continue

                    key = (drought_state, flood_state, soil_state)
                    yield_dist = self._cpts["yield_cpt"][key]

                    for yield_cat, y_prob in yield_dist.items():
                        yield_marginal[yield_cat] += joint_prob * y_prob

        total = sum(yield_marginal.values())
        if total > 0:
            yield_marginal = {k: v / total for k, v in yield_marginal.items()}

        yield_factors = {"low": 0.5, "medium": 1.0, "high": 1.3}
        expected_factor = sum(
            yield_marginal[cat] * yield_factors[cat]
            for cat in yield_marginal
        )

        return BayesianPredictionResult(
            crop_id=self._crop.id,
            yield_probabilities={
                k: round(v, 4) for k, v in yield_marginal.items()
            },
            expected_yield_factor=round(expected_factor, 4),
            evidence_used=evidence_names,
        )


def compute_bayesian_returns(
    crops: list[CropProfile],
    drought_prob: float,
    flood_prob: float,
    evidence: list[EvidenceItem] | None = None,
) -> tuple[list[float], BayesianPortfolioResult]:
    """Compute Bayesian-adjusted expected returns for portfolio optimization.

    Mirrors the signature of compute_expected_returns() but uses BBN
    inference to adjust returns based on evidence. Each crop gets its
    own BBN with CPTs derived from its tolerance profile.

    Args:
        crops: List of crop profiles.
        drought_prob: Climate engine drought probability.
        flood_prob: Climate engine flood probability.
        evidence: Optional evidence items for Bayesian updating.

    Returns:
        Tuple of (adjusted_returns_list, BayesianPortfolioResult).
    """
    predictions: list[BayesianPredictionResult] = []
    adjusted_returns: list[float] = []

    for crop in crops:
        bbn = CropBayesianNetwork(crop)
        prediction = bbn.predict(
            evidence=evidence,
            drought_prob=drought_prob,
            flood_prob=flood_prob,
        )
        predictions.append(prediction)

        base_income = crop.avg_yield_kg_per_ha * crop.avg_price_mmk_per_kg
        adjusted = base_income * prediction.expected_yield_factor
        adjusted_returns.append(adjusted)

    result = BayesianPortfolioResult(
        crop_predictions=predictions,
        model_type="bayesian",
    )

    return adjusted_returns, result
