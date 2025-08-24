# src/itcredibl/api/routes/health.py
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "policy_engine": "operational",
            "compliance": "operational",
            "budget_control": "operational"
        }
    }

@router.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "ITCREDIBL Enterprise AI Governance Platform",
        "version": "2.0.0",
        "description": "Enterprise-grade AI governance with policy enforcement and compliance controls",
        "documentation": "https://docs.itcredibl.com",
        "support": "enterprise-support@itcredibl.com"
    }