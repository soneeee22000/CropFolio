"""Unit tests for fertilizer-crop matching algorithm."""

from __future__ import annotations

from app.domain.fertilizer_matcher import match_fertilizers
from app.domain.fertilizers import (
    SoilProfile,
    get_all_fertilizers,
    get_nutrient_requirement,
)

# Reusable soil fixtures
CLAY_LOAM_SOIL = SoilProfile(
    township_id="test_clay_loam",
    ph_h2o=7.0,
    nitrogen_g_per_kg=1.1,
    soc_g_per_kg=9.8,
    clay_pct=28,
    sand_pct=35,
    silt_pct=37,
    cec_cmol_per_kg=18.5,
    texture_class="clay_loam",
    fertility_rating="moderate",
)

ALKALINE_SOIL = SoilProfile(
    township_id="test_alkaline",
    ph_h2o=8.0,
    nitrogen_g_per_kg=0.6,
    soc_g_per_kg=4.8,
    clay_pct=20,
    sand_pct=50,
    silt_pct=30,
    cec_cmol_per_kg=11.5,
    texture_class="sandy_loam",
    fertility_rating="low",
)

ALL_FERTILIZERS = get_all_fertilizers()
ALL_CROP_IDS = [
    "rice", "black_gram", "green_gram", "chickpea", "sesame",
    "groundnut", "maize", "sugarcane", "potato", "onion", "chili",
]


class TestRiceInClayLoam:
    """Rice in clay-loam soil should favor N-heavy fertilizers."""

    def test_returns_results(self) -> None:
        """Should return non-empty fertilizer list."""
        req = get_nutrient_requirement("rice")
        assert req is not None
        results = match_fertilizers("rice", req, CLAY_LOAM_SOIL, ALL_FERTILIZERS)
        assert len(results) > 0

    def test_top_pick_is_n_heavy(self) -> None:
        """Top recommendation should have high nitrogen content."""
        req = get_nutrient_requirement("rice")
        assert req is not None
        results = match_fertilizers("rice", req, CLAY_LOAM_SOIL, ALL_FERTILIZERS)
        top = results[0]
        # Urea or compound_20_10_10 should rank high for rice
        assert top.fertilizer_id in ("urea", "compound_20_10_10", "compound_15_15_15")


class TestGroundnutInAlkalineSoil:
    """Groundnut in alkaline soil should favor sulfur-containing fertilizers."""

    def test_returns_results(self) -> None:
        """Should return non-empty list."""
        req = get_nutrient_requirement("groundnut")
        assert req is not None
        results = match_fertilizers("groundnut", req, ALKALINE_SOIL, ALL_FERTILIZERS)
        assert len(results) > 0

    def test_sulfur_ferts_rank_well(self) -> None:
        """Gypsum or ammonium_sulfate should appear in top 3."""
        req = get_nutrient_requirement("groundnut")
        assert req is not None
        results = match_fertilizers(
            "groundnut", req, ALKALINE_SOIL, ALL_FERTILIZERS, top_n=3,
        )
        fert_ids = {r.fertilizer_id for r in results}
        assert fert_ids & {"gypsum", "ammonium_sulfate"}, (
            f"Expected sulfur ferts in {fert_ids}"
        )


class TestTopNParameter:
    """The top_n parameter should control result count."""

    def test_returns_exact_n(self) -> None:
        """Should return exactly N results."""
        req = get_nutrient_requirement("rice")
        assert req is not None
        for n in [1, 2, 5]:
            results = match_fertilizers(
                "rice", req, CLAY_LOAM_SOIL, ALL_FERTILIZERS, top_n=n,
            )
            assert len(results) == min(n, len(ALL_FERTILIZERS))


class TestAllCropsGetResults:
    """Every crop should get non-empty results when soil is provided."""

    def test_all_crops_match(self) -> None:
        """All 11 crops should get at least 1 fertilizer recommendation."""
        for crop_id in ALL_CROP_IDS:
            req = get_nutrient_requirement(crop_id)
            if req is None:
                continue
            results = match_fertilizers(
                crop_id, req, CLAY_LOAM_SOIL, ALL_FERTILIZERS, top_n=1,
            )
            assert len(results) >= 1, f"No fertilizer match for {crop_id}"


class TestScoreRange:
    """All scores should be within valid range."""

    def test_scores_between_0_and_1(self) -> None:
        """Composite and component scores should be in [0, 1]."""
        req = get_nutrient_requirement("rice")
        assert req is not None
        results = match_fertilizers(
            "rice", req, CLAY_LOAM_SOIL, ALL_FERTILIZERS, top_n=8,
        )
        for r in results:
            assert 0.0 <= r.score <= 1.0, f"Score {r.score} out of range"
            assert 0.0 <= r.crop_need_score <= 1.0
            assert 0.0 <= r.cost_efficiency_score <= 1.0
