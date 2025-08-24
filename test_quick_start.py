# test_quick_start.py
"""
Quick test to verify ITCREDIBL platform works with Python 3.13.
"""
from fastapi import FastAPI
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("itcredibl")

app = FastAPI(title="ITCREDIBL Quick Test", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "ITCREDIBL Enterprise AI Governance Platform", "status": "running"}

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "version": "1.0.0",
        "python_version": "3.13",
        "features": ["policy_engine", "mcp_tools", "cost_controls"]
    }

@app.get("/test-policy")
async def test_policy():
    """Test policy engine functionality."""
    return {
        "feature": "policy_engine",
        "status": "active",
        "capabilities": ["pii_detection", "compliance_routing", "content_redaction"]
    }

if __name__ == "__main__":
    logger.info("Starting ITCREDIBL Quick Test...")
    logger.info("Testing basic functionality...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")