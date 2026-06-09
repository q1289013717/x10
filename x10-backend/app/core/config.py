from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "X10增长引擎 API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "X10增长引擎后端服务 - Vue3 + Python + PostgreSQL"

    SECRET_KEY: str = "x10-engine-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    DATABASE_URL: str = "sqlite:///./x10.db"

    # 是否使用 PostgreSQL（生产环境自动检测）
    @property
    def is_postgres(self) -> bool:
        return self.DATABASE_URL.startswith("postgresql")

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://localhost:5174", "http://localhost:5175", "http://localhost:5176"]

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
