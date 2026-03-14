"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    nasa_power_base_url: str = "https://power.larc.nasa.gov/api/temporal/"
    open_meteo_base_url: str = "https://api.open-meteo.com/v1/"
    gemini_api_key: str = ""
    cors_origins: str = "http://localhost:5173,http://localhost:4173"
    port: int = 8000
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
