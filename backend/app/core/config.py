"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # External APIs
    nasa_power_base_url: str = "https://power.larc.nasa.gov/api/temporal/"
    open_meteo_base_url: str = "https://api.open-meteo.com/v1/"
    gemini_api_key: str = ""

    # Server
    cors_origins: str = "http://localhost:5173,http://localhost:4173"
    port: int = 8000
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql+asyncpg://cropfolio:cropfolio@localhost:5432/cropfolio"

    # Authentication
    jwt_secret_key: str = "CHANGE-ME-IN-PRODUCTION"
    jwt_algorithm: str = "HS256"
    jwt_farmer_expiry_hours: int = 24
    jwt_distributor_expiry_hours: int = 8
    otp_ttl_seconds: int = 300

    model_config = {
        "env_file": (".env", "../.env.local"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
