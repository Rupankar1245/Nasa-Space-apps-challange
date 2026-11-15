from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CrewPulse API"
    database_url: str = "postgresql+psycopg://crewpulse:crewpulse@localhost:5432/crewpulse"
    jwt_secret: str = "development-only-change-me"
    jwt_expire_minutes: int = 60
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
