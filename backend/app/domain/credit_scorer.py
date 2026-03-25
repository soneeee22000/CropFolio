"""Credit scoring algorithm for farmer creditworthiness.

Computes a 0.0-1.0 evolving credit score from five factors:
- Cumulative compliance history (40%)
- Loan repayment history (30%)
- Tenure / seasons active (15%)
- Plan acceptance rate (10%)
- Reporting engagement (5%)

After 2 seasons, this score becomes the basis for loan amounts
and a competitive moat no new entrant can replicate.
"""

from __future__ import annotations

from dataclasses import dataclass

WEIGHT_COMPLIANCE = 0.40
WEIGHT_REPAYMENT = 0.30
WEIGHT_TENURE = 0.15
WEIGHT_ACCEPTANCE = 0.10
WEIGHT_ENGAGEMENT = 0.05

MAX_TENURE_SEASONS = 10
BASELINE_SCORE = 0.3


@dataclass(frozen=True)
class CreditInput:
    """Input data for credit score computation."""

    compliance_scores: list[float]
    loans_total: int
    loans_repaid_on_time: int
    seasons_active: int
    plans_offered: int
    plans_accepted: int
    applications_expected: int
    applications_reported: int


@dataclass(frozen=True)
class CreditResult:
    """Credit scoring result with component breakdown."""

    overall_score: float
    compliance_factor: float
    repayment_factor: float
    tenure_factor: float
    acceptance_factor: float
    engagement_factor: float


def compute_credit_score(inputs: CreditInput) -> CreditResult:
    """Compute a farmer's credit score from historical data.

    New farmers with no history start at BASELINE_SCORE (0.3)
    and build up through demonstrated compliance and repayment.
    """
    compliance = _compliance_factor(inputs.compliance_scores)
    repayment = _repayment_factor(
        inputs.loans_total, inputs.loans_repaid_on_time
    )
    tenure = _tenure_factor(inputs.seasons_active)
    acceptance = _acceptance_factor(
        inputs.plans_offered, inputs.plans_accepted
    )
    engagement = _engagement_factor(
        inputs.applications_expected, inputs.applications_reported
    )

    overall = (
        WEIGHT_COMPLIANCE * compliance
        + WEIGHT_REPAYMENT * repayment
        + WEIGHT_TENURE * tenure
        + WEIGHT_ACCEPTANCE * acceptance
        + WEIGHT_ENGAGEMENT * engagement
    )

    if not inputs.compliance_scores and inputs.loans_total == 0:
        overall = BASELINE_SCORE

    return CreditResult(
        overall_score=round(overall, 4),
        compliance_factor=round(compliance, 4),
        repayment_factor=round(repayment, 4),
        tenure_factor=round(tenure, 4),
        acceptance_factor=round(acceptance, 4),
        engagement_factor=round(engagement, 4),
    )


def _compliance_factor(scores: list[float]) -> float:
    """Average compliance score across all seasons."""
    if not scores:
        return BASELINE_SCORE
    return sum(scores) / len(scores)


def _repayment_factor(total: int, on_time: int) -> float:
    """Fraction of loans repaid on time."""
    if total == 0:
        return BASELINE_SCORE
    return on_time / total


def _tenure_factor(seasons: int) -> float:
    """Normalized tenure (capped at MAX_TENURE_SEASONS)."""
    if seasons <= 0:
        return 0.0
    return min(seasons / MAX_TENURE_SEASONS, 1.0)


def _acceptance_factor(offered: int, accepted: int) -> float:
    """Fraction of offered plans that farmer accepted."""
    if offered == 0:
        return BASELINE_SCORE
    return accepted / offered


def _engagement_factor(expected: int, reported: int) -> float:
    """Fraction of expected reports that farmer submitted."""
    if expected == 0:
        return 1.0
    return min(reported / expected, 1.0)
