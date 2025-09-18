from exceptions import (
    UserNotFoundException, InvalidCredentialsException, 
    TokenException
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy import select
from typing import Optional
from config import settings
from database import get_db
from models import User
import bcrypt

security = HTTPBearer()

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt
    
    Args:
        password (str): The plain text password to hash.
    Returns:
        str: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    
    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to compare against.
    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token

    Args:
        data (dict): The data to encode in the token.
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({ "exp": expire })
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt

def verify_token(token: str):
    """
    Verify JWT token

    Args:
        token (str): The JWT token to verify.
    Returns:
        dict: The decoded token payload if valid, None otherwise.
    Raises:
        JWTError: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload

    except JWTError:
        return None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    """
    Get current user from JWT token
    
    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials.
        db (AsyncSession): The database session.
    Returns:
        User: The authenticated user.
    Raises:
        InvalidCredentialsException: If the token is invalid (401 Unauthorized).
        TokenException: If there are issues processing the token (401 Unauthorized).
        UserNotFoundException: If the user does not exist (401 Unauthorized).
    """
    try:
        payload = jwt.decode(credentials.credentials, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str | None = payload.get("userId")

        if not user_id:
            raise InvalidCredentialsException("Invalid credentials", 401)
    except JWTError:
        raise TokenException("Error processing JWT token", 401)
    
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFoundException("User does not exist", 401)
    
    return user
