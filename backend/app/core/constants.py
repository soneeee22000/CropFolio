"""Named constants used across the application."""

# Monte Carlo simulation
DEFAULT_NUM_SIMULATIONS = 1000
MAX_NUM_SIMULATIONS = 10000
CATASTROPHIC_LOSS_THRESHOLD = 0.5  # 50% income drop

# Portfolio optimization
MIN_CROP_WEIGHT = 0.0
MAX_CROP_WEIGHT = 1.0
WEIGHT_SUM_TOLERANCE = 1e-6
RISK_FREE_RATE = 0.0  # No risk-free asset in farming

# Climate risk thresholds
DROUGHT_RAINFALL_PERCENTILE = 20  # Below 20th percentile = drought
FLOOD_RAINFALL_PERCENTILE = 90  # Above 90th percentile = flood risk
TEMP_ANOMALY_WARNING_CELSIUS = 1.5

# Seasonal calendar (Myanmar)
MONSOON_SEASON_DAYS = 153
DRY_SEASON_DAYS = 212
DEFAULT_FORECAST_DAYS = 14

# Data constraints
MIN_CROPS_FOR_OPTIMIZATION = 2
MAX_CROPS_FOR_OPTIMIZATION = 10
STANDARD_DEVIATION_CAP = 3.0  # Cap Monte Carlo outliers at 3 std devs
