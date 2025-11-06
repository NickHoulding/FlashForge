from fastapi.security import HTTPBearer
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from exceptions import handle_exception
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any
import logging
import ollama
import json
import sys
from schemas import StudySet
from config import Settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flashforge_backend.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
security = HTTPBearer()

app = FastAPI(
    title="FlashForge API", 
    version='1.0.0',
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allow_headers=['Content-Type', 'Authorization']
)

class MessageRequest(BaseModel):
    """  """
    model_name: str
    user_message: str

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

@app.post("/sendmessage")
async def send_message(request: MessageRequest) -> Dict[str, Any]:
    """
    Send message endpoint

    Returns:
        The AI Response to the user's message.
    """
    response = ollama.chat(
        model=request.model_name,
        messages=[
            {
                'role': 'system',
                'content': Settings.AI_SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': request.user_message
            }
        ],
        format=StudySet.model_json_schema(),
        stream=False
    )

    return {
        'message': {
            'content': response['message']['content']
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
