"""Unit tests for context_builder module."""

from app.domain.context_builder import (
    TownshipContext,
    build_township_context,
    render_context_document,
)

MOCK_TOWNSHIP = {
    "id": "mdy_amarapura",
    "name": "Amarapura",
    "region": "Mandalay",
    "lat": 21.87,
    "lon": 96.04,
}


class TestBuildTownshipContext:
    """Tests for build_township_context."""

    def test_builds_valid_context(self) -> None:
        """Context is assembled with crops, soil, and prices."""
        ctx = build_township_context(
            township_id="mdy_amarapura",
            season="monsoon",
            township=MOCK_TOWNSHIP,
        )
        assert isinstance(ctx, TownshipContext)
        assert ctx.township_id == "mdy_amarapura"
        assert ctx.township_name == "Amarapura"
        assert ctx.region == "Mandalay"
        assert ctx.season == "monsoon"
        assert len(ctx.crops) > 0

    def test_builds_context_with_climate(self) -> None:
        """Climate data is included when provided."""
        climate = {
            "drought_probability": 0.3,
            "flood_probability": 0.2,
            "risk_level": "moderate",
            "rainfall_mm": 1200.0,
        }
        ctx = build_township_context(
            township_id="mdy_amarapura",
            season="monsoon",
            township=MOCK_TOWNSHIP,
            climate_risk=climate,
        )
        assert ctx.climate is not None
        assert ctx.climate.drought_probability == 0.3
        assert ctx.climate.risk_level == "moderate"

    def test_handles_missing_climate(self) -> None:
        """Context works without climate data."""
        ctx = build_township_context(
            township_id="mdy_amarapura",
            season="monsoon",
            township=MOCK_TOWNSHIP,
            climate_risk=None,
        )
        assert ctx.climate is None

    def test_handles_unknown_township_soil(self) -> None:
        """Context handles township with no soil data."""
        ctx = build_township_context(
            township_id="nonexistent_township_xyz",
            season="monsoon",
            township={"name": "Test", "region": "Test"},
        )
        assert ctx.soil is None


class TestRenderContextDocument:
    """Tests for render_context_document."""

    def test_renders_all_sections(self) -> None:
        """Rendered document includes all section headers."""
        ctx = build_township_context(
            township_id="mdy_amarapura",
            season="monsoon",
            township=MOCK_TOWNSHIP,
        )
        doc = render_context_document(ctx)
        assert "Township Advisory Context" in doc
        assert "Amarapura" in doc
        assert "Suitable Crops" in doc

    def test_renders_with_climate(self) -> None:
        """Rendered document includes climate section."""
        climate = {
            "drought_probability": 0.25,
            "flood_probability": 0.15,
            "risk_level": "moderate",
            "rainfall_mm": 1500.0,
        }
        ctx = build_township_context(
            township_id="mdy_amarapura",
            season="monsoon",
            township=MOCK_TOWNSHIP,
            climate_risk=climate,
        )
        doc = render_context_document(ctx)
        assert "Climate Risk" in doc
        assert "25%" in doc
        assert "moderate" in doc

    def test_renders_without_climate(self) -> None:
        """Rendered document handles missing climate gracefully."""
        ctx = build_township_context(
            township_id="mdy_amarapura",
            season="monsoon",
            township=MOCK_TOWNSHIP,
            climate_risk=None,
        )
        doc = render_context_document(ctx)
        assert "No climate data available" in doc
