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

# Copula tail risk engine
COPULA_MIN_OBSERVATIONS = 4  # Minimum return observations for KDE fitting
DEFAULT_CLAYTON_THETA = 0.5  # Default Clayton theta when insufficient data
CLAYTON_DROUGHT_SCALE_FACTOR = 2.0  # Drought prob multiplier for tail dependence
GAUSSIAN_COPULA_REGULARIZATION = 1e-6  # Tikhonov regularization for copula corr

# Bayesian Belief Network
BBN_MAX_NODES = 20  # Maximum DAG nodes for VariableElimination efficiency
BBN_DEFAULT_PRIOR_STRENGTH = 10  # Dirichlet prior pseudo-count
BBN_YIELD_CATEGORIES = 3  # low / medium / high discretization
BBN_RAINFALL_CATEGORIES = 3  # low / normal / high
BBN_SOIL_CATEGORIES = 3  # poor / moderate / good

# Fertilizer optimizer
FERT_OPT_MAX_COST_MMK = 500000  # Maximum fertilizer budget per hectare (MMK)
FERT_OPT_MIN_NP_RATIO = 2.0  # Minimum N:P ratio (Liebig's law)
FERT_OPT_MAX_NP_RATIO = 4.0  # Maximum N:P ratio
FERT_OPT_ZINC_PH_THRESHOLD = 7.0  # pH above which Zn deficiency risk increases
FERT_OPT_ZINC_RATE_KG_HA = 25  # ZnSO4 application rate for deficient soils

# SAR pipeline
SAR_VH_FLOOD_THRESHOLD = -18.0  # dB, VH below this indicates flooding
SAR_VH_VEGETATION_THRESHOLD = -14.0  # dB, VH above this indicates vegetation
SAR_CONFIDENCE_MIN_SIGNALS = 3  # Minimum phenological signals for confidence
SAR_JOB_TIMEOUT_SECONDS = 300  # Maximum SAR analysis duration
