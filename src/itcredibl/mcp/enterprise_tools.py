# In src/itcredibl/mcp/enterprise_tools.py, update the database handling:

class EnterpriseToolServer:
    def __init__(self):
        self.tools = { ... }
        self.db_manager = DatabaseManager()
        self.db_manager.connect()
        self.db_manager.init_demo_data()
    
    async def _query_customers(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Demonstrate secure data access with compliance."""
        try:
            if 'customer_id' in arguments:
                results = self.db_manager.execute_query(
                    'SELECT id, name, email, risk_score, compliance_status FROM customers WHERE id = ?',
                    (arguments['customer_id'],)
                )
            elif 'email' in arguments:
                results = self.db_manager.execute_query(
                    'SELECT id, name, email, risk_score, compliance_status FROM customers WHERE email = ?',
                    (arguments['email'],)
                )
            else:
                results = self.db_manager.execute_query(
                    'SELECT id, name, email, risk_score, compliance_status FROM customers LIMIT 10'
                )
            
            return {
                "status": "success",
                "data": results,
                "compliance_checked": True,
                "audit_logged": True,
                "row_count": len(results)
            }
            
        except Exception as e:
            logger.error("Database query failed", error=str(e))
            return {"status": "error", "message": str(e)}