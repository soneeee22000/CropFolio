"""SAR (Sentinel-1) pipeline for rice paddy detection and planting verification.

Uses Sentinel-1 C-band SAR data (VH/VV polarization) to detect rice
paddy phenological stages from backscatter time series.

Real pipeline uses Google Earth Engine (optional dependency).
Mock pipeline provides realistic synthetic data for development.

Rice detection heuristic:
- VH dip in June-July (flooding) → rise in Aug-Sep (tillering)
  → peak in Oct (heading). Confidence = proportion of signals detected.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import ClassVar

from app.core.constants import (
    SAR_CONFIDENCE_MIN_SIGNALS,
    SAR_VH_FLOOD_THRESHOLD,
    SAR_VH_VEGETATION_THRESHOLD,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SARTimePoint:
    """A single SAR observation point."""

    date: str
    vh_db: float
    vv_db: float
    vh_vv_ratio: float


@dataclass(frozen=True)
class PhenologySignal:
    """A detected phenological signal from SAR time series."""

    signal_type: str
    detected: bool
    confidence: float
    date_range: str
    description: str


@dataclass(frozen=True)
class SARAnalysisResult:
    """Complete SAR analysis result for a township."""

    township_id: str
    analysis_date: str
    season: str
    time_series: list[SARTimePoint]
    phenology_signals: list[PhenologySignal]
    rice_detected: bool
    rice_confidence: float
    estimated_area_pct: float
    summary: str


class BaseSARPipeline(ABC):
    """Abstract base for SAR analysis pipelines."""

    @abstractmethod
    def analyze(
        self,
        township_id: str,
        latitude: float,
        longitude: float,
        season: str,
        year: int,
    ) -> SARAnalysisResult:
        """Run SAR analysis for a township location."""


class MockSARPipeline(BaseSARPipeline):
    """Mock SAR pipeline with realistic synthetic data.

    Returns data based on published Sentinel-1 VH profiles for
    Myanmar rice paddies (Torbick et al., 2017; Nguyen et al., 2016).
    Works without GEE credentials for development and demo.
    """

    RICE_VH_PROFILE: ClassVar[dict[str, float]] = {
        "2025-05-01": -16.5,
        "2025-05-15": -17.2,
        "2025-06-01": -18.8,
        "2025-06-15": -20.1,
        "2025-07-01": -21.3,
        "2025-07-15": -19.5,
        "2025-08-01": -17.8,
        "2025-08-15": -16.2,
        "2025-09-01": -14.5,
        "2025-09-15": -13.8,
        "2025-10-01": -12.9,
        "2025-10-15": -13.2,
        "2025-11-01": -14.8,
        "2025-11-15": -16.0,
    }

    RICE_VV_PROFILE: ClassVar[dict[str, float]] = {
        "2025-05-01": -10.2,
        "2025-05-15": -10.8,
        "2025-06-01": -12.1,
        "2025-06-15": -13.5,
        "2025-07-01": -14.2,
        "2025-07-15": -12.8,
        "2025-08-01": -11.5,
        "2025-08-15": -10.8,
        "2025-09-01": -9.5,
        "2025-09-15": -9.0,
        "2025-10-01": -8.5,
        "2025-10-15": -8.8,
        "2025-11-01": -9.5,
        "2025-11-15": -10.2,
    }

    def analyze(
        self,
        township_id: str,
        latitude: float,
        longitude: float,
        season: str,
        year: int,
    ) -> SARAnalysisResult:
        """Generate mock SAR analysis with realistic phenology."""
        time_series = self._build_time_series(latitude, longitude)
        signals = self._detect_phenology(time_series)

        detected_count = sum(1 for s in signals if s.detected)
        total_signals = len(signals)
        confidence = (
            detected_count / total_signals if total_signals > 0 else 0.0
        )
        rice_detected = detected_count >= SAR_CONFIDENCE_MIN_SIGNALS

        area_pct = 0.0
        if rice_detected:
            area_pct = min(confidence * 85.0, 95.0)

        summary = self._build_summary(
            township_id, rice_detected, confidence, area_pct, season
        )

        return SARAnalysisResult(
            township_id=township_id,
            analysis_date=date.today().isoformat(),
            season=season,
            time_series=time_series,
            phenology_signals=signals,
            rice_detected=rice_detected,
            rice_confidence=round(confidence, 4),
            estimated_area_pct=round(area_pct, 1),
            summary=summary,
        )

    def _build_time_series(
        self, latitude: float, longitude: float,
    ) -> list[SARTimePoint]:
        """Build mock SAR time series with location-based variation."""
        lat_offset = (latitude - 20.0) * 0.1
        lon_offset = (longitude - 96.0) * 0.05

        points: list[SARTimePoint] = []
        for date_str, vh in self.RICE_VH_PROFILE.items():
            vv = self.RICE_VV_PROFILE.get(date_str, vh + 5.0)

            adj_vh = vh + lat_offset + lon_offset
            adj_vv = vv + lat_offset * 0.5

            points.append(
                SARTimePoint(
                    date=date_str,
                    vh_db=round(adj_vh, 2),
                    vv_db=round(adj_vv, 2),
                    vh_vv_ratio=round(adj_vh - adj_vv, 2),
                )
            )

        return points

    def _detect_phenology(
        self, time_series: list[SARTimePoint],
    ) -> list[PhenologySignal]:
        """Detect rice phenological signals from SAR time series."""
        signals: list[PhenologySignal] = []

        flood_detected = any(
            p.vh_db < SAR_VH_FLOOD_THRESHOLD
            for p in time_series
            if "06" in p.date or "07" in p.date
        )
        signals.append(
            PhenologySignal(
                signal_type="flooding",
                detected=flood_detected,
                confidence=0.85 if flood_detected else 0.1,
                date_range="June-July",
                description="VH backscatter dip indicating paddy flooding",
            )
        )

        tillering_vh = [
            p.vh_db for p in time_series
            if "08" in p.date or "09" in p.date[:7]
        ]
        flood_vh = [
            p.vh_db for p in time_series
            if "06" in p.date or "07" in p.date
        ]
        vh_rise = False
        if tillering_vh and flood_vh:
            vh_rise = max(tillering_vh) > min(flood_vh) + 2.0

        signals.append(
            PhenologySignal(
                signal_type="tillering",
                detected=vh_rise,
                confidence=0.80 if vh_rise else 0.15,
                date_range="August-September",
                description="VH backscatter rise indicating crop tillering",
            )
        )

        heading_detected = any(
            p.vh_db > SAR_VH_VEGETATION_THRESHOLD
            for p in time_series
            if "10" in p.date[:7]
        )
        signals.append(
            PhenologySignal(
                signal_type="heading",
                detected=heading_detected,
                confidence=0.75 if heading_detected else 0.2,
                date_range="October",
                description="VH backscatter peak indicating crop heading/maturity",
            )
        )

        senescence_vh = [
            p.vh_db for p in time_series
            if "11" in p.date[:7]
        ]
        peak_vh = [
            p.vh_db for p in time_series
            if "10" in p.date[:7]
        ]
        decline = False
        if senescence_vh and peak_vh:
            decline = min(senescence_vh) < max(peak_vh) - 1.0

        signals.append(
            PhenologySignal(
                signal_type="senescence",
                detected=decline,
                confidence=0.70 if decline else 0.25,
                date_range="November",
                description="VH backscatter decline indicating harvest readiness",
            )
        )

        return signals

    def _build_summary(
        self,
        township_id: str,
        rice_detected: bool,
        confidence: float,
        area_pct: float,
        season: str,
    ) -> str:
        """Build human-readable analysis summary."""
        if rice_detected:
            return (
                f"Rice paddy cultivation detected in {township_id} for "
                f"{season} season with {confidence:.0%} confidence. "
                f"Estimated {area_pct:.1f}% of monitored area shows "
                f"rice phenological signatures."
            )
        return (
            f"Rice paddy signals insufficient in {township_id} for "
            f"{season} season (confidence: {confidence:.0%}). "
            f"Area may be fallow or planted with non-rice crops."
        )


class SARPipeline(BaseSARPipeline):
    """Real SAR pipeline using Google Earth Engine.

    Requires earthengine-api and service account credentials.
    Set GEE_SERVICE_ACCOUNT_KEY env var to enable.
    """

    def __init__(self) -> None:
        """Initialize GEE connection."""
        try:
            import ee  # type: ignore[import-untyped]
            ee.Initialize()
            self._ee = ee
            logger.info("GEE initialized successfully")
        except Exception as exc:
            logger.warning("GEE initialization failed: %s", exc)
            raise RuntimeError("GEE not available") from exc

    def analyze(
        self,
        township_id: str,
        latitude: float,
        longitude: float,
        season: str,
        year: int,
    ) -> SARAnalysisResult:
        """Run real SAR analysis via Google Earth Engine.

        Queries Sentinel-1 GRD collection for the specified location
        and time range, extracts VH/VV time series, and runs
        phenology detection.
        """
        ee = self._ee

        point = ee.Geometry.Point([longitude, latitude])
        buffer = point.buffer(5000)

        start_date = f"{year}-05-01"
        end_date = f"{year}-11-30"

        collection = (
            ee.ImageCollection("COPERNICUS/S1_GRD")
            .filterBounds(buffer)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH"))
            .filter(ee.Filter.eq("instrumentMode", "IW"))
            .select(["VH", "VV"])
        )

        def extract_means(image: object) -> object:
            """Extract mean VH/VV values over the buffer area."""
            means = image.reduceRegion(  # type: ignore[union-attr]
                reducer=ee.Reducer.mean(),
                geometry=buffer,
                scale=10,
            )
            return image.set(means).set("date", image.date().format("YYYY-MM-dd"))  # type: ignore[union-attr]

        results = collection.map(extract_means).getInfo()

        time_series: list[SARTimePoint] = []
        for feature in results.get("features", []):
            props = feature.get("properties", {})
            vh = props.get("VH", -20.0)
            vv = props.get("VV", -14.0)
            if vh is not None and vv is not None:
                time_series.append(
                    SARTimePoint(
                        date=props.get("date", ""),
                        vh_db=round(float(vh), 2),
                        vv_db=round(float(vv), 2),
                        vh_vv_ratio=round(float(vh) - float(vv), 2),
                    )
                )

        mock = MockSARPipeline()
        signals = mock._detect_phenology(time_series)

        detected_count = sum(1 for s in signals if s.detected)
        total_signals = len(signals)
        confidence = (
            detected_count / total_signals if total_signals > 0 else 0.0
        )
        rice_detected = detected_count >= SAR_CONFIDENCE_MIN_SIGNALS
        area_pct = min(confidence * 85.0, 95.0) if rice_detected else 0.0

        summary = mock._build_summary(
            township_id, rice_detected, confidence, area_pct, season
        )

        return SARAnalysisResult(
            township_id=township_id,
            analysis_date=date.today().isoformat(),
            season=season,
            time_series=time_series,
            phenology_signals=signals,
            rice_detected=rice_detected,
            rice_confidence=round(confidence, 4),
            estimated_area_pct=round(area_pct, 1),
            summary=summary,
        )
