"""Pydantic schemas for Monte Carlo simulation API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class SimulateRequest(BaseModel):
    """Request body for Monte Carlo simulation."""

    crop_ids: list[str] = Field(min_length=2, max_length=10)
    weights: dict[str, float]
    township_id: str
    num_simulations: int = Field(default=1000, ge=100, le=10000)
    season: Literal["monsoon", "dry"] = "monsoon"

    @model_validator(mode="after")
    def validate_weights_sum(self) -> SimulateRequest:
        """Ensure weights sum to approximately 1.0."""
        weight_sum = sum(self.weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            msg = f"Weights must sum to 1.0, got {weight_sum:.4f}"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_weights_match_crops(self) -> SimulateRequest:
        """Ensure all crop_ids have corresponding weights."""
        missing = set(self.crop_ids) - set(self.weights.keys())
        if missing:
            msg = f"Missing weights for crops: {missing}"
            raise ValueError(msg)
        return self


class HistogramBin(BaseModel):
    """Single bin in income distribution histogram."""

    bin_start: float
    bin_end: float
    count: int
    frequency: float


class SimulationStats(BaseModel):
    """Statistical summary of the simulation."""

    mean_income: float
    median_income: float
    std_dev: float
    percentile_5: float
    percentile_95: float
    prob_catastrophic_loss: float
    value_at_risk_95: float


class SimulateResponse(BaseModel):
    """Response from Monte Carlo simulation."""

    township_id: str
    township_name: str
    season: str
    num_simulations: int
    stats: SimulationStats
    histogram: list[HistogramBin]
