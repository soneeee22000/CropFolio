"""Myanmar crop profiles with agronomic and economic characteristics."""

# DATA SOURCES
# Yield: FAO GAEZ v4 (gaez.fao.org), IRRI World Rice Statistics 2023,
#        Myanmar CSO Agricultural Statistics 2022-23
# Prices: WFP VAM Food Prices Myanmar (data.humdata.org),
#         WFP Market Price Bulletins 2022-2025
# Tolerance: FAO AquaCrop reference manual, IRRI Knowledge Bank
# Variance: Coefficient of variation from CSO/WFP time series

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
        drought_tolerance=0.3,  # FAO AquaCrop: paddy sensitive to drought
        flood_tolerance=0.7,  # IRRI: paddy tolerates standing water
        avg_yield_kg_per_ha=3800.0,  # IRRI: Myanmar avg 3.8 t/ha (2019-2023)
        yield_variance=0.25,  # CSO: CV ~25% across townships
        avg_price_mmk_per_kg=650.0,  # WFP: median Mandalay 2022-2025
        price_variance=0.15,  # WFP: price CV ~15%
    ),
    "black_gram": CropProfile(
        id="black_gram",
        name_en="Black Gram (Urad)",
        name_mm="မတ်ပဲ",
        category="pulse",
        growing_season="dry",
        drought_tolerance=0.7,  # FAO: moderate-high drought tolerance
        flood_tolerance=0.2,  # FAO: pulses waterlogging-sensitive
        avg_yield_kg_per_ha=1200.0,  # CSO: Myanmar avg 1.2 t/ha (2022-23)
        yield_variance=0.30,  # CSO: CV ~30%
        avg_price_mmk_per_kg=1800.0,  # WFP: median Mandalay 2022-2025
        price_variance=0.25,  # WFP: export-driven volatility
    ),
    "green_gram": CropProfile(
        id="green_gram",
        name_en="Green Gram (Mung Bean)",
        name_mm="ပဲတီစိမ်း",
        category="pulse",
        growing_season="dry",
        drought_tolerance=0.65,  # FAO: moderate drought tolerance
        flood_tolerance=0.25,  # FAO: slightly better than black gram
        avg_yield_kg_per_ha=1100.0,  # CSO: Myanmar avg 1.1 t/ha (2022-23)
        yield_variance=0.28,  # CSO: CV ~28%
        avg_price_mmk_per_kg=2000.0,  # WFP: median Mandalay 2022-2025
        price_variance=0.22,  # WFP: export price linkage
    ),
    "chickpea": CropProfile(
        id="chickpea",
        name_en="Chickpea",
        name_mm="ကုလားပဲ",
        category="pulse",
        growing_season="dry",
        drought_tolerance=0.85,  # FAO: high drought tolerance (deep roots)
        flood_tolerance=0.1,  # FAO: very waterlogging-sensitive
        avg_yield_kg_per_ha=900.0,  # CSO: Myanmar avg 0.9 t/ha (2022-23)
        yield_variance=0.35,  # CSO: CV ~35%, climate-sensitive
        avg_price_mmk_per_kg=2200.0,  # WFP: median Mandalay 2022-2025
        price_variance=0.20,  # WFP: domestic demand stabilizes
    ),
    "sesame": CropProfile(
        id="sesame",
        name_en="Sesame",
        name_mm="နှမ်း",
        category="oilseed",
        growing_season="dry",
        drought_tolerance=0.80,  # FAO: high drought tolerance
        flood_tolerance=0.1,  # FAO: very waterlogging-sensitive
        avg_yield_kg_per_ha=450.0,  # FAO GAEZ: Myanmar avg 0.45 t/ha
        yield_variance=0.40,  # CSO: CV ~40%, highly variable
        avg_price_mmk_per_kg=4500.0,  # WFP: median Mandalay 2022-2025
        price_variance=0.30,  # WFP: export-driven, high volatility
    ),
    "groundnut": CropProfile(
        id="groundnut",
        name_en="Groundnut (Peanut)",
        name_mm="မြေပဲ",
        category="oilseed",
        growing_season="dry",
        drought_tolerance=0.55,  # FAO: moderate, needs consistent moisture
        flood_tolerance=0.2,  # FAO: susceptible to waterlogging
        avg_yield_kg_per_ha=1500.0,  # CSO: Myanmar avg 1.5 t/ha (2022-23)
        yield_variance=0.30,  # CSO: CV ~30%
        avg_price_mmk_per_kg=2800.0,  # WFP: median Mandalay 2022-2025
        price_variance=0.18,  # WFP: stable domestic demand
    ),
}


def get_all_crops() -> list[CropProfile]:
    """Return all available Myanmar crop profiles."""
    return list(MYANMAR_CROPS.values())


def get_crop_by_id(crop_id: str) -> CropProfile | None:
    """Return a specific crop profile by ID."""
    return MYANMAR_CROPS.get(crop_id)
