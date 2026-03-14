"""Unit tests for NASA POWER data extraction."""

from __future__ import annotations

import calendar

from app.infrastructure.nasa_power import _extract_annual_rainfall


class TestExtractAnnualRainfall:
    """Tests for _extract_annual_rainfall mm/day to mm/month conversion."""

    def test_uniform_3mm_day_produces_correct_annual(self) -> None:
        """3.0 mm/day across all months should yield ~1096mm (not 36mm)."""
        monthly_data = {}
        for month in range(1, 13):
            key = f"2023{month:02d}"
            monthly_data[key] = 3.0

        data = {"properties": {"parameter": {"PRECTOTCORR": monthly_data}}}
        result = _extract_annual_rainfall(data)

        expected = sum(
            3.0 * calendar.monthrange(2023, m)[1] for m in range(1, 13)
        )
        assert len(result) == 1
        assert abs(result[0] - expected) < 0.01
        assert result[0] > 1000  # Must not be the raw sum of 36

    def test_negative_values_skipped(self) -> None:
        """Values < 0 (e.g. -999 fill values) should be excluded."""
        monthly_data = {}
        for month in range(1, 13):
            key = f"2023{month:02d}"
            monthly_data[key] = -999.0 if month <= 6 else 2.0

        data = {"properties": {"parameter": {"PRECTOTCORR": monthly_data}}}
        result = _extract_annual_rainfall(data)

        assert len(result) == 1
        # Only July-December contribute
        expected = sum(
            2.0 * calendar.monthrange(2023, m)[1] for m in range(7, 13)
        )
        assert abs(result[0] - expected) < 0.01

    def test_leap_year_february(self) -> None:
        """Leap year February should use 29 days, not 28."""
        monthly_data = {"202402": 5.0}
        data = {"properties": {"parameter": {"PRECTOTCORR": monthly_data}}}
        result = _extract_annual_rainfall(data)

        assert len(result) == 1
        assert abs(result[0] - 5.0 * 29) < 0.01  # 29 days in Feb 2024

    def test_multi_year_data(self) -> None:
        """Multiple years should produce separate annual totals."""
        monthly_data = {}
        for year in [2022, 2023]:
            for month in range(1, 13):
                monthly_data[f"{year}{month:02d}"] = 2.0

        data = {"properties": {"parameter": {"PRECTOTCORR": monthly_data}}}
        result = _extract_annual_rainfall(data)

        assert len(result) == 2
        for total in result:
            assert total > 700  # 2mm/day * ~365 days
