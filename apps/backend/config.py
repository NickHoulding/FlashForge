from dotenv import load_dotenv
from typing import List
import secrets
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)

class Settings:
    """Authentication/Database configuration settings"""
    ALLOWED_JWT_ALGORITHMS: List[str] = ["HS256", "HS384", "HS512"]

    # Database
    db_host: str = os.getenv("DB_HOST", "")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_user: str = os.getenv("DB_USER", "")
    db_pass: str = os.getenv("DB_PASS", "")
    db_name: str = os.getenv("DB_NAME", "")

    # JWT Configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    def __init__(self) -> None:
        self._validate_jwt_config()
        self._validate_db_config()

    def _validate_jwt_config(self) -> None:
        """Validate JWT configuration"""
        if not self.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY must be set in environment variables")
        
        if len(self.JWT_SECRET_KEY) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long")
        
        if self.JWT_ALGORITHM not in self.ALLOWED_JWT_ALGORITHMS:
            raise ValueError(f"JWT_ALGORITHM must be one of {self.ALLOWED_JWT_ALGORITHMS}")
        
        if self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
            raise ValueError("JWT_ACCESS_TOKEN_EXPIRE_MINUTES must be greater than 0")
        
        if self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES > 60 * 24:
            logger.warning(f"Warning: JWT token expires in {self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES} minutes (>24h)")

    def _validate_db_config(self) -> None:
        missing_vars = []

        if not self.db_host:
            missing_vars.append("DB_HOST")
        if not self.db_user:
            missing_vars.append("DB_USER")
        if not self.db_pass:
            missing_vars.append("DB_PASS")
        if not self.db_name:
            missing_vars.append("DB_NAME")

        if missing_vars:
            raise ValueError(f"Missing required database environment variables: {', '.join(missing_vars)}")
        
        if not (1 <= self.db_port <= 65535):
            raise ValueError(f"DB_PORT must be between 1 and 65535, got: {self.db_port}")
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @staticmethod
    def generate_secret_key() -> str:
        """Generate a secure random secret key"""
        return secrets.token_urlsafe(32)

settings = Settings()
