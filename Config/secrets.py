from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    AES_SECRET: str
    class Config:
        env_file = ".env"

settings = Settings()