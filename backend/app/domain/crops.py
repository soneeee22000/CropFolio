"""Myanmar crop profiles with agronomic and economic characteristics."""

# DATA SOURCES
# Yield: FAOSTAT via data.un.org, element 5419, country 28 (Myanmar), 2010-2021.
#        Recent yield = mean of 2019-2021.
# Yield variance: CV computed from FAOSTAT 12-year national yield series.
#        Note: national-level CV underestimates farm-level risk.
# Prices: WFP VAM Food Prices Myanmar (data.humdata.org),
#         WFP Market Price Bulletins 2022-2025
# Tolerance: FAO AquaCrop reference manual, IRRI Knowledge Bank

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
        avg_yield_kg_per_ha=3804.0,  # FAOSTAT: Myanmar mean 2019-2021
        yield_variance=0.0169,  # FAOSTAT: CV from 2010-2021 national yields
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
        avg_yield_kg_per_ha=932.0,  # FAOSTAT: beans_dry proxy, mean 2019-2021
        yield_variance=0.016,  # FAOSTAT: CV from beans_dry 2014-2021
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
        avg_yield_kg_per_ha=932.0,  # FAOSTAT: beans_dry proxy, mean 2019-2021
        yield_variance=0.016,  # FAOSTAT: CV from beans_dry 2014-2021
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
        avg_yield_kg_per_ha=1336.0,  # FAOSTAT: Myanmar mean 2019-2021
        yield_variance=0.0526,  # FAOSTAT: CV from 2010-2021 national yields
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
        avg_yield_kg_per_ha=469.0,  # FAOSTAT: Myanmar mean 2019-2021
        yield_variance=0.0674,  # FAOSTAT: CV from 2010-2021 national yields
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
        avg_yield_kg_per_ha=1419.0,  # FAOSTAT: Myanmar mean 2019-2021
        yield_variance=0.0475,  # FAOSTAT: CV from 2010-2021 national yields
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
