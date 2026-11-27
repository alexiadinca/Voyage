from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Configuration loaded from environment variables / backend/.env."""

    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Supabase (server-side only – never expose the service role key to the browser)
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""
    database_url: str = ""

    # OpenAI (assistant)
    openai_api_key: str = ""
    openai_model: str = ""

    # External data services
    open_meteo_base_url: str = "https://api.open-meteo.com/v1"
    overpass_api_url: str = "https://overpass-api.de/api/interpreter"
    weather_rain_threshold: int = 60

    # ML
    model_artifact_path: str = "../ml/artifacts/destination_ranker.joblib"


settings = Settings()
