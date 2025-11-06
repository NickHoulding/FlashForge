from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
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
