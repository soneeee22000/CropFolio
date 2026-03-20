"""Unit tests for the Field Monitor domain."""

from __future__ import annotations

import pytest

from app.domain.field_monitor import (
    AlertRuleEngine,
    ComplianceEngine,
    ComplianceInfo,
    ComplianceStatus,
    MockPlotGenerator,
)


@pytest.fixture()
def generator():
    """Mock plot generator instance."""
    return MockPlotGenerator()


class TestMockPlotGenerator:
    """Tests for MockPlotGenerator."""

    def test_generates_plots_within_count_range(self, generator):
        """Should generate between 5 and 15 plots."""
        plots = generator.generate("monywa", 21.9, 95.1)
        assert 5 <= len(plots) <= 15

    def test_deterministic_output(self, generator):
        """Same township should produce identical plots."""
        plots_a = generator.generate("monywa", 21.9, 95.1)
        plots_b = generator.generate("monywa", 21.9, 95.1)
        assert len(plots_a) == len(plots_b)
        for a, b in zip(plots_a, plots_b, strict=True):
            assert a.plot_id == b.plot_id
            assert a.farmer_name == b.farmer_name

    def test_different_townships_differ(self, generator):
        """Different townships should produce different plots."""
        plots_a = generator.generate("monywa", 21.9, 95.1)
        plots_b = generator.generate("myingyan", 21.4, 95.4)
        ids_a = {p.plot_id for p in plots_a}
        ids_b = {p.plot_id for p in plots_b}
        assert ids_a.isdisjoint(ids_b)

    def test_plots_near_center(self, generator):
        """Plots should be within 3km of center (approx 0.03 degrees)."""
        center_lat, center_lon = 21.9, 95.1
        plots = generator.generate("monywa", center_lat, center_lon)
        for plot in plots:
            lat_diff = abs(plot.location.latitude - center_lat)
            lon_diff = abs(plot.location.longitude - center_lon)
            assert lat_diff < 0.05
            assert lon_diff < 0.05

    def test_compliance_distribution(self, generator):
        """Should have a mix of compliance statuses."""
        plots = generator.generate("monywa", 21.9, 95.1)
        statuses = [p.compliance.status for p in plots]
        status_set = set(statuses)
        assert len(status_set) >= 1

    def test_each_plot_has_observations(self, generator):
        """Every plot should have SAR observation data."""
        plots = generator.generate("monywa", 21.9, 95.1)
        for plot in plots:
            assert len(plot.observations) > 0
            for obs in plot.observations:
                assert obs.date
                assert isinstance(obs.observed_vh_db, float)
                assert isinstance(obs.expected_vh_db, float)


class TestComplianceEngine:
    """Tests for ComplianceEngine."""

    def test_compliant_score_above_threshold(self):
        """Compliant status should have score >= 0.8."""
        import random

        rng = random.Random(42)
        info = ComplianceEngine.score(ComplianceStatus.COMPLIANT, rng)
        assert info.status == ComplianceStatus.COMPLIANT
        assert info.score >= 0.8
        assert info.planting_detected is True
        assert info.crop_match is True

    def test_warning_score_in_range(self):
        """Warning status should have score between 0.5 and 0.8."""
        import random

        rng = random.Random(42)
        info = ComplianceEngine.score(ComplianceStatus.WARNING, rng)
        assert info.status == ComplianceStatus.WARNING
        assert 0.5 <= info.score < 0.8

    def test_deviation_score_below_threshold(self):
        """Deviation status should have score < 0.5."""
        import random

        rng = random.Random(42)
        info = ComplianceEngine.score(ComplianceStatus.DEVIATION, rng)
        assert info.status == ComplianceStatus.DEVIATION
        assert info.score < 0.5
        assert info.crop_match is False


class TestAlertRuleEngine:
    """Tests for AlertRuleEngine."""

    def test_no_alerts_for_compliant(self):
        """Compliant plots should generate no alerts."""
        import random

        rng = random.Random(42)
        compliance = ComplianceInfo(
            status=ComplianceStatus.COMPLIANT,
            score=0.9,
            planting_detected=True,
            crop_match=True,
            phenology_match=0.9,
        )
        alerts = AlertRuleEngine.generate("plot_001", "U Test", compliance, rng)
        assert len(alerts) == 0

    def test_alerts_for_no_planting(self):
        """No planting should generate a critical alert."""
        import random

        rng = random.Random(42)
        compliance = ComplianceInfo(
            status=ComplianceStatus.DEVIATION,
            score=0.2,
            planting_detected=False,
            crop_match=False,
            phenology_match=0.1,
        )
        alerts = AlertRuleEngine.generate("plot_002", "U Test", compliance, rng)
        alert_types = {a.alert_type for a in alerts}
        assert "no_planting" in alert_types
        critical = [a for a in alerts if a.severity.value == "critical"]
        assert len(critical) >= 1

    def test_alerts_for_crop_mismatch(self):
        """Crop mismatch should generate a high-severity alert."""
        import random

        rng = random.Random(42)
        compliance = ComplianceInfo(
            status=ComplianceStatus.WARNING,
            score=0.6,
            planting_detected=True,
            crop_match=False,
            phenology_match=0.6,
        )
        alerts = AlertRuleEngine.generate("plot_003", "U Test", compliance, rng)
        alert_types = {a.alert_type for a in alerts}
        assert "crop_mismatch" in alert_types

    def test_severity_mapping(self):
        """Alerts should have valid severity values."""
        import random

        rng = random.Random(42)
        compliance = ComplianceInfo(
            status=ComplianceStatus.DEVIATION,
            score=0.2,
            planting_detected=True,
            crop_match=False,
            phenology_match=0.3,
        )
        alerts = AlertRuleEngine.generate("plot_004", "U Test", compliance, rng)
        valid_severities = {"low", "medium", "high", "critical"}
        for alert in alerts:
            assert alert.severity.value in valid_severities
