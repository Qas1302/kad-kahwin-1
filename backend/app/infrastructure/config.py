from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="WEDDING_", env_file=".env", extra="ignore")

    app_name: str = "Wedding RSVP API"
    database_url: SecretStr = SecretStr(f"sqlite:///{BACKEND_ROOT / 'data' / 'wedding.db'}")
    # Create missing tables on startup. Handy locally; turn off when the schema is
    # managed with the SQL files in migrations/ (e.g. on Supabase).
    auto_create_schema: bool = True
    event_file: Path = BACKEND_ROOT / "data" / "event.json"
    cors_origins: str = "http://localhost:5173"
    # Optional regex for extra allowed origins, e.g. Vercel preview URLs.
    cors_origin_regex: str | None = None
    admin_api_key: SecretStr | None = None

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
