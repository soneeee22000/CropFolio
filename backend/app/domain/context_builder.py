"""Context builder — assembles platform data into structured LLM prompts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.domain.crops import get_all_crops
from app.domain.fertilizers import get_soil_profile
from app.infrastructure.wfp_prices import load_price_history


@dataclass(frozen=True)
class CropContextEntry:
    """Crop data assembled for LLM context."""

    name: str
    name_mm: str
    category: str
    avg_yield_kg_per_ha: float
    avg_price_mmk_per_kg: float
    drought_tolerance: float
    flood_tolerance: float
    growing_season: str


@dataclass(frozen=True)
class SoilContextSummary:
    """Soil profile summary for LLM context."""

    ph: float
    nitrogen_g_per_kg: float
    texture: str
    fertility: str
    clay_pct: int
    sand_pct: int


@dataclass(frozen=True)
class ClimateContextSummary:
    """Climate risk summary for LLM context."""

    drought_probability: float
    flood_probability: float
    risk_level: str
    rainfall_mm: float


@dataclass(frozen=True)
class PriceContextEntry:
    """Recent price info for a crop."""

    crop_name: str
    recent_price_mmk: float
    num_records: int


@dataclass
class TownshipContext:
    """Aggregated context for a township — ready for LLM rendering."""

    township_id: str
    township_name: str
    region: str
    season: str
    crops: list[CropContextEntry] = field(default_factory=list)
    soil: SoilContextSummary | None = None
    climate: ClimateContextSummary | None = None
    prices: list[PriceContextEntry] = field(default_factory=list)


def build_township_context(
    township_id: str,
    season: str,
    township: dict[str, Any],
    climate_risk: dict[str, Any] | None = None,
) -> TownshipContext:
    """Assemble all platform data for a township into structured context.

    Args:
        township_id: Township identifier.
        season: Growing season (monsoon/dry).
        township: Township dict from TownshipService.
        climate_risk: Optional climate risk data dict.

    Returns:
        Populated TownshipContext.
    """
    ctx = TownshipContext(
        township_id=township_id,
        township_name=township.get("name", township_id),
        region=township.get("region", "Unknown"),
        season=season,
    )

    ctx.crops = _build_crop_entries(season)
    ctx.soil = _build_soil_summary(township_id)
    ctx.climate = _build_climate_summary(climate_risk)
    ctx.prices = _build_price_entries()

    return ctx


def render_context_document(ctx: TownshipContext) -> str:
    """Format a TownshipContext into structured text for LLM prompting.

    Args:
        ctx: Populated TownshipContext.

    Returns:
        Multi-section text document.
    """
    sections = [
        _render_header(ctx),
        _render_climate(ctx.climate),
        _render_soil(ctx.soil),
        _render_crops(ctx.crops),
        _render_prices(ctx.prices),
    ]
    return "\n\n".join(s for s in sections if s)


def _build_crop_entries(season: str) -> list[CropContextEntry]:
    """Build crop context entries filtered by season compatibility."""
    entries: list[CropContextEntry] = []
    for crop in get_all_crops():
        if season == "dry" and crop.growing_season == "monsoon":
            continue
        if season == "monsoon" and crop.growing_season == "dry":
            continue
        entries.append(
            CropContextEntry(
                name=crop.name_en,
                name_mm=crop.name_mm,
                category=crop.category,
                avg_yield_kg_per_ha=crop.avg_yield_kg_per_ha,
                avg_price_mmk_per_kg=crop.avg_price_mmk_per_kg,
                drought_tolerance=crop.drought_tolerance,
                flood_tolerance=crop.flood_tolerance,
                growing_season=crop.growing_season,
            )
        )
    return entries


def _build_soil_summary(township_id: str) -> SoilContextSummary | None:
    """Build soil summary from soil profile data."""
    soil = get_soil_profile(township_id)
    if soil is None:
        return None
    return SoilContextSummary(
        ph=soil.ph_h2o,
        nitrogen_g_per_kg=soil.nitrogen_g_per_kg,
        texture=soil.texture_class,
        fertility=soil.fertility_rating,
        clay_pct=soil.clay_pct,
        sand_pct=soil.sand_pct,
    )


def _build_climate_summary(
    climate_risk: dict[str, Any] | None,
) -> ClimateContextSummary | None:
    """Build climate summary from risk assessment data."""
    if climate_risk is None:
        return None
    return ClimateContextSummary(
        drought_probability=climate_risk.get("drought_probability", 0.0),
        flood_probability=climate_risk.get("flood_probability", 0.0),
        risk_level=climate_risk.get("risk_level", "unknown"),
        rainfall_mm=climate_risk.get("rainfall_mm", 0.0),
    )


def _build_price_entries() -> list[PriceContextEntry]:
    """Build price context from WFP data for all crops."""
    entries: list[PriceContextEntry] = []
    for crop in get_all_crops():
        records = load_price_history(crop.id)
        if records:
            recent = records[-1].price_mmk_per_kg
            entries.append(
                PriceContextEntry(
                    crop_name=crop.name_en,
                    recent_price_mmk=recent,
                    num_records=len(records),
                )
            )
    return entries


def _render_header(ctx: TownshipContext) -> str:
    """Render header section."""
    return (
        f"=== Township Advisory Context ===\n"
        f"Township: {ctx.township_name}\n"
        f"Region: {ctx.region}\n"
        f"Season: {ctx.season}"
    )


def _render_climate(climate: ClimateContextSummary | None) -> str:
    """Render climate section."""
    if climate is None:
        return "=== Climate ===\nNo climate data available."
    return (
        f"=== Climate Risk ===\n"
        f"Drought Probability: {climate.drought_probability:.0%}\n"
        f"Flood Probability: {climate.flood_probability:.0%}\n"
        f"Overall Risk Level: {climate.risk_level}\n"
        f"Expected Rainfall: {climate.rainfall_mm:.0f} mm"
    )


def _render_soil(soil: SoilContextSummary | None) -> str:
    """Render soil section."""
    if soil is None:
        return "=== Soil ===\nNo soil data available."
    return (
        f"=== Soil Profile ===\n"
        f"pH: {soil.ph:.1f}\n"
        f"Nitrogen: {soil.nitrogen_g_per_kg:.1f} g/kg\n"
        f"Texture: {soil.texture}\n"
        f"Fertility: {soil.fertility}\n"
        f"Clay: {soil.clay_pct}%, Sand: {soil.sand_pct}%"
    )


def _render_crops(crops: list[CropContextEntry]) -> str:
    """Render crops section."""
    if not crops:
        return "=== Crops ===\nNo crop data available."
    lines = ["=== Suitable Crops ==="]
    for c in crops:
        lines.append(
            f"- {c.name} ({c.name_mm}): yield {c.avg_yield_kg_per_ha:.0f} kg/ha, "
            f"price {c.avg_price_mmk_per_kg:.0f} MMK/kg, "
            f"drought tol {c.drought_tolerance:.1f}, "
            f"flood tol {c.flood_tolerance:.1f}"
        )
    return "\n".join(lines)


def _render_prices(prices: list[PriceContextEntry]) -> str:
    """Render price section."""
    if not prices:
        return "=== Market Prices ===\nNo price data available."
    lines = ["=== Market Prices (WFP) ==="]
    for p in prices:
        lines.append(
            f"- {p.crop_name}: {p.recent_price_mmk:.0f} MMK/kg "
            f"({p.num_records} observations)"
        )
    return "\n".join(lines)
