from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PolicyAction(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    WARN = "warn"
    REQUIRE_APPROVAL = "require_approval"

class PolicyConfig(BaseModel):
    id: str = Field(..., description="Policy identifier")
    name: str = Field(..., description="Policy name")
    description: str = Field(..., description="Policy description")
    action: PolicyAction = Field(..., description="Action to take")
    conditions: List[str] = Field(default_factory=list, description="Policy conditions")
    priority: int = Field(0, description="Policy priority")
    enabled: bool = Field(True, description="Whether policy is enabled")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Update timestamp")