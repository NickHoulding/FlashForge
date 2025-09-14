from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy import select
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

def create_access_token(data: dict) -> str:
    """
    Create JWT access token

    Args:
        data (dict): The data to encode in the token.
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({ "exp": expire })
    return jwt.encode(
        to_encode, 
        settings.jwt_sec, 
        algorithm=settings.algorithm
    )

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    """
    Get current user from JWT token
    
    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP authorization credentials.
        db (AsyncSession): The database session.
    Returns:
        User: The authenticated user.
    Raises:
        HTTPException: 
            - If the credentials are invalid.
            - If the user is not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_sec, algorithms=[settings.algorithm])
        user_id: str | None = payload.get("userId")

        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise credentials_exception
    
    return user
