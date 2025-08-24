# src/itcredibl/core/database.py
"""
Database utilities with SQLite support for Python 3.13 compatibility.
"""
import sqlite3
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class DatabaseManager:
    """SQLite database manager for enterprise demo."""
    
    def __init__(self, database_url: str = "sqlite:///./itcredibl_demo.db"):
        self.database_url = database_url
        self.connection = None
        
    def connect(self):
        """Connect to SQLite database."""
        try:
            # Extract path from SQLAlchemy-style URL
            if self.database_url.startswith('sqlite:///'):
                db_path = self.database_url.replace('sqlite:///', '')
            else:
                db_path = self.database_url
                
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row
            logger.info("Connected to SQLite database", db_path=db_path)
            return True
        except Exception as e:
            logger.error("Database connection failed", error=str(e))
            return False
    
    def init_demo_data(self):
        """Initialize demo data for enterprise showcase."""
        if not self.connection:
            self.connect()
            
        try:
            cursor = self.connection.cursor()
            
            # Create customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    risk_score INTEGER,
                    compliance_status TEXT,
                    department TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert demo enterprise data
            demo_customers = [
                ('cust_001', 'John Enterprise', 'john@enterprise.com', 25, 'compliant', 'finance'),
                ('cust_002', 'Sarah Business', 'sarah@business.com', 65, 'review', 'operations'),
                ('cust_003', 'David Corporation', 'david@corporation.com', 85, 'non_compliant', 'sales'),
                ('cust_004', 'Maria Holdings', 'maria@holdings.com', 45, 'compliant', 'hr'),
                ('cust_005', 'James Group', 'james@group.com', 75, 'review', 'it')
            ]
            
            cursor.executemany(
                'INSERT OR IGNORE INTO customers (id, name, email, risk_score, compliance_status, department) VALUES (?, ?, ?, ?, ?, ?)',
                demo_customers
            )
            
            self.connection.commit()
            logger.info("Demo data initialized", customer_count=len(demo_customers))
            
        except Exception as e:
            logger.error("Failed to initialize demo data", error=str(e))
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Execute a SQL query safely."""
        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error("Query execution failed", error=str(e), query=query)
            raise
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")

# Global database instance
db_manager = DatabaseManager()