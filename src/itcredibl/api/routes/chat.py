from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import logging
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/v1", tags=["chat"])
logger = logging.getLogger(__name__)

# Simple authentication function
# Change the header parameter name to match what the frontend sends

async def verify_api_key(api_key: str = Header(..., alias="X-API-Key")):
    expected_key = os.getenv("ITCREDIBL_API_KEY", "itcr_")
    if api_key != expected_key:
        logger.warning(f"Invalid API key attempt: {api_key}")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    user_id: str = Field(...)
    department: str = Field(...)

class ChatResponse(BaseModel):
    message: str
    is_blocked: bool
    block_reason: Optional[str] = None
    policy_violations: List[str] = []
    request_id: str
    timestamp: str
    cost_estimate: float

@router.post("/chat", response_model=ChatResponse)
async def chat_completion(
    request: ChatRequest,
    x_api_key: str = Depends(verify_api_key)
):
    """Enterprise AI chat with policy enforcement"""
    try:
        logger.info(f"Chat request from {request.user_id} in {request.department}")
        
        # Policy enforcement logic
        sensitive_keywords = ["social security", "password", "credit card", "salary", "compensation"]
        violations = []
        
        for keyword in sensitive_keywords:
            if keyword in request.message.lower():
                violations.append(f"PII violation: {keyword}")
        
        is_blocked = len(violations) > 0
        
        if is_blocked:
            return ChatResponse(
                message="Request blocked by policy enforcement",
                is_blocked=True,
                block_reason="Sensitive data access attempted",
                policy_violations=violations,
                request_id="blocked_001",
                timestamp="2024-01-15T10:30:00Z",
                cost_estimate=0.0
            )
        
        # Successful processing
        return ChatResponse(
            message=f"Processed: {request.message}",
            is_blocked=False,
            block_reason=None,
            policy_violations=[],
            request_id="success_001",
            timestamp="2024-01-15T10:30:00Z",
            cost_estimate=0.0025
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")