from pydantic import BeforeValidator
from pydantic_settings import BaseSettings
from typing import Annotated, Optional, Any
import json

def _parse_cors(v: Any) -> list[str]:
    if isinstance(v, str):
        # 支持 "*" 或直接逗号分隔的域名字符串
        if v.strip() == "*":
            return ["*"]
        try:
            return json.loads(v)
        except (json.JSONDecodeError, TypeError):
            # 逗号分隔：https://a.com,https://b.com
            return [s.strip() for s in v.split(",") if s.strip()]
    return v

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

    # CORS：支持环境变量传 "*" 或 JSON 数组
    CORS_ORIGINS: Annotated[list[str], BeforeValidator(_parse_cors)] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
    ]

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
