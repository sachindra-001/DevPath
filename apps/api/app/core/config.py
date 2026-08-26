from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "CPGS API"
    app_version: str = "0.1.0"
    log_level: str = "INFO"
    debug: bool = False

    # Database
    database_url: str = "postgresql+psycopg://cpgs:cpgs_dev_password@localhost:5432/cpgs"

    # Auth (DESIGN.md §23)
    jwt_secret: str = "dev-only-change-me-to-a-secure-random-secret-key-32-chars"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    cookie_secure: bool = False
    cookie_samesite: str = "lax"

    # First admin seed (FR-04)
    admin_email: str = "admin@cpgs.local"
    admin_password: str = "ChangeMeAdmin!2026"
    admin_name: str = "Platform Admin"

    # CORS
    cors_origins: str = "http://localhost:3000"

    # External AI services (P5/P6)
    openai_api_key: str = ""
    tavily_api_key: str = ""

    # Pipeline tunables (DESIGN.md §11.3)
    max_candidates_per_run: int = 30
    max_evaluations_per_run: int = 18
    eval_batch_size: int = 4
    dedup_cosine_threshold: float = 0.92
    run_concurrency: int = 2
    llm_monthly_budget_usd: float = 50.0
    disable_ai_pipeline: bool = False

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
