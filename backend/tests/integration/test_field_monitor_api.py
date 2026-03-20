"""Integration tests for Field Monitor API endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

AMARAPURA = "mdy_amarapura"


class TestFieldMonitorEndpoint:
    """Tests for POST /api/v1/field-monitor/monitor."""

    def test_valid_monitor_returns_200(self) -> None:
        """Valid township should return 200 with plots and alerts."""
        response = client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["township_id"] == AMARAPURA
        assert data["total_plots"] >= 5
        assert "plots" in data
        assert "alerts" in data

    def test_counts_sum_to_total(self) -> None:
        """Compliant + warning + deviation should equal total_plots."""
        response = client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        data = response.json()
        total = (
            data["compliant_count"] + data["warning_count"] + data["deviation_count"]
        )
        assert total == data["total_plots"]

    def test_compliance_rate_in_range(self) -> None:
        """Compliance rate should be between 0 and 1."""
        response = client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        data = response.json()
        assert 0.0 <= data["compliance_rate"] <= 1.0

    def test_invalid_township_returns_400(self) -> None:
        """Unknown township must return 400."""
        response = client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": "nonexistent_twp", "season": "monsoon", "year": 2025},
        )
        assert response.status_code == 400

    def test_malformed_township_id_returns_422(self) -> None:
        """Township ID with special chars must be rejected by validation."""
        response = client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": "'; DROP TABLE--", "season": "monsoon", "year": 2025},
        )
        assert response.status_code == 422

    def test_plots_have_observations(self) -> None:
        """Each plot should have observation time series."""
        response = client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        data = response.json()
        for plot in data["plots"]:
            assert len(plot["observations"]) > 0


class TestPlotDetailEndpoint:
    """Tests for GET /api/v1/field-monitor/plot/{township_id}/{plot_id}."""

    def test_valid_plot_returns_200(self) -> None:
        """Known plot should return 200 with time series."""
        client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        monitor_resp = client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        plot_id = monitor_resp.json()["plots"][0]["plot_id"]

        response = client.get(
            f"/api/v1/field-monitor/plot/{AMARAPURA}/{plot_id}",
        )
        assert response.status_code == 200
        data = response.json()
        assert data["plot_id"] == plot_id
        assert len(data["observations"]) > 0

    def test_invalid_plot_returns_404(self) -> None:
        """Unknown plot ID should return 404."""
        response = client.get(
            f"/api/v1/field-monitor/plot/{AMARAPURA}/nonexistent_plot",
        )
        assert response.status_code == 404


class TestAlertsEndpoint:
    """Tests for GET /api/v1/field-monitor/alerts/{township_id}."""

    def test_returns_alert_list(self) -> None:
        """Should return a list of alerts."""
        client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        response = client.get(
            f"/api/v1/field-monitor/alerts/{AMARAPURA}",
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_severity_filter(self) -> None:
        """Severity filter should narrow results."""
        client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        all_resp = client.get(
            f"/api/v1/field-monitor/alerts/{AMARAPURA}",
        )
        high_resp = client.get(
            f"/api/v1/field-monitor/alerts/{AMARAPURA}?severity=high",
        )
        all_alerts = all_resp.json()
        high_alerts = high_resp.json()

        assert len(high_alerts) <= len(all_alerts)
        for alert in high_alerts:
            assert alert["severity"] == "high"

    def test_invalid_severity_returns_422(self) -> None:
        """Invalid severity value must return 422."""
        client.post(
            "/api/v1/field-monitor/monitor",
            json={"township_id": AMARAPURA, "season": "monsoon", "year": 2025},
        )
        response = client.get(
            f"/api/v1/field-monitor/alerts/{AMARAPURA}?severity=invalid",
        )
        assert response.status_code == 422
