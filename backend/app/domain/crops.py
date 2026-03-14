"""Myanmar crop profiles with agronomic and economic characteristics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CropProfile:
    """Represents a crop's agronomic and economic profile for Myanmar."""

    id: str
    name_en: str
    name_mm: str
    category: str
    growing_season: str
    drought_tolerance: float
    flood_tolerance: float
    avg_yield_kg_per_ha: float
    yield_variance: float
    avg_price_mmk_per_kg: float
    price_variance: float


# Research-backed crop profiles for Myanmar
# Sources: FAO GAEZ, IRRI, Myanmar Agriculture Statistics
MYANMAR_CROPS: dict[str, CropProfile] = {
    "rice": CropProfile(
        id="rice",
        name_en="Rice (Paddy)",
        name_mm="စပါး",
        category="cereal",
        growing_season="monsoon",
        drought_tolerance=0.3,
        flood_tolerance=0.7,
        avg_yield_kg_per_ha=3800.0,
        yield_variance=0.25,
        avg_price_mmk_per_kg=650.0,
        price_variance=0.15,
    ),
    "black_gram": CropProfile(
        id="black_gram",
        name_en="Black Gram (Urad)",
        name_mm="မတ်ပဲ",
        category="pulse",
        growing_season="dry",
        drought_tolerance=0.7,
        flood_tolerance=0.2,
        avg_yield_kg_per_ha=1200.0,
        yield_variance=0.30,
        avg_price_mmk_per_kg=1800.0,
        price_variance=0.25,
    ),
    "green_gram": CropProfile(
        id="green_gram",
        name_en="Green Gram (Mung Bean)",
        name_mm="ပဲတီစိမ်း",
        category="pulse",
        growing_season="dry",
        drought_tolerance=0.65,
        flood_tolerance=0.25,
        avg_yield_kg_per_ha=1100.0,
        yield_variance=0.28,
        avg_price_mmk_per_kg=2000.0,
        price_variance=0.22,
    ),
    "chickpea": CropProfile(
        id="chickpea",
        name_en="Chickpea",
        name_mm="ကုလားပဲ",
        category="pulse",
        growing_season="dry",
        drought_tolerance=0.85,
        flood_tolerance=0.1,
        avg_yield_kg_per_ha=900.0,
        yield_variance=0.35,
        avg_price_mmk_per_kg=2200.0,
        price_variance=0.20,
    ),
    "sesame": CropProfile(
        id="sesame",
        name_en="Sesame",
        name_mm="နှမ်း",
        category="oilseed",
        growing_season="dry",
        drought_tolerance=0.80,
        flood_tolerance=0.1,
        avg_yield_kg_per_ha=450.0,
        yield_variance=0.40,
        avg_price_mmk_per_kg=4500.0,
        price_variance=0.30,
    ),
    "groundnut": CropProfile(
        id="groundnut",
        name_en="Groundnut (Peanut)",
        name_mm="မြေပဲ",
        category="oilseed",
        growing_season="dry",
        drought_tolerance=0.55,
        flood_tolerance=0.2,
        avg_yield_kg_per_ha=1500.0,
        yield_variance=0.30,
        avg_price_mmk_per_kg=2800.0,
        price_variance=0.18,
    ),
}


def get_all_crops() -> list[CropProfile]:
    """Return all available Myanmar crop profiles."""
    return list(MYANMAR_CROPS.values())


def get_crop_by_id(crop_id: str) -> CropProfile | None:
    """Return a specific crop profile by ID."""
    return MYANMAR_CROPS.get(crop_id)
