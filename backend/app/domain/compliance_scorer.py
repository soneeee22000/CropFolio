"""Compliance scoring algorithm for farmer crop plan adherence.

Computes a 0.0-1.0 composite score from five weighted dimensions:
- Fertilizer timing accuracy (30%)
- Fertilizer quantity accuracy (25%)
- Crop selection adherence (20%)
- SAR satellite verification (15%)
- Reporting regularity (10%)
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

WEIGHT_TIMING = 0.30
WEIGHT_QUANTITY = 0.25
WEIGHT_CROP_SELECTION = 0.20
WEIGHT_SAR_VERIFICATION = 0.15
WEIGHT_REPORTING = 0.10

TIMING_TOLERANCE_DAYS = 14
DEFAULT_SAR_SCORE = 0.5


@dataclass(frozen=True)
class ApplicationRecord:
    """Minimal fertilizer application record for scoring."""

    planned_day: int
    actual_day: int | None
    planned_rate: float
    actual_rate: float | None
    applied: bool


@dataclass(frozen=True)
class ComplianceResult:
    """Detailed compliance scoring result with component breakdown."""

    overall_score: float
    timing_score: float
    quantity_score: float
    crop_selection_score: float
    sar_score: float
    reporting_score: float
    level: str
    deviations: list[str]


def compute_compliance_score(
    applications: list[ApplicationRecord],
    crop_ids_planned: list[str],
    crop_ids_planted: list[str] | None = None,
    sar_planting_confirmed: bool | None = None,
    current_day: int = 0,
) -> ComplianceResult:
    """Compute the composite compliance score for a crop plan.

    Args:
        applications: List of fertilizer application records.
        crop_ids_planned: Crop IDs in the accepted plan.
        crop_ids_planted: Crop IDs actually planted (if known).
        sar_planting_confirmed: Whether SAR verified planting.
        current_day: Current day relative to plan start.

    Returns:
        ComplianceResult with overall score and component breakdown.
    """
    deviations: list[str] = []

    timing = _score_timing(applications, deviations)
    quantity = _score_quantity(applications, deviations)
    crop_selection = _score_crop_selection(
        crop_ids_planned, crop_ids_planted, deviations
    )
    sar = _score_sar(sar_planting_confirmed)
    reporting = _score_reporting(applications, current_day, deviations)

    overall = (
        WEIGHT_TIMING * timing
        + WEIGHT_QUANTITY * quantity
        + WEIGHT_CROP_SELECTION * crop_selection
        + WEIGHT_SAR_VERIFICATION * sar
        + WEIGHT_REPORTING * reporting
    )

    level = _classify_level(overall)

    return ComplianceResult(
        overall_score=round(overall, 4),
        timing_score=round(timing, 4),
        quantity_score=round(quantity, 4),
        crop_selection_score=round(crop_selection, 4),
        sar_score=round(sar, 4),
        reporting_score=round(reporting, 4),
        level=level,
        deviations=deviations,
    )


def _score_timing(
    apps: list[ApplicationRecord], deviations: list[str]
) -> float:
    """Score fertilizer application timing accuracy."""
    scores = []
    for app in apps:
        if app.applied and app.actual_day is not None:
            day_diff = abs(app.actual_day - app.planned_day)
            score = max(0.0, 1.0 - day_diff / TIMING_TOLERANCE_DAYS)
            scores.append(score)
            if day_diff > TIMING_TOLERANCE_DAYS:
                deviations.append(
                    f"Application day {app.planned_day}: "
                    f"{day_diff} days late"
                )
    return mean(scores) if scores else 0.0


def _score_quantity(
    apps: list[ApplicationRecord], deviations: list[str]
) -> float:
    """Score fertilizer quantity accuracy."""
    scores = []
    for app in apps:
        if app.applied and app.actual_rate is not None:
            if app.planned_rate <= 0:
                continue
            deviation_pct = abs(
                app.actual_rate - app.planned_rate
            ) / app.planned_rate
            score = max(0.0, 1.0 - deviation_pct)
            scores.append(score)
            if deviation_pct > 0.3:
                deviations.append(
                    f"Day {app.planned_day}: rate deviation "
                    f"{deviation_pct:.0%}"
                )
    return mean(scores) if scores else 0.0


def _score_crop_selection(
    planned: list[str],
    planted: list[str] | None,
    deviations: list[str],
) -> float:
    """Score crop selection adherence."""
    if planted is None:
        return 1.0
    planned_set = set(planned)
    planted_set = set(planted)
    if planned_set == planted_set:
        return 1.0
    missing = planned_set - planted_set
    if missing:
        deviations.append(f"Crops not planted: {', '.join(missing)}")
    overlap = len(planned_set & planted_set)
    return overlap / len(planned_set) if planned_set else 0.0


def _score_sar(confirmed: bool | None) -> float:
    """Score SAR satellite verification."""
    if confirmed is None:
        return DEFAULT_SAR_SCORE
    return 1.0 if confirmed else 0.0


def _score_reporting(
    apps: list[ApplicationRecord],
    current_day: int,
    deviations: list[str],
) -> float:
    """Score reporting regularity."""
    expected = [a for a in apps if a.planned_day <= current_day]
    if not expected:
        return 1.0
    reported = sum(1 for a in expected if a.applied)
    score = reported / len(expected)
    unreported = len(expected) - reported
    if unreported > 0:
        deviations.append(f"{unreported} applications not reported")
    return score


def _classify_level(score: float) -> str:
    """Classify a compliance score into a human-readable level."""
    if score >= 0.8:
        return "compliant"
    if score >= 0.5:
        return "warning"
    return "deviation"
