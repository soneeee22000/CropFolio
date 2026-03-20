"""Field Monitor domain — mock plot generation, compliance scoring, and alerts.

Generates deterministic virtual plots for any township using seeded RNG.
Each plot gets SAR-like time series data, compliance scoring, and deviation
alerts. Designed for the distributor pitch demo: "Here's how you'd monitor
thousands of plots from space."

Swap to real database when field data arrives — the domain API stays the same.
"""

from __future__ import annotations

import hashlib
import logging
import math
import random
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from app.core.constants import (
    FIELD_MONITOR_COMPLIANCE_GREEN,
    FIELD_MONITOR_COMPLIANCE_YELLOW,
    FIELD_MONITOR_MAX_PLOTS,
    FIELD_MONITOR_MIN_PLOTS,
    FIELD_MONITOR_PLOT_AREA_MAX_HA,
    FIELD_MONITOR_PLOT_AREA_MIN_HA,
    FIELD_MONITOR_PLOT_RADIUS_M,
)

logger = logging.getLogger(__name__)


class ComplianceStatus(str, Enum):
    """Plot compliance status."""

    COMPLIANT = "compliant"
    WARNING = "warning"
    DEVIATION = "deviation"


class AlertSeverity(str, Enum):
    """Alert severity level."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class PlotLocation:
    """Geographic location of a monitored plot."""

    latitude: float
    longitude: float


@dataclass(frozen=True)
class PlotObservation:
    """A single SAR observation for a plot."""

    date: str
    observed_vh_db: float
    expected_vh_db: float


@dataclass(frozen=True)
class PlotAlert:
    """An alert generated from a plot deviation."""

    alert_id: str
    plot_id: str
    farmer_name: str
    alert_type: str
    severity: AlertSeverity
    message: str
    created_date: str


@dataclass(frozen=True)
class ComplianceInfo:
    """Compliance scoring breakdown for a plot."""

    status: ComplianceStatus
    score: float
    planting_detected: bool
    crop_match: bool
    phenology_match: float


@dataclass(frozen=True)
class MonitoredPlot:
    """A single monitored plot with full details."""

    plot_id: str
    farmer_name: str
    location: PlotLocation
    area_ha: float
    recommended_crop: str
    compliance: ComplianceInfo
    observations: list[PlotObservation]
    alerts: list[PlotAlert]


@dataclass(frozen=True)
class FieldMonitorSummary:
    """Summary of field monitoring for a township."""

    township_id: str
    season: str
    year: int
    total_plots: int
    compliant_count: int
    warning_count: int
    deviation_count: int
    compliance_rate: float
    total_area_ha: float
    active_alerts: int
    plots: list[MonitoredPlot]
    alerts: list[PlotAlert]


MYANMAR_FARMER_NAMES: list[str] = [
    "U Kyaw Win", "U Tin Aung", "U Zaw Min", "Daw Myint Myint",
    "U Aung Ko", "U Htun Oo", "Daw Khin Mar", "U Soe Lwin",
    "U Myo Thant", "U Thura", "Daw Ni Ni", "U Win Naing",
    "U Hla Tun", "Daw Aye Aye", "U Than Htay",
]

CROP_CHOICES: list[str] = [
    "rice", "black_gram", "sesame", "groundnut", "sunflower",
]

RICE_VH_EXPECTED: list[tuple[str, float]] = [
    ("2025-05-01", -16.5), ("2025-05-15", -17.2),
    ("2025-06-01", -18.8), ("2025-06-15", -20.1),
    ("2025-07-01", -21.3), ("2025-07-15", -19.5),
    ("2025-08-01", -17.8), ("2025-08-15", -16.2),
    ("2025-09-01", -14.5), ("2025-09-15", -13.8),
    ("2025-10-01", -12.9), ("2025-10-15", -13.2),
    ("2025-11-01", -14.8), ("2025-11-15", -16.0),
]


def _seed_from_township(township_id: str) -> int:
    """Derive deterministic seed from township ID."""
    digest = hashlib.sha256(township_id.encode()).hexdigest()
    return int(digest[:8], 16)


class MockPlotGenerator:
    """Generates deterministic mock plots around a township center."""

    def generate(
        self,
        township_id: str,
        center_lat: float,
        center_lon: float,
    ) -> list[MonitoredPlot]:
        """Generate 5-15 plots around the township center.

        Distribution: ~60% compliant, ~25% warning, ~15% deviation.
        Uses seeded RNG for rehearsal consistency.
        """
        seed = _seed_from_township(township_id)
        rng = random.Random(seed)

        plot_count = rng.randint(FIELD_MONITOR_MIN_PLOTS, FIELD_MONITOR_MAX_PLOTS)

        plots: list[MonitoredPlot] = []
        for idx in range(plot_count):
            plot_id = f"{township_id}_plot_{idx:03d}"
            farmer = MYANMAR_FARMER_NAMES[idx % len(MYANMAR_FARMER_NAMES)]
            crop = CROP_CHOICES[rng.randint(0, len(CROP_CHOICES) - 1)]

            location = self._scatter_location(
                rng, center_lat, center_lon,
            )
            area = round(
                rng.uniform(
                    FIELD_MONITOR_PLOT_AREA_MIN_HA,
                    FIELD_MONITOR_PLOT_AREA_MAX_HA,
                ),
                2,
            )

            roll = rng.random()
            if roll < 0.60:
                target_status = ComplianceStatus.COMPLIANT
            elif roll < 0.85:
                target_status = ComplianceStatus.WARNING
            else:
                target_status = ComplianceStatus.DEVIATION

            observations = self._build_observations(
                rng, target_status, location.latitude,
            )
            compliance = ComplianceEngine.score(target_status, rng)
            alerts = AlertRuleEngine.generate(
                plot_id, farmer, compliance, rng,
            )

            plots.append(
                MonitoredPlot(
                    plot_id=plot_id,
                    farmer_name=farmer,
                    location=location,
                    area_ha=area,
                    recommended_crop=crop,
                    compliance=compliance,
                    observations=observations,
                    alerts=alerts,
                )
            )

        return plots

    def _scatter_location(
        self,
        rng: random.Random,
        center_lat: float,
        center_lon: float,
    ) -> PlotLocation:
        """Scatter a plot within PLOT_RADIUS_M of the township center."""
        meters_per_deg_lat = 111_320.0
        meters_per_deg_lon = 111_320.0 * math.cos(math.radians(center_lat))

        offset_m = rng.uniform(200, FIELD_MONITOR_PLOT_RADIUS_M)
        angle = rng.uniform(0, 2 * math.pi)

        d_lat = (offset_m * math.sin(angle)) / meters_per_deg_lat
        d_lon = (offset_m * math.cos(angle)) / meters_per_deg_lon

        return PlotLocation(
            latitude=round(center_lat + d_lat, 6),
            longitude=round(center_lon + d_lon, 6),
        )

    def _build_observations(
        self,
        rng: random.Random,
        target_status: ComplianceStatus,
        latitude: float,
    ) -> list[PlotObservation]:
        """Build SAR observations with deviation based on compliance target."""
        lat_offset = (latitude - 20.0) * 0.1

        noise_range = {
            ComplianceStatus.COMPLIANT: 1.0,
            ComplianceStatus.WARNING: 3.0,
            ComplianceStatus.DEVIATION: 6.0,
        }
        noise = noise_range[target_status]

        observations: list[PlotObservation] = []
        for date_str, expected_vh in RICE_VH_EXPECTED:
            adj_expected = expected_vh + lat_offset
            observed = adj_expected + rng.uniform(-noise, noise)
            observations.append(
                PlotObservation(
                    date=date_str,
                    observed_vh_db=round(observed, 2),
                    expected_vh_db=round(adj_expected, 2),
                )
            )

        return observations


class ComplianceEngine:
    """Scores plot compliance from detection signals."""

    @staticmethod
    def score(
        target_status: ComplianceStatus,
        rng: random.Random,
    ) -> ComplianceInfo:
        """Generate compliance info matching the target status.

        Green: score >= 0.8, all checks pass.
        Yellow: score 0.5-0.8, partial matches.
        Red: score < 0.5, planting or crop mismatch.
        """
        if target_status == ComplianceStatus.COMPLIANT:
            score = rng.uniform(
                FIELD_MONITOR_COMPLIANCE_GREEN, 1.0,
            )
            return ComplianceInfo(
                status=ComplianceStatus.COMPLIANT,
                score=round(score, 3),
                planting_detected=True,
                crop_match=True,
                phenology_match=round(rng.uniform(0.8, 1.0), 3),
            )

        if target_status == ComplianceStatus.WARNING:
            score = rng.uniform(
                FIELD_MONITOR_COMPLIANCE_YELLOW,
                FIELD_MONITOR_COMPLIANCE_GREEN - 0.01,
            )
            return ComplianceInfo(
                status=ComplianceStatus.WARNING,
                score=round(score, 3),
                planting_detected=True,
                crop_match=rng.choice([True, False]),
                phenology_match=round(rng.uniform(0.4, 0.7), 3),
            )

        score = rng.uniform(0.1, FIELD_MONITOR_COMPLIANCE_YELLOW - 0.01)
        return ComplianceInfo(
            status=ComplianceStatus.DEVIATION,
            score=round(score, 3),
            planting_detected=rng.choice([True, False]),
            crop_match=False,
            phenology_match=round(rng.uniform(0.0, 0.4), 3),
        )


class AlertRuleEngine:
    """Generates alerts from compliance deviations."""

    ALERT_TEMPLATES: ClassVar[list[tuple[str, AlertSeverity, str]]] = [
        (
            "no_planting",
            AlertSeverity.CRITICAL,
            "No planting activity detected despite recommendation",
        ),
        (
            "crop_mismatch",
            AlertSeverity.HIGH,
            "Detected crop does not match recommendation",
        ),
        (
            "delayed_planting",
            AlertSeverity.MEDIUM,
            "Planting detected but significantly delayed from schedule",
        ),
        (
            "phenology_deviation",
            AlertSeverity.LOW,
            "Growth pattern deviates from expected phenology curve",
        ),
    ]

    @staticmethod
    def generate(
        plot_id: str,
        farmer_name: str,
        compliance: ComplianceInfo,
        rng: random.Random,
    ) -> list[PlotAlert]:
        """Generate alerts based on compliance flags."""
        if compliance.status == ComplianceStatus.COMPLIANT:
            return []

        alerts: list[PlotAlert] = []
        today = "2025-10-15"

        if not compliance.planting_detected:
            alerts.append(
                PlotAlert(
                    alert_id=f"{plot_id}_alert_no_planting",
                    plot_id=plot_id,
                    farmer_name=farmer_name,
                    alert_type="no_planting",
                    severity=AlertSeverity.CRITICAL,
                    message="No planting activity detected despite recommendation",
                    created_date=today,
                )
            )

        if not compliance.crop_match:
            alerts.append(
                PlotAlert(
                    alert_id=f"{plot_id}_alert_crop_mismatch",
                    plot_id=plot_id,
                    farmer_name=farmer_name,
                    alert_type="crop_mismatch",
                    severity=AlertSeverity.HIGH,
                    message="Detected crop does not match recommendation",
                    created_date=today,
                )
            )

        if compliance.phenology_match < 0.5:
            alerts.append(
                PlotAlert(
                    alert_id=f"{plot_id}_alert_phenology",
                    plot_id=plot_id,
                    farmer_name=farmer_name,
                    alert_type="phenology_deviation",
                    severity=AlertSeverity.MEDIUM,
                    message="Growth pattern deviates from expected phenology curve",
                    created_date=today,
                )
            )

        if compliance.planting_detected and compliance.phenology_match < 0.6:
            delayed = rng.random() < 0.4
            if delayed:
                alerts.append(
                    PlotAlert(
                        alert_id=f"{plot_id}_alert_delayed",
                        plot_id=plot_id,
                        farmer_name=farmer_name,
                        alert_type="delayed_planting",
                        severity=AlertSeverity.LOW,
                        message="Planting detected but significantly delayed",
                        created_date=today,
                    )
                )

        return alerts
