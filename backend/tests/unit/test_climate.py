"""Tests for climate risk assessment engine."""

from app.domain.climate import ClimateRiskProfile, assess_climate_risk


class TestClimateRiskAssessment:
    """Tests for climate risk computation."""

    def test_low_rainfall_increases_drought_risk(self) -> None:
        """Below-average rainfall should increase drought probability."""
        historical = [100.0, 150.0, 200.0, 250.0, 300.0] * 4  # 20 years
        result = assess_climate_risk(
            township_id="t001",
            township_name="Magway",
            season="dry",
            historical_rainfall=historical,
            forecast_rainfall_mm=80.0,
            forecast_temp_anomaly=0.0,
        )
        assert result.drought_probability > 0.5

    def test_high_rainfall_increases_flood_risk(self) -> None:
        """Above-average rainfall should increase flood probability."""
        historical = [100.0, 150.0, 200.0, 250.0, 300.0] * 4
        result = assess_climate_risk(
            township_id="t002",
            township_name="Bago",
            season="monsoon",
            historical_rainfall=historical,
            forecast_rainfall_mm=350.0,
            forecast_temp_anomaly=0.0,
        )
        assert result.flood_probability > 0.3

    def test_normal_rainfall_low_risk(self) -> None:
        """Near-average rainfall should result in low or moderate risk."""
        historical = [180.0, 190.0, 195.0, 200.0, 205.0, 210.0, 220.0] * 3
        result = assess_climate_risk(
            township_id="t003",
            township_name="Mandalay",
            season="monsoon",
            historical_rainfall=historical,
            forecast_rainfall_mm=200.0,
            forecast_temp_anomaly=0.0,
        )
        assert result.risk_level in ("low", "moderate")

    def test_temp_anomaly_increases_drought_risk(self) -> None:
        """High temperature anomaly should amplify drought risk."""
        historical = [200.0] * 20
        no_anomaly = assess_climate_risk(
            township_id="t004",
            township_name="Sagaing",
            season="dry",
            historical_rainfall=historical,
            forecast_rainfall_mm=150.0,
            forecast_temp_anomaly=0.5,
        )
        high_anomaly = assess_climate_risk(
            township_id="t004",
            township_name="Sagaing",
            season="dry",
            historical_rainfall=historical,
            forecast_rainfall_mm=150.0,
            forecast_temp_anomaly=2.0,
        )
        assert high_anomaly.drought_probability >= no_anomaly.drought_probability

    def test_empty_historical_returns_default(self) -> None:
        """Missing historical data should return default risk profile."""
        result = assess_climate_risk(
            township_id="t005",
            township_name="Unknown",
            season="monsoon",
            historical_rainfall=[],
            forecast_rainfall_mm=200.0,
            forecast_temp_anomaly=0.0,
        )
        assert result.confidence == 0.3
        assert result.risk_level == "moderate"

    def test_result_type(self) -> None:
        """Should return ClimateRiskProfile."""
        result = assess_climate_risk(
            township_id="t001",
            township_name="Magway",
            season="dry",
            historical_rainfall=[200.0] * 10,
            forecast_rainfall_mm=180.0,
            forecast_temp_anomaly=0.5,
        )
        assert isinstance(result, ClimateRiskProfile)

    def test_probabilities_bounded(self) -> None:
        """All probabilities should be between 0 and 1."""
        result = assess_climate_risk(
            township_id="t001",
            township_name="Test",
            season="monsoon",
            historical_rainfall=[100.0, 500.0] * 10,
            forecast_rainfall_mm=50.0,
            forecast_temp_anomaly=3.0,
        )
        assert 0.0 <= result.drought_probability <= 1.0
        assert 0.0 <= result.flood_probability <= 1.0
        assert 0.0 <= result.confidence <= 1.0

    def test_risk_level_classification(self) -> None:
        """Critical risk level for extreme conditions."""
        historical = [200.0] * 20
        result = assess_climate_risk(
            township_id="t006",
            township_name="Ayeyarwady",
            season="monsoon",
            historical_rainfall=historical,
            forecast_rainfall_mm=50.0,
            forecast_temp_anomaly=2.5,
        )
        assert result.risk_level in ("high", "critical")
