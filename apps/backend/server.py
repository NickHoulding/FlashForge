from auth import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import HTTPBearer
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from database import get_db, init_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from exceptions import handle_exception
from pydantic import BaseModel
from sqlalchemy import select
from datetime import datetime
from typing import Dict
from models import User
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flashforge_backend.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting up FlashForge API...")
        await init_db()
        logger.info("Database initialized successfully")
        yield
        logger.info("Shutting down FlashForge API...")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

app = FastAPI(
    title="FlashForge API", 
    version='1.0.0',
    lifespan=lifespan
)
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['Content-Type', 'Authorization']
)

class UserCreate(BaseModel):
    """Structure of user creation and login requests"""
    username: str
    password: str

class UserResponse(BaseModel):
    """Structure of user data in responses"""
    user_id: str
    username: str

class Token(BaseModel):
    """Structure of the authentication token response"""
    token: str

@app.exception_handler(Exception)
async def global_error_handler(req: Request, exc: Exception):
    """Route to call custom error handling functionality"""
    response_data, status_code = handle_exception(exc)
    return JSONResponse(
        content=response_data,
        status_code=status_code
    )

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint
    
    Returns:
        The health status of the application.
    """
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> Token:
    """
    Register a new user
    
    Args:
        user_data (UserCreate): The user data for registration.
        db (AsyncSession): The database session.
    Returns:
        Token: The authentication token for the newly registered user.
    Raises:
        HTTPException:
            1. If the request data is invalid (400 Bad Request).
            2. If the username already exists (409 Conflict).
            3. If there is a server error during registration (500 Internal Server Error).
    """
    logger.info(f"Registration attempt for username: {user_data.username}")
    
    if not user_data.username or not user_data.password:
        logger.warning(f"Registration failed: Missing username or password for user: {user_data.username}")
        raise HTTPException(
            status_code=400,
            detail="Username and password are required"
        )

    try:
        result = await db.execute(
            select(User).where(User.username == user_data.username)
        )
        if result.scalar_one_or_none():
            logger.warning(f"Registration failed: Username already exists: {user_data.username}")
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )
        
        hashed_password = hash_password(user_data.password)
        user = User(
            username=user_data.username, 
            password_hash=hashed_password
        )
        db.add(user)

        await db.commit()
        await db.refresh(user)
        
        logger.info(f"User registered successfully: {user_data.username} (ID: {user.user_id})")
        token = create_access_token({"userId": str(user.user_id)})
        return Token(token=token)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error for user {user_data.username}: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Server error during registration"
        )

@app.post('/api/login', response_model=Token)
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> Token:
    """
    Authenticate a user and provide an access token

    Args:
        user_data (UserCreate): The user data for login.
        db (AsyncSession): The database session.
    Returns:
        Token: The authentication token for the logged-in user.
    Raises:
        HTTPException:
            1. If the request data is invalid (400 Bad Request).
            2. If the credentials are invalid (401 Unauthorized).
            3. If there is a server error during login (500 Internal Server Error).
    """
    logger.info(f"Login attempt for username: {user_data.username}")
    
    if not user_data.username or not user_data.password:
        logger.warning(f"Login failed: Missing username or password for user: {user_data.username}")
        raise HTTPException(
            status_code=400,
            detail="Username and password are required"
        )
    
    try:
        result = await db.execute(select(User).where(User.username == user_data.username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(user_data.password, user.password_hash):
            logger.warning(f"Login failed: Invalid credentials for user: {user_data.username}")
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )
        
        user.last_login = datetime.utcnow()
        await db.commit()

        logger.info(f"User logged in successfully: {user_data.username} (ID: {user.user_id})")
        token = create_access_token({"userId": str(user.user_id)})
        return Token(token=token)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for user {user_data.username}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Server error during login"
        )
    
@app.get("/api/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)) -> UserResponse:
    """
    Retrieve the profile of the currently authenticated user

    Args:
        current_user (User): The currently authenticated user.
    Returns:
        UserResponse: The profile information of the user.
    """
    logger.info(f"Profile request for user: {current_user.username} (ID: {current_user.user_id})")
    return UserResponse(
        user_id=str(current_user.user_id), 
        username=current_user.username
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
