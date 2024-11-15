from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    AES_SECRET: str
    NODE_ID : str
    NODE_HOST : str
    NODE_PORT : int
    class Config:
        env_file = ".env"

settings = Settings()