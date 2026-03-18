"""Fertilizer profiles, soil profiles, and crop nutrient requirements for Myanmar."""

# DATA SOURCES
# Fertilizers: Common Myanmar market products (Awba, Golden Lion, other brands)
# Soil: ISRIC SoilGrids v2.0, 0-30cm median predictions
# Nutrients: FAO Bulletin 16, IRRI, ICRISAT, Myanmar DoA recommendations

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

FertilityRating = Literal[
    "very_low", "low", "moderate", "moderate_high", "high"
]
TextureClass = Literal[
    "sand", "loamy_sand", "sandy_loam", "loam",
    "silt_loam", "silt", "sandy_clay_loam", "clay_loam",
    "silty_clay_loam", "sandy_clay", "silty_clay", "clay",
]


@dataclass(frozen=True)
class FertilizerProfile:
    """Represents a fertilizer product available in Myanmar."""

    id: str
    name_en: str
    name_mm: str
    formulation: str
    nitrogen_pct: float
    phosphorus_pct: float
    potassium_pct: float
    sulfur_pct: float
    price_mmk_per_50kg: int
    application_rate_kg_per_ha: int
    availability: str
    notes: str


@dataclass(frozen=True)
class SoilProfile:
    """Soil characteristics for a Myanmar township at 0-30cm depth."""

    township_id: str
    ph_h2o: float
    nitrogen_g_per_kg: float
    soc_g_per_kg: float
    clay_pct: int
    sand_pct: int
    silt_pct: int
    cec_cmol_per_kg: float
    texture_class: str
    fertility_rating: str


@dataclass(frozen=True)
class CropNutrientRequirement:
    """NPK and sulfur requirements for a crop in kg/ha."""

    crop_id: str
    nitrogen_kg_per_ha: int
    phosphorus_kg_per_ha: int
    potassium_kg_per_ha: int
    sulfur_kg_per_ha: int
    primary_nutrient: str
    notes: str


@lru_cache(maxsize=1)
def _load_fertilizers_data() -> list[dict]:
    """Load fertilizer catalog from JSON."""
    path = DATA_DIR / "fertilizers.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_soil_profiles_data() -> dict:
    """Load soil profiles from JSON."""
    path = DATA_DIR / "soil_profiles.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_nutrient_requirements_data() -> dict:
    """Load crop nutrient requirements from JSON."""
    path = DATA_DIR / "crop_nutrient_requirements.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_fertilizer_matrix() -> dict[str, dict[str, float]]:
    """Load crop-fertilizer effectiveness matrix from JSON."""
    path = DATA_DIR / "crop_fertilizer_matrix.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Remove metadata key
    return {k: v for k, v in data.items() if not k.startswith("_")}


def get_all_fertilizers() -> list[FertilizerProfile]:
    """Return all available fertilizer profiles."""
    raw = _load_fertilizers_data()
    return [FertilizerProfile(**item) for item in raw]


def get_fertilizer_by_id(fertilizer_id: str) -> FertilizerProfile | None:
    """Return a specific fertilizer profile by ID."""
    for item in _load_fertilizers_data():
        if item["id"] == fertilizer_id:
            return FertilizerProfile(**item)
    return None


def get_soil_profile(township_id: str) -> SoilProfile | None:
    """Return soil profile for a specific township."""
    data = _load_soil_profiles_data()
    profile = data.get(township_id)
    if profile is None:
        logger.warning("No soil profile found for township: %s", township_id)
        return None
    return SoilProfile(**profile)


def get_all_soil_profiles() -> list[SoilProfile]:
    """Return soil profiles for all townships."""
    data = _load_soil_profiles_data()
    return [
        SoilProfile(**v)
        for k, v in data.items()
        if not k.startswith("_")
    ]


def get_nutrient_requirement(crop_id: str) -> CropNutrientRequirement | None:
    """Return NPK requirements for a specific crop."""
    data = _load_nutrient_requirements_data()
    req = data.get(crop_id)
    if req is None:
        return None
    return CropNutrientRequirement(**req)


def get_all_nutrient_requirements() -> dict[str, CropNutrientRequirement]:
    """Return NPK requirements for all crops."""
    data = _load_nutrient_requirements_data()
    return {
        k: CropNutrientRequirement(**v)
        for k, v in data.items()
        if not k.startswith("_")
    }


def get_fertilizer_matrix() -> dict[str, dict[str, float]]:
    """Return the crop-fertilizer effectiveness matrix."""
    return _load_fertilizer_matrix()


def get_crop_fertilizer_score(crop_id: str, fertilizer_id: str) -> float:
    """Return the effectiveness score for a crop-fertilizer pair.

    Returns 0.0 if the pair is not found in the matrix.
    """
    matrix = _load_fertilizer_matrix()
    crop_scores = matrix.get(crop_id, {})
    return crop_scores.get(fertilizer_id, 0.0)
