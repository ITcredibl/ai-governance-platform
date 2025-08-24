# src/itcredibl/core/models/chat.py

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class Department(str, Enum):
    FINANCE = "finance"
    HR = "hr"
    IT = "it"
    MARKETING = "marketing"
    SALES = "sales"
    LEGAL = "legal"
    EXECUTIVE = "executive"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PolicyResult(BaseModel):
    is_blocked: bool = Field(..., description="Whether the request is blocked")
    violations: List[str] = Field(default_factory=list, description="List of policy violations")
    risk_score: float = Field(0.0, ge=0.0, le=1.0, description="Risk score from 0.0 to 1.0")
    risk_level: RiskLevel = Field(RiskLevel.LOW, description="Risk level")
    recommended_action: Optional[str] = Field(None, description="Recommended action")

class AuditLog(BaseModel):
    id: str = Field(..., description="Unique log identifier")
    timestamp: datetime = Field(..., description="Event timestamp")
    user_id: str = Field(..., description="User identifier")
    department: Department = Field(..., description="User department")
    endpoint: str = Field(..., description="API endpoint")
    request: Dict[str, Any] = Field(..., description="Request data")
    response: Dict[str, Any] = Field(..., description="Response data")
    policy_result: PolicyResult = Field(..., description="Policy enforcement result")
    cost: Optional[float] = Field(None, description="Transaction cost")
    duration_ms: float = Field(..., description="Processing duration in milliseconds")