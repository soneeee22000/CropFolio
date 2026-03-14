"""Climate risk assessment engine for Myanmar townships."""

from dataclasses import dataclass

from app.core.constants import (
    DROUGHT_RAINFALL_PERCENTILE,
    FLOOD_RAINFALL_PERCENTILE,
    TEMP_ANOMALY_WARNING_CELSIUS,
)


@dataclass(frozen=True)
class ClimateRiskProfile:
    """Climate risk assessment for a township and season."""

    township_id: str
    township_name: str
    season: str
    drought_probability: float
    flood_probability: float
    temp_anomaly_celsius: float
    rainfall_forecast_mm: float
    rainfall_historical_avg_mm: float
    risk_level: str
    confidence: float


def assess_climate_risk(
    township_id: str,
    township_name: str,
    season: str,
    historical_rainfall: list[float],
    forecast_rainfall_mm: float,
    forecast_temp_anomaly: float,
) -> ClimateRiskProfile:
    """Assess climate risk for a township based on historical and forecast data.

    Args:
        township_id: Unique identifier for the township.
        township_name: Human-readable township name.
        season: 'monsoon' or 'dry'.
        historical_rainfall: List of historical seasonal rainfall values (mm).
        forecast_rainfall_mm: Forecasted rainfall for the upcoming season (mm).
        forecast_temp_anomaly: Forecasted temperature anomaly (°C vs. average).

    Returns:
        ClimateRiskProfile with computed risk probabilities.
    """
    if not historical_rainfall:
        return _default_risk_profile(township_id, township_name, season)

    sorted_rainfall = sorted(historical_rainfall)
    n = len(sorted_rainfall)

    drought_threshold_idx = max(0, int(n * DROUGHT_RAINFALL_PERCENTILE / 100) - 1)
    flood_threshold_idx = min(n - 1, int(n * FLOOD_RAINFALL_PERCENTILE / 100))

    drought_threshold = sorted_rainfall[drought_threshold_idx]
    flood_threshold = sorted_rainfall[flood_threshold_idx]

    historical_avg = sum(historical_rainfall) / n

    drought_prob = _compute_drought_probability(
        forecast_rainfall_mm, drought_threshold, historical_avg
    )
    flood_prob = _compute_flood_probability(
        forecast_rainfall_mm, flood_threshold, historical_avg
    )

    if abs(forecast_temp_anomaly) > TEMP_ANOMALY_WARNING_CELSIUS:
        drought_prob = min(drought_prob * 1.2, 0.95)

    risk_level = _classify_risk_level(drought_prob, flood_prob)
    confidence = min(0.5 + n * 0.02, 0.9)

    return ClimateRiskProfile(
        township_id=township_id,
        township_name=township_name,
        season=season,
        drought_probability=round(drought_prob, 3),
        flood_probability=round(flood_prob, 3),
        temp_anomaly_celsius=round(forecast_temp_anomaly, 2),
        rainfall_forecast_mm=round(forecast_rainfall_mm, 1),
        rainfall_historical_avg_mm=round(historical_avg, 1),
        risk_level=risk_level,
        confidence=round(confidence, 2),
    )


def _compute_drought_probability(
    forecast_mm: float,
    drought_threshold: float,
    historical_avg: float,
) -> float:
    """Estimate drought probability based on forecast vs. thresholds."""
    if historical_avg <= 0:
        return 0.5

    ratio = forecast_mm / historical_avg

    if forecast_mm <= drought_threshold:
        return min(0.7 + (1 - ratio) * 0.3, 0.95)
    elif ratio < 0.8:
        return 0.3 + (0.8 - ratio) * 1.0
    else:
        return max(0.05, 0.3 - (ratio - 0.8) * 0.5)


def _compute_flood_probability(
    forecast_mm: float,
    flood_threshold: float,
    historical_avg: float,
) -> float:
    """Estimate flood probability based on forecast vs. thresholds."""
    if historical_avg <= 0:
        return 0.5

    ratio = forecast_mm / historical_avg

    if forecast_mm >= flood_threshold:
        return min(0.6 + (ratio - 1) * 0.3, 0.95)
    elif ratio > 1.2:
        return 0.3 + (ratio - 1.2) * 0.5
    else:
        return max(0.05, ratio * 0.1)


def _classify_risk_level(
    drought_prob: float,
    flood_prob: float,
) -> str:
    """Classify overall risk as low, moderate, high, or critical."""
    max_risk = max(drought_prob, flood_prob)
    if max_risk >= 0.7:
        return "critical"
    elif max_risk >= 0.4:
        return "high"
    elif max_risk >= 0.2:
        return "moderate"
    return "low"


def _default_risk_profile(
    township_id: str,
    township_name: str,
    season: str,
) -> ClimateRiskProfile:
    """Return a default risk profile when no historical data is available."""
    return ClimateRiskProfile(
        township_id=township_id,
        township_name=township_name,
        season=season,
        drought_probability=0.3,
        flood_probability=0.2,
        temp_anomaly_celsius=0.0,
        rainfall_forecast_mm=0.0,
        rainfall_historical_avg_mm=0.0,
        risk_level="moderate",
        confidence=0.3,
    )
