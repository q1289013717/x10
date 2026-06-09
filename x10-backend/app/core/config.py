from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import Any
import json

CORS_DEFAULT = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
]


class Settings(BaseSettings):
    PROJECT_NAME: str = "X10增长引擎 API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "X10增长引擎后端服务 - Vue3 + Python + PostgreSQL"

    SECRET_KEY: str = "x10-engine-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    DATABASE_URL: str = "sqlite:///./x10.db"

    # CORS：环境变量可以是 "*"、JSON数组字符串、或逗号分隔字符串
    CORS_ORIGINS: list[str] = CORS_DEFAULT

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            s = v.strip()
            if s == "*":
                return ["*"]
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, TypeError):
                pass
            # 逗号分隔
            return [x.strip() for x in s.split(",") if x.strip()]
        return v

    @property
    def is_postgres(self) -> bool:
        return self.DATABASE_URL.startswith("postgresql")

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
