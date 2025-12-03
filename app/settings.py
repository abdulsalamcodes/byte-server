from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
