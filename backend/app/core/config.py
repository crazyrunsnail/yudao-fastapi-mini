from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API 配置
    API_V1_STR: str = "/admin-api"
    PROJECT_NAME: str = "yudao-fastapi-mini"
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # 数据库配置
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "yudao_fastapi"
    POSTGRES_PASSWORD: str = "Fast_api@123"
    POSTGRES_DB: str = "yudao_fastapi"
    POSTGRES_PORT: str = "5432"
    
    @property
    def ASYNC_DATABASE_URI(self) -> str:
        import urllib.parse
        password = urllib.parse.quote_plus(self.POSTGRES_PASSWORD)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{password}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis 配置
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    
    # 安全配置
    SECRET_KEY: str = "super-secret-key-change-it-in-production"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 1800  # 30 分钟
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 2592000  # 30 天
    
    class Config:
        case_sensitive = True

settings = Settings()
