"""
Enterprise configuration management for ITCREDIBL AI Governance Platform.
Python 3.13 compatible version.
"""
from typing import List, Optional
from enum import Enum
import os

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class Settings:
    """Enterprise settings management."""
    
    def __init__(self):
        # Application Settings
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.log_level = os.getenv("LOG_LEVEL", "info")
        self.app_name = "itcredibl-ai-governance-platform"
        self.app_version = "2.0.0"
        
        # API Settings
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.api_prefix = os.getenv("API_PREFIX", "/api/v1")
        
        # Security Settings
        self.secret_key = os.getenv("SECRET_KEY", "itcredibl-enterprise-demo-key-change-in-production")
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        
        # Database Settings (SQLite for compatibility)
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./itcredibl_enterprise.db")
        
        # Redis Settings (with fallback)
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        
        # ITCREDIBL API Settings
        self.itcredibl_base_url = os.getenv("ITCREDIBL_BASE_URL", "https://api.itcredibl.com")
        self.itcredibl_api_key = os.getenv("ITCREDIBL_API_KEY", "demo-enterprise-api-key")
        
        # Provider Configuration
        self.default_providers = ["openai", "anthropic", "azure"]
        self.restricted_providers = ["aws_bedrock", "google_vertex"]
        self.highly_restricted_providers = ["on_prem_llm"]
        
        # Policy Engine Configuration
        self.pii_detection_enabled = os.getenv("PII_DETECTION_ENABLED", "true").lower() == "true"
        self.compliance_enforcement = os.getenv("COMPLIANCE_ENFORCEMENT", "true").lower() == "true"
        
        # Cache Configuration
        self.cache_enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        
        # Circuit Breaker Configuration
        self.circuit_breaker_enabled = os.getenv("CIRCUIT_BREAKER_ENABLED", "true").lower() == "true"
        
        # Budget Configuration
        self.budget_enforcement = os.getenv("BUDGET_ENFORCEMENT", "true").lower() == "true"
        
        # MCP Configuration
        self.mcp_enabled = os.getenv("MCP_ENABLED", "true").lower() == "true"

# Global settings instance
settings = Settings()