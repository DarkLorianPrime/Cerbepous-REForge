from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DATABASE: str

    TG_TOKEN: str

settings = Settings()