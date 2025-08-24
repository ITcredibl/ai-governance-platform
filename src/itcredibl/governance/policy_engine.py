"""
Enterprise Policy Engine with advanced PII detection and compliance routing.
Python 3.13 compatible version.
"""
import re
import hashlib
from enum import Enum
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

from src.itcredibl.core.logging import get_logger
from config.settings import settings

logger = get_logger("itcredibl.policy")

class ComplianceLevel(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    HIGHLY_RESTRICTED = "highly_restricted"

class DataCategory(str, Enum):
    PII = "pii"
    FINANCIAL = "financial"
    PROPRIETARY = "proprietary"

@dataclass
class PolicyResult:
    redacted_text: str
    allowed_providers: List[str]
    required_tags: List[str]
    compliance_level: ComplianceLevel
    detected_categories: List[DataCategory]
    risk_score: float
    audit_id: str

class EnterprisePolicyEngine:
    """Advanced policy engine with comprehensive governance capabilities."""
    
    def __init__(self):
        self.patterns = {
            DataCategory.PII: [
                (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'EMAIL', 0.6),
                (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN', 0.9),
                (r'\b\d{3}-\d{3}-\d{4}\b', 'PHONE', 0.5),
            ],
            DataCategory.FINANCIAL: [
                (r'\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b', 'CREDIT_CARD', 0.8),
            ],
            DataCategory.PROPRIETARY: [
                (r'\b(?:sk-|AKIA|SG\.)[A-Za-z0-9_\-]{20,60}\b', 'API_KEY', 0.95),
            ]
        }
        
        self.compliance_rules = {
            ComplianceLevel.PUBLIC: {
                "providers": settings.default_providers,
                "tags": ["compliance:public"]
            },
            ComplianceLevel.INTERNAL: {
                "providers": settings.default_providers,
                "tags": ["compliance:internal"]
            },
            ComplianceLevel.RESTRICTED: {
                "providers": settings.restricted_providers,
                "tags": ["compliance:restricted", "data:pii"]
            },
            ComplianceLevel.HIGHLY_RESTRICTED: {
                "providers": settings.highly_restricted_providers,
                "tags": ["compliance:highly_restricted", "data:sensitive"]
            }
        }
    
    def enforce_policy(self, text: str, user_context: Dict) -> PolicyResult:
        """
        Comprehensive policy enforcement with enterprise-grade features.
        """
        audit_id = f"audit_{hash(text) % 10000:04d}"
        
        if not settings.pii_detection_enabled:
            return self._create_bypass_result(text, audit_id)
        
        # Analyze content for sensitive information
        detected_categories, risk_score = self._analyze_content(text)
        
        # Determine compliance level
        compliance_level = self._determine_compliance_level(risk_score, detected_categories)
        
        # Apply content redaction
        redacted_text = self._redact_content(text, detected_categories)
        
        # Get provider restrictions
        compliance_config = self.compliance_rules[compliance_level]
        allowed_providers = compliance_config["providers"]
        required_tags = compliance_config["tags"] + [f"category:{cat.value}" for cat in detected_categories]
        
        logger.info(
            "policy_enforced",
            audit_id=audit_id,
            compliance_level=compliance_level.value,
            risk_score=risk_score,
            detected_categories=[cat.value for cat in detected_categories],
            allowed_providers=allowed_providers
        )
        
        return PolicyResult(
            redacted_text=redacted_text,
            allowed_providers=allowed_providers,
            required_tags=required_tags,
            compliance_level=compliance_level,
            detected_categories=list(detected_categories),
            risk_score=risk_score,
            audit_id=audit_id
        )
    
    def _analyze_content(self, text: str) -> Tuple[Set[DataCategory], float]:
        """Analyze content for sensitive information."""
        detected_categories = set()
        risk_score = 0.0
        
        for category, patterns in self.patterns.items():
            for pattern, pattern_type, pattern_risk in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    detected_categories.add(category)
                    risk_score = max(risk_score, pattern_risk)
        
        return detected_categories, min(risk_score, 1.0)
    
    def _redact_content(self, text: str, categories: Set[DataCategory]) -> str:
        """Redact sensitive content while preserving context."""
        redacted_text = text
        
        for category in categories:
            if category in self.patterns:
                for pattern, pattern_type, _ in self.patterns[category]:
                    redacted_text = re.sub(
                        pattern, 
                        f"[REDACTED_{pattern_type}]", 
                        redacted_text, 
                        flags=re.IGNORECASE
                    )
        
        return redacted_text
    
    def _determine_compliance_level(self, risk_score: float, categories: Set[DataCategory]) -> ComplianceLevel:
        """Determine appropriate compliance level."""
        if risk_score >= 0.8:
            return ComplianceLevel.HIGHLY_RESTRICTED
        elif risk_score >= 0.6:
            return ComplianceLevel.RESTRICTED
        elif risk_score >= 0.3:
            return ComplianceLevel.INTERNAL
        else:
            return ComplianceLevel.PUBLIC
    
    def _create_bypass_result(self, text: str, audit_id: str) -> PolicyResult:
        """Create result when policy enforcement is disabled."""
        logger.warning("policy_enforcement_bypassed", audit_id=audit_id)
        
        return PolicyResult(
            redacted_text=text,
            allowed_providers=settings.default_providers,
            required_tags=["compliance:bypassed"],
            compliance_level=ComplianceLevel.PUBLIC,
            detected_categories=[],
            risk_score=0.0,
            audit_id=audit_id
        )

# Global policy engine instance
policy_engine = EnterprisePolicyEngine()


# src/itcredibl/governance/policy_engine.py

class PolicyResult:
    def __init__(self, is_blocked: bool = False, violations: list = None, risk_score: float = 0.0):
        self.is_blocked = is_blocked
        self.violations = violations or []
        self.risk_score = risk_score