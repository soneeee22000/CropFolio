"""Unit tests for the SAR pipeline."""

from __future__ import annotations

import pytest

from app.infrastructure.sar_pipeline import (
    MockSARPipeline,
    SARAnalysisResult,
)


@pytest.fixture()
def mock_pipeline():
    """Mock SAR pipeline instance."""
    return MockSARPipeline()


class TestMockSARPipeline:
    """Tests for the mock SAR pipeline."""

    def test_analyze_returns_result(self, mock_pipeline):
        """Analysis should return a SARAnalysisResult."""
        result = mock_pipeline.analyze(
            township_id="monywa",
            latitude=21.9,
            longitude=95.1,
            season="monsoon",
            year=2025,
        )
        assert isinstance(result, SARAnalysisResult)
        assert result.township_id == "monywa"

    def test_time_series_has_points(self, mock_pipeline):
        """Time series should have data points."""
        result = mock_pipeline.analyze(
            "monywa", 21.9, 95.1, "monsoon", 2025,
        )
        assert len(result.time_series) > 0

    def test_phenology_signals_detected(self, mock_pipeline):
        """Should detect phenological signals."""
        result = mock_pipeline.analyze(
            "monywa", 21.9, 95.1, "monsoon", 2025,
        )
        assert len(result.phenology_signals) == 4
        signal_types = {s.signal_type for s in result.phenology_signals}
        assert "flooding" in signal_types
        assert "tillering" in signal_types

    def test_rice_detected_with_confidence(self, mock_pipeline):
        """Mock should detect rice with reasonable confidence."""
        result = mock_pipeline.analyze(
            "monywa", 21.9, 95.1, "monsoon", 2025,
        )
        assert result.rice_detected is True
        assert result.rice_confidence > 0.5

    def test_different_locations_vary(self, mock_pipeline):
        """Different lat/lon should produce different VH values."""
        r1 = mock_pipeline.analyze(
            "loc_a", 16.0, 96.0, "monsoon", 2025,
        )
        r2 = mock_pipeline.analyze(
            "loc_b", 25.0, 98.0, "monsoon", 2025,
        )
        vh_1 = [p.vh_db for p in r1.time_series]
        vh_2 = [p.vh_db for p in r2.time_series]
        assert vh_1 != vh_2
