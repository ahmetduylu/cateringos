from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://catering_user:catering_pass_2026@db:5432/localcateringos"
    SECRET_KEY: str = "supersecret-jwt-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    APIFY_API_TOKEN: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
