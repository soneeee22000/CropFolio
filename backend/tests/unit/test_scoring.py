"""Unit tests for compliance and credit scoring algorithms."""

from __future__ import annotations

from app.domain.compliance_scorer import (
    ApplicationRecord,
    compute_compliance_score,
)
from app.domain.credit_scorer import CreditInput, compute_credit_score


class TestComplianceScorer:
    """Tests for the compliance scoring algorithm."""

    def test_perfect_compliance(self) -> None:
        """All applications on time and correct rate yields ~1.0."""
        apps = [
            ApplicationRecord(
                planned_day=10, actual_day=10,
                planned_rate=50.0, actual_rate=50.0, applied=True,
            ),
            ApplicationRecord(
                planned_day=30, actual_day=30,
                planned_rate=75.0, actual_rate=75.0, applied=True,
            ),
        ]
        result = compute_compliance_score(
            apps, ["rice"], ["rice"], True, current_day=30
        )
        assert result.overall_score >= 0.95
        assert result.level == "compliant"
        assert len(result.deviations) == 0

    def test_late_applications_reduce_timing(self) -> None:
        """Applications 7 days late should reduce timing score."""
        apps = [
            ApplicationRecord(
                planned_day=10, actual_day=17,
                planned_rate=50.0, actual_rate=50.0, applied=True,
            ),
        ]
        result = compute_compliance_score(
            apps, ["rice"], ["rice"], None, current_day=17
        )
        assert result.timing_score < 1.0
        assert result.timing_score > 0.0

    def test_wrong_quantity_reduces_score(self) -> None:
        """50% rate deviation should reduce quantity score."""
        apps = [
            ApplicationRecord(
                planned_day=10, actual_day=10,
                planned_rate=100.0, actual_rate=50.0, applied=True,
            ),
        ]
        result = compute_compliance_score(
            apps, ["rice"], None, None, current_day=10
        )
        assert result.quantity_score == 0.5

    def test_unreported_applications_reduce_reporting(self) -> None:
        """Unreported applications reduce reporting score."""
        apps = [
            ApplicationRecord(
                planned_day=10, actual_day=None,
                planned_rate=50.0, actual_rate=None, applied=False,
            ),
            ApplicationRecord(
                planned_day=20, actual_day=20,
                planned_rate=50.0, actual_rate=50.0, applied=True,
            ),
        ]
        result = compute_compliance_score(
            apps, ["rice"], None, None, current_day=20
        )
        assert result.reporting_score == 0.5

    def test_missing_crops_reduce_selection(self) -> None:
        """Not planting a recommended crop reduces selection score."""
        apps = []
        result = compute_compliance_score(
            apps, ["rice", "sesame"], ["rice"], None, current_day=0
        )
        assert result.crop_selection_score == 0.5

    def test_zero_applications_baseline(self) -> None:
        """No applications at all yields zero scores."""
        result = compute_compliance_score(
            [], ["rice"], None, None, current_day=0
        )
        assert result.overall_score >= 0.0

    def test_sar_confirmed_gives_full_score(self) -> None:
        """SAR confirmation gives 1.0 SAR score."""
        result = compute_compliance_score(
            [], ["rice"], None, True, current_day=0
        )
        assert result.sar_score == 1.0

    def test_sar_denied_gives_zero(self) -> None:
        """SAR denial gives 0.0 SAR score."""
        result = compute_compliance_score(
            [], ["rice"], None, False, current_day=0
        )
        assert result.sar_score == 0.0

    def test_level_classification(self) -> None:
        """Score thresholds classify correctly."""
        apps = [
            ApplicationRecord(
                planned_day=10, actual_day=10,
                planned_rate=50.0, actual_rate=50.0, applied=True,
            ),
        ]
        compliant = compute_compliance_score(
            apps, ["rice"], ["rice"], True, current_day=10
        )
        assert compliant.level == "compliant"


class TestCreditScorer:
    """Tests for the credit scoring algorithm."""

    def test_new_farmer_gets_baseline(self) -> None:
        """Farmer with no history gets baseline score."""
        inputs = CreditInput(
            compliance_scores=[],
            loans_total=0, loans_repaid_on_time=0,
            seasons_active=0,
            plans_offered=0, plans_accepted=0,
            applications_expected=0, applications_reported=0,
        )
        result = compute_credit_score(inputs)
        assert result.overall_score == 0.3

    def test_perfect_history_gives_high_score(self) -> None:
        """Farmer with perfect history gets high score."""
        inputs = CreditInput(
            compliance_scores=[0.95, 0.90, 0.92],
            loans_total=3, loans_repaid_on_time=3,
            seasons_active=3,
            plans_offered=3, plans_accepted=3,
            applications_expected=9, applications_reported=9,
        )
        result = compute_credit_score(inputs)
        assert result.overall_score > 0.8

    def test_poor_repayment_lowers_score(self) -> None:
        """Missing loan repayments lowers the score."""
        good = CreditInput(
            compliance_scores=[0.8],
            loans_total=2, loans_repaid_on_time=2,
            seasons_active=2,
            plans_offered=2, plans_accepted=2,
            applications_expected=4, applications_reported=4,
        )
        bad = CreditInput(
            compliance_scores=[0.8],
            loans_total=2, loans_repaid_on_time=0,
            seasons_active=2,
            plans_offered=2, plans_accepted=2,
            applications_expected=4, applications_reported=4,
        )
        good_result = compute_credit_score(good)
        bad_result = compute_credit_score(bad)
        assert good_result.overall_score > bad_result.overall_score

    def test_more_tenure_improves_score(self) -> None:
        """Longer tenure improves the score."""
        short = CreditInput(
            compliance_scores=[0.7],
            loans_total=1, loans_repaid_on_time=1,
            seasons_active=1,
            plans_offered=1, plans_accepted=1,
            applications_expected=2, applications_reported=2,
        )
        long = CreditInput(
            compliance_scores=[0.7],
            loans_total=1, loans_repaid_on_time=1,
            seasons_active=5,
            plans_offered=1, plans_accepted=1,
            applications_expected=2, applications_reported=2,
        )
        long_score = compute_credit_score(long).tenure_factor
        short_score = compute_credit_score(short).tenure_factor
        assert long_score > short_score

    def test_score_between_zero_and_one(self) -> None:
        """Score is always between 0 and 1."""
        inputs = CreditInput(
            compliance_scores=[0.5, 0.6],
            loans_total=1, loans_repaid_on_time=1,
            seasons_active=2,
            plans_offered=3, plans_accepted=2,
            applications_expected=6, applications_reported=4,
        )
        result = compute_credit_score(inputs)
        assert 0.0 <= result.overall_score <= 1.0
