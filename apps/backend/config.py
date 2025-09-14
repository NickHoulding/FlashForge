from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Authentication/Database configuration settings"""
    # Database
    db_host: str = "localhost"
    db_port: int = 3002
    db_user: str = "pguser"
    db_pass: str = "pgpass"
    db_name: str = "flashforgedb"

    # JWT
    jwt_sec: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
