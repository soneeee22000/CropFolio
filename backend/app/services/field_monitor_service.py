"""Field Monitor service — orchestrates plot generation and caching.

Synchronous (no polling) since mock data is CPU-cheap.
Caches results per (township_id, season, year) for consistency.
"""

from __future__ import annotations

import logging
from collections import OrderedDict
from functools import lru_cache

from app.domain.field_monitor import (
    AlertSeverity,
    FieldMonitorSummary,
    MockPlotGenerator,
    MonitoredPlot,
    PlotAlert,
)
from app.services.township_service import TownshipService, get_township_service

logger = logging.getLogger(__name__)


CACHE_MAX_SIZE = 100


class FieldMonitorService:
    """Manages field monitoring with plot generation and caching."""

    def __init__(
        self,
        township_service: TownshipService | None = None,
    ) -> None:
        """Initialize with dependencies."""
        self._township_service = township_service or get_township_service()
        self._generator = MockPlotGenerator()
        self._cache: OrderedDict[str, FieldMonitorSummary] = OrderedDict()

    def get_township_monitor(
        self,
        township_id: str,
        season: str = "monsoon",
        year: int = 2025,
    ) -> FieldMonitorSummary:
        """Get full monitoring summary for a township.

        Args:
            township_id: Township to monitor.
            season: Growing season.
            year: Monitoring year.

        Returns:
            FieldMonitorSummary with plots, alerts, and KPIs.

        Raises:
            ValueError: If township not found.
        """
        cache_key = f"{township_id}:{season}:{year}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        township = self._township_service.get_by_id(township_id)
        if township is None:
            raise ValueError("Unknown township")

        plots = self._generator.generate(
            township_id=township_id,
            center_lat=township["latitude"],
            center_lon=township["longitude"],
        )

        all_alerts: list[PlotAlert] = []
        for plot in plots:
            all_alerts.extend(plot.alerts)

        compliant = sum(
            1 for p in plots if p.compliance.status.value == "compliant"
        )
        warning = sum(
            1 for p in plots if p.compliance.status.value == "warning"
        )
        deviation = sum(
            1 for p in plots if p.compliance.status.value == "deviation"
        )
        total = len(plots)
        total_area = round(sum(p.area_ha for p in plots), 2)
        compliance_rate = round(compliant / total, 3) if total > 0 else 0.0

        summary = FieldMonitorSummary(
            township_id=township_id,
            season=season,
            year=year,
            total_plots=total,
            compliant_count=compliant,
            warning_count=warning,
            deviation_count=deviation,
            compliance_rate=compliance_rate,
            total_area_ha=total_area,
            active_alerts=len(all_alerts),
            plots=plots,
            alerts=all_alerts,
        )

        self._cache[cache_key] = summary
        if len(self._cache) > CACHE_MAX_SIZE:
            self._cache.popitem(last=False)
        logger.info(
            "Field monitor: %s — %d plots, %.0f%% compliant, %d alerts",
            township_id, total, compliance_rate * 100, len(all_alerts),
        )
        return summary

    def get_plot_detail(
        self,
        township_id: str,
        plot_id: str,
    ) -> MonitoredPlot | None:
        """Get detailed data for a specific plot.

        Searches cached summaries first.
        """
        for summary in self._cache.values():
            if summary.township_id == township_id:
                for plot in summary.plots:
                    if plot.plot_id == plot_id:
                        return plot
        return None

    def get_alerts(
        self,
        township_id: str,
        severity: str | None = None,
    ) -> list[PlotAlert]:
        """Get alerts for a township, optionally filtered by severity.

        Args:
            township_id: Township to query alerts for.
            severity: Optional severity filter (low/medium/high/critical).

        Returns:
            List of PlotAlert objects.
        """
        alerts: list[PlotAlert] = []
        for summary in self._cache.values():
            if summary.township_id == township_id:
                alerts.extend(summary.alerts)

        if severity is not None:
            sev = AlertSeverity(severity)
            alerts = [a for a in alerts if a.severity == sev]

        return alerts


@lru_cache(maxsize=1)
def get_field_monitor_service() -> FieldMonitorService:
    """Return singleton FieldMonitorService instance."""
    return FieldMonitorService()
