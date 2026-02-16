from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    HOST: str = "127.0.0.1"
    PORT: int = 8008
    DATABASE_URL: str = "sqlite:///./aiops.db"
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "mistral"
    OLLAMA_TIMEOUT: int = 120
    RETENTION_MAX_EVENTS: int = 50000
    RETENTION_MAX_AGE_DAYS: int = 30
    RETENTION_SWEEP_INTERVAL_MINUTES: int = 60
    CLUSTER_WINDOW_MINUTES: int = 5
    CLUSTER_MAX_EVENTS: int = 200
    CLUSTER_MAX_SAMPLES: int = 10
    SUMMARY_DEBOUNCE_SECONDS: float = 30.0
    SUMMARY_CEILING_SECONDS: float = 120.0
    SUMMARY_CONTEXT_WINDOW_MINUTES: int = 15

    class Config:
        env_prefix = "AIOPS_"
        env_file = ".env"


settings = Settings()
