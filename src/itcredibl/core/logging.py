"""
Enterprise logging configuration for ITCREDIBL platform.
"""
import logging
import json
from typing import Dict, Any

class StructuredLogger:
    """Enterprise-grade structured logging."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler with structured format
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def info(self, message: str, **kwargs):
        """Structured info logging."""
        log_data = {"message": message, **kwargs}
        self.logger.info(json.dumps(log_data))
    
    def error(self, message: str, **kwargs):
        """Structured error logging."""
        log_data = {"message": message, **kwargs}
        self.logger.error(json.dumps(log_data))
    
    def warning(self, message: str, **kwargs):
        """Structured warning logging."""
        log_data = {"message": message, **kwargs}
        self.logger.warning(json.dumps(log_data))

def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance."""
    return StructuredLogger(name)