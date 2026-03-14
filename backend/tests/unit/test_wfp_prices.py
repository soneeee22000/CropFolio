"""Unit tests for WFP price data loader."""

from __future__ import annotations

from app.infrastructure.wfp_prices import (
    PriceRecord,
    compute_price_statistics,
    load_price_history,
)


class TestLoadPriceHistory:
    """Tests for load_price_history."""

    def test_load_rice_returns_records(self) -> None:
        """Should load rice.csv and return list of PriceRecord."""
        records = load_price_history("rice")
        assert records is not None
        assert len(records) == 48
        assert isinstance(records[0], PriceRecord)
        assert records[0].market == "Mandalay"

    def test_load_nonexistent_returns_none(self) -> None:
        """Should return None for a crop that has no CSV."""
        result = load_price_history("nonexistent_crop")
        assert result is None

    def test_all_crops_loadable(self) -> None:
        """All six crop CSVs should be loadable."""
        crop_ids = ["rice", "black_gram", "green_gram", "chickpea", "sesame", "groundnut"]
        for crop_id in crop_ids:
            records = load_price_history(crop_id)
            assert records is not None, f"Failed to load {crop_id}"
            assert len(records) == 48, f"Wrong row count for {crop_id}"


class TestComputePriceStatistics:
    """Tests for compute_price_statistics."""

    def test_known_values(self) -> None:
        """Should compute correct mean and CV for known inputs."""
        records = [
            PriceRecord(date="2023-01-01", price_mmk_per_kg=100.0, market="Test"),
            PriceRecord(date="2023-02-01", price_mmk_per_kg=200.0, market="Test"),
            PriceRecord(date="2023-03-01", price_mmk_per_kg=300.0, market="Test"),
        ]
        stats = compute_price_statistics(records)

        assert stats["mean"] == 200.0
        assert stats["min"] == 100.0
        assert stats["max"] == 300.0
        assert stats["cv"] > 0

    def test_rice_statistics_reasonable(self) -> None:
        """Rice price stats should be within expected ranges."""
        records = load_price_history("rice")
        assert records is not None
        stats = compute_price_statistics(records)

        assert 400 < stats["mean"] < 900
        assert stats["min"] >= 400
        assert stats["max"] <= 1000
        assert 0.0 < stats["cv"] < 1.0
