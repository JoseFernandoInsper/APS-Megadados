from pydantic import BaseSettings

class Settings(BaseSettings):
    password: str = "Awesome API"
    admin: str

    class Config:
        env_file = ".env"

