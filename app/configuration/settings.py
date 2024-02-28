from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    db_url_test: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
