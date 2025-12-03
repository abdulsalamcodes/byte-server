from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OLLAMA_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
