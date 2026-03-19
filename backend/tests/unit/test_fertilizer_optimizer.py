"""Unit tests for the enhanced fertilizer optimizer."""

from __future__ import annotations

import pytest

from app.domain.fertilizer_optimizer import (
    FertilizerPlan,
    optimize_fertilizer_plan,
)
from app.domain.fertilizers import SoilProfile


@pytest.fixture()
def alkaline_soil():
    """Alkaline soil profile (pH > 7.0, Zn deficiency risk)."""
    return SoilProfile(
        township_id="test_township",
        ph_h2o=7.5,
        nitrogen_g_per_kg=0.8,
        soc_g_per_kg=7.0,
        clay_pct=35,
        sand_pct=25,
        silt_pct=40,
        cec_cmol_per_kg=18.0,
        texture_class="clay_loam",
        fertility_rating="moderate",
    )


@pytest.fixture()
def acidic_soil():
    """Acidic soil profile (pH < 5.5)."""
    return SoilProfile(
        township_id="test_township",
        ph_h2o=5.2,
        nitrogen_g_per_kg=1.5,
        soc_g_per_kg=12.0,
        clay_pct=20,
        sand_pct=50,
        silt_pct=30,
        cec_cmol_per_kg=12.0,
        texture_class="sandy_loam",
        fertility_rating="moderate",
    )


class TestOptimizeFertilizerPlan:
    """Tests for LP-based fertilizer optimization."""

    def test_rice_plan_returns_plan(self, alkaline_soil):
        """Rice should produce a valid fertilizer plan."""
        plan = optimize_fertilizer_plan("rice", soil=alkaline_soil)
        assert plan is not None
        assert isinstance(plan, FertilizerPlan)
        assert plan.crop_id == "rice"

    def test_plan_has_applications(self, alkaline_soil):
        """Plan should have at least one application."""
        plan = optimize_fertilizer_plan("rice", soil=alkaline_soil)
        assert plan is not None
        assert len(plan.applications) > 0

    def test_plan_has_nutrient_totals(self, alkaline_soil):
        """Plan should report NPK totals."""
        plan = optimize_fertilizer_plan("rice", soil=alkaline_soil)
        assert plan is not None
        assert "N" in plan.nutrient_totals
        assert "P" in plan.nutrient_totals
        assert "K" in plan.nutrient_totals

    def test_rice_zinc_flag_on_alkaline_soil(self, alkaline_soil):
        """Rice on alkaline soil should flag zinc deficiency."""
        plan = optimize_fertilizer_plan("rice", soil=alkaline_soil)
        assert plan is not None

        zinc_flags = [
            f for f in plan.micronutrient_flags if f.nutrient == "zinc"
        ]
        assert len(zinc_flags) > 0

    def test_roi_estimate_positive(self, alkaline_soil):
        """ROI estimate should have positive return ratio."""
        plan = optimize_fertilizer_plan("rice", soil=alkaline_soil)
        assert plan is not None
        assert plan.roi_estimate.return_ratio > 0
        assert plan.roi_estimate.total_cost_mmk > 0

    def test_lp_feasible_for_rice(self, alkaline_soil):
        """LP should be feasible for rice (standard NPK requirements)."""
        plan = optimize_fertilizer_plan("rice", soil=alkaline_soil)
        assert plan is not None
        assert plan.lp_feasible is True

    def test_chickpea_plan(self, alkaline_soil):
        """Chickpea (pulse) should get a valid plan."""
        plan = optimize_fertilizer_plan("chickpea", soil=alkaline_soil)
        assert plan is not None
        assert plan.crop_id == "chickpea"

    def test_unknown_crop_returns_none(self):
        """Unknown crop should return None."""
        plan = optimize_fertilizer_plan("unknown_crop")
        assert plan is None

    def test_plan_without_soil(self):
        """Plan should work without soil profile (no micro flags)."""
        plan = optimize_fertilizer_plan("rice", soil=None)
        assert plan is not None

    def test_applications_sorted_by_day(self, alkaline_soil):
        """Applications should be sorted by growth stage day."""
        plan = optimize_fertilizer_plan("rice", soil=alkaline_soil)
        assert plan is not None
        days = [a.day for a in plan.applications]
        assert days == sorted(days)

    def test_all_crops_get_plans(self, alkaline_soil):
        """All 11 crops should produce valid plans."""
        crop_ids = [
            "rice", "black_gram", "green_gram", "chickpea",
            "sesame", "groundnut", "maize", "sugarcane",
            "potato", "onion", "chili",
        ]
        for crop_id in crop_ids:
            plan = optimize_fertilizer_plan(crop_id, soil=alkaline_soil)
            assert plan is not None, f"No plan for {crop_id}"
