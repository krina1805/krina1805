from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Healthcare Education API"
    api_prefix: str = ""
    environment: str = "development"
    cors_origins: str = "*"
    rate_limit_per_minute: int = 60
    safety_block_message: str = (
        "Your query may contain unsafe content. This service provides general health education only. "
        "If you are in immediate danger, call emergency services right away."
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
