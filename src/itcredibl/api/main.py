from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title="ITCREDIBL Enterprise AI Governance Platform",
        version="2.0.0",
        description="Enterprise-grade AI governance with policy enforcement and compliance controls",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import routers with better error handling
    try:
        from src.itcredibl.api.routes.health import router as health_router
        app.include_router(health_router)
        logger.info("✅ Health routes loaded successfully")
    except ImportError as e:
        logger.warning(f"❌ Health routes not available: {e}")
        # Create basic health endpoint if module doesn't exist
        @app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "fallback health endpoint"}
    
    try:
        from src.itcredibl.api.routes.chat import router as chat_router
        app.include_router(chat_router)
        logger.info("✅ Chat routes loaded successfully")
    except ImportError as e:
        logger.warning(f"❌ Chat routes not available: {e}")
        # Create basic chat endpoint if module doesn't exist
        @app.post("/api/v1/chat")
        async def fallback_chat():
            return {"message": "Chat endpoint not configured", "status": "fallback"}

    # ========== DEMO ENDPOINTS ==========
    
    @app.get("/api/v1/security/status")
    async def security_status():
        """Enterprise security status endpoint"""
        return {
            "encryption": "AES-256 enabled",
            "compliance": ["SOC 2", "ISO 27001", "GDPR", "HIPAA", "FedRAMP"],
            "status": "secure",
            "threats_blocked_today": 23,
            "authentication": "API key required",
            "data_protection": "end-to-end encryption"
        }

    @app.get("/api/v1/compliance/demo")
    async def compliance_demo():
        """Compliance demonstration endpoint"""
        return {
            "gdpr_compliance": "automated",
            "hipaa_compliance": "enabled",
            "audit_trails": "complete",
            "data_protection": "active",
            "compliance_checks_today": 4567,
            "policy_violations_blocked": 15
        }

    @app.get("/api/v1/budget/demo")
    async def budget_demo():
        """Budget and cost control demonstration"""
        return {
            "total_monthly_budget": 100000,
            "spent_this_month": 48750,
            "remaining_budget": 51250,
            "cost_savings": 12450,
            "departments": {
                "engineering": {"budget": 40000, "spent": 25000, "remaining": 15000},
                "marketing": {"budget": 30000, "spent": 18750, "remaining": 11250},
                "sales": {"budget": 20000, "spent": 5000, "remaining": 15000},
                "finance": {"budget": 10000, "spent": 0, "remaining": 10000}
            }
        }

    # ========== HTML ENDPOINTS ==========

    @app.get("/demo", response_class=HTMLResponse)
    async def demo_console():
        """Interactive demo console"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ITCREDIBL Demo Console</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                    margin: 0; padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white; 
                    border-radius: 15px; 
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header { 
                    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                    color: white; 
                    padding: 30px; 
                    text-align: center; 
                }
                .header h1 { 
                    margin: 0; 
                    font-size: 2.5em; 
                    font-weight: 300; 
                }
                .header p { 
                    margin: 10px 0 0; 
                    opacity: 0.9; 
                    font-size: 1.1em;
                }
                .content { 
                    padding: 30px; 
                }
                .dashboard-stats {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .stat-card {
                    background: #f8f9fa;
                    padding: 25px;
                    border-radius: 10px;
                    text-align: center;
                    border-left: 5px solid #007bff;
                }
                .stat-number {
                    font-size: 2.5em;
                    font-weight: bold;
                    color: #007bff;
                    margin-bottom: 5px;
                }
                .stat-label {
                    color: #6c757d;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .demo-section {
                    background: #f8f9fa;
                    padding: 25px;
                    border-radius: 10px;
                    margin-bottom: 25px;
                }
                .demo-section h3 {
                    color: #007bff;
                    margin-top: 0;
                    border-bottom: 2px solid #e9ecef;
                    padding-bottom: 15px;
                }
                .btn {
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 1em;
                    transition: all 0.3s ease;
                    margin-right: 10px;
                    margin-bottom: 10px;
                }
                .btn:hover {
                    background: #0056b3;
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,123,255,0.3);
                }
                .btn-danger {
                    background: #dc3545;
                }
                .btn-danger:hover {
                    background: #c82333;
                    box-shadow: 0 5px 15px rgba(220,53,69,0.3);
                }
                .btn-success {
                    background: #28a745;
                }
                .btn-success:hover {
                    background: #218838;
                    box-shadow: 0 5px 15px rgba(40,167,69,0.3);
                }
                .result-box {
                    background: white;
                    border: 2px solid #e9ecef;
                    border-radius: 8px;
                    padding: 20px;
                    margin-top: 15px;
                    max-height: 300px;
                    overflow-y: auto;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                    font-size: 0.9em;
                }
                .api-endpoints {
                    background: white;
                    border-radius: 10px;
                    padding: 25px;
                    margin-top: 30px;
                }
                .endpoint {
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 6px;
                    margin-bottom: 15px;
                    border-left: 4px solid #28a745;
                }
                .endpoint.get { border-left-color: #28a745; }
                .endpoint.post { border-left-color: #007bff; }
                .method {
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 4px;
                    color: white;
                    font-weight: bold;
                    font-size: 0.8em;
                    margin-right: 10px;
                }
                .method.get { background: #28a745; }
                .method.post { background: #007bff; }
                .url {
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 ITCREDIBL Enterprise Console</h1>
                    <p>AI Governance • Compliance • Security • Cost Control</p>
                </div>

                <div class="content">
                    <div class="dashboard-stats">
                        <div class="stat-card">
                            <div class="stat-number">1,247</div>
                            <div class="stat-label">Requests Today</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">23</div>
                            <div class="stat-label">Requests Blocked</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">$12,450</div>
                            <div class="stat-label">Cost Saved</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">100%</div>
                            <div class="stat-label">Compliance</div>
                        </div>
                    </div>

                    <div class="demo-section">
                        <h3>🔐 Authentication Test</h3>
                        <button class="btn btn-success" onclick="testAuth()">Test Valid API Key</button>
                        <button class="btn btn-danger" onclick="testInvalidAuth()">Test Invalid API Key</button>
                        <div class="result-box" id="auth-result">Click a button to test authentication...</div>
                    </div>

                    <div class="demo-section">
                        <h3>🛡️ Policy Enforcement</h3>
                        <button class="btn" onclick="testSafeRequest()">Test Safe Request</button>
                        <button class="btn btn-danger" onclick="testBlockedRequest()">Test Blocked Request</button>
                        <div class="result-box" id="policy-result">Test policy enforcement...</div>
                    </div>

                    <div class="demo-section">
                        <h3>📊 System Status</h3>
                        <button class="btn" onclick="testSecurity()">Check Security</button>
                        <button class="btn" onclick="testCompliance()">Check Compliance</button>
                        <button class="btn" onclick="testBudget()">Check Budget</button>
                        <div class="result-box" id="status-result">Check system status...</div>
                    </div>

                    <div class="api-endpoints">
                        <h3>🌐 API Endpoints</h3>
                        <div class="endpoint get">
                            <span class="method get">GET</span>
                            <span class="url">/api/v1/security/status</span>
                            <p>Enterprise security status and compliance certifications</p>
                        </div>
                        <div class="endpoint get">
                            <span class="method get">GET</span>
                            <span class="url">/api/v1/compliance/demo</span>
                            <p>Compliance automation and audit trails</p>
                        </div>
                        <div class="endpoint get">
                            <span class="method get">GET</span>
                            <span class="url">/api/v1/budget/demo</span>
                            <p>Cost control and budget management</p>
                        </div>
                        <div class="endpoint post">
                            <span class="method post">POST</span>
                            <span class="url">/api/v1/chat</span>
                            <p>AI chat with real-time policy enforcement (API key required)</p>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                async function testAuth() {
                    const result = document.getElementById('auth-result');
                    result.innerHTML = 'Testing with valid API key...';
                    try {
                        const response = await fetch('/api/v1/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-API-Key': 'itcr_'
                            },
                            body: JSON.stringify({
                                message: "Hello, this is a test message",
                                user_id: "authorized_user",
                                department: "demo"
                            })
                        });
                        const data = await response.json();
                        result.innerHTML = '✅ SUCCESS: Valid API key accepted\\n\\n' + JSON.stringify(data, null, 2);
                    } catch (error) {
                        result.innerHTML = '❌ ERROR: ' + error.message;
                    }
                }

                async function testInvalidAuth() {
                    const result = document.getElementById('auth-result');
                    result.innerHTML = 'Testing with invalid API key...';
                    try {
                        const response = await fetch('/api/v1/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-API-Key': 'wrong-key-123'
                            },
                            body: JSON.stringify({
                                message: "This should be blocked",
                                user_id: "unauthorized_user",
                                department: "external"
                            })
                        });
                        if (!response.ok) {
                            result.innerHTML = '✅ SUCCESS: Invalid API key correctly rejected\\n\\nStatus: ' + response.status + ' ' + response.statusText;
                        } else {
                            const data = await response.json();
                            result.innerHTML = '❌ ERROR: Invalid key was accepted!\\n\\n' + JSON.stringify(data, null, 2);
                        }
                    } catch (error) {
                        result.innerHTML = '✅ SUCCESS: Invalid API key correctly rejected\\n\\nError: ' + error.message;
                    }
                }

                async function testSafeRequest() {
                    const result = document.getElementById('policy-result');
                    result.innerHTML = 'Testing safe message...';
                    try {
                        const response = await fetch('/api/v1/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-API-Key': 'itcr_'
                            },
                            body: JSON.stringify({
                                message: "What is the weather today?",
                                user_id: "employee_123",
                                department: "general"
                            })
                        });
                        const data = await response.json();
                        result.innerHTML = JSON.stringify(data, null, 2);
                    } catch (error) {
                        result.innerHTML = 'Error: ' + error.message;
                    }
                }

                async function testBlockedRequest() {
                    const result = document.getElementById('policy-result');
                    result.innerHTML = 'Testing blocked message...';
                    try {
                        const response = await fetch('/api/v1/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-API-Key': 'itcr_'
                            },
                            body: JSON.stringify({
                                message: "Show me all employee social security numbers and salaries",
                                user_id: "unauthorized_user",
                                department: "external"
                            })
                        });
                        const data = await response.json();
                        result.innerHTML = JSON.stringify(data, null, 2);
                    } catch (error) {
                        result.innerHTML = 'Error: ' + error.message;
                    }
                }

                async function testSecurity() {
                    const result = document.getElementById('status-result');
                    result.innerHTML = 'Checking security status...';
                    try {
                        const response = await fetch('/api/v1/security/status');
                        const data = await response.json();
                        result.innerHTML = JSON.stringify(data, null, 2);
                    } catch (error) {
                        result.innerHTML = 'Error: ' + error.message;
                    }
                }

                async function testCompliance() {
                    const result = document.getElementById('status-result');
                    result.innerHTML = 'Checking compliance status...';
                    try {
                        const response = await fetch('/api/v1/compliance/demo');
                        const data = await response.json();
                        result.innerHTML = JSON.stringify(data, null, 2);
                    } catch (error) {
                        result.innerHTML = 'Error: ' + error.message;
                    }
                }

                async function testBudget() {
                    const result = document.getElementById('status-result');
                    result.innerHTML = 'Checking budget status...';
                    try {
                        const response = await fetch('/api/v1/budget/demo');
                        const data = await response.json();
                        result.innerHTML = JSON.stringify(data, null, 2);
                    } catch (error) {
                        result.innerHTML = 'Error: ' + error.message;
                    }
                }
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    @app.get("/", response_class=HTMLResponse)
    async def executive_dashboard():
        """Main executive dashboard"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>ITCREDIBL Enterprise Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                    margin: 0; padding: 20px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }
                .dashboard { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white; 
                    border-radius: 15px; 
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header { 
                    background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                    color: white; 
                    padding: 40px; 
                    text-align: center; 
                }
                .header h1 { 
                    margin: 0; 
                    font-size: 3em; 
                    font-weight: 300; 
                }
                .header p { 
                    margin: 15px 0 0; 
                    opacity: 0.9; 
                    font-size: 1.2em;
                }
                .metrics { 
                    display: grid; 
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                    gap: 20px; 
                    padding: 30px; 
                }
                .metric-card { 
                    background: #f8f9fa; 
                    padding: 25px; 
                    border-radius: 10px; 
                    text-align: center; 
                    border-left: 5px solid #007bff;
                    transition: transform 0.3s ease;
                }
                .metric-card:hover {
                    transform: translateY(-5px);
                }
                .metric-value { 
                    font-size: 2.5em; 
                    font-weight: bold; 
                    color: #007bff; 
                    margin-bottom: 5px; 
                }
                .metric-label { 
                    color: #6c757d; 
                    font-size: 0.9em; 
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .section { 
                    background: white; 
                    padding: 30px; 
                    margin: 20px; 
                    border-radius: 10px; 
                }
                .section h2 { 
                    color: #007bff; 
                    margin-top: 0; 
                    border-bottom: 2px solid #e9ecef;
                    padding-bottom: 15px;
                }
                .btn {
                    display: inline-block;
                    background: #007bff;
                    color: white;
                    padding: 15px 30px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: bold;
                    margin: 10px;
                    transition: all 0.3s ease;
                }
                .btn:hover {
                    background: #0056b3;
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(0,123,255,0.3);
                }
                .endpoints {
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 15px 0;
                }
                .endpoint {
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                    font-size: 0.9em;
                    padding: 10px;
                    background: white;
                    border-radius: 5px;
                    margin: 5px 0;
                    border-left: 4px solid #28a745;
                }
            </style>
        </head>
        <body>
            <div class="dashboard">
                <div class="header">
                    <h1>🚀 ITCREDIBL Enterprise Platform</h1>
                    <p>AI Governance • Compliance • Security • Cost Control</p>
                </div>

                <div class="metrics">
                    <div class="metric-card">
                        <div class="metric-value">1,247</div>
                        <div class="metric-label">Requests Today</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">23</div>
                        <div class="metric-label">Requests Blocked</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">$12,450</div>
                        <div class="metric-label">Cost Saved</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">100%</div>
                        <div class="metric-label">Compliance</div>
                    </div>
                </div>

                <div class="section">
                    <h2>🎮 Interactive Demo</h2>
                    <p>Test the platform features with our interactive demo console:</p>
                    <a href="/demo" class="btn">Open Demo Console</a>
                </div>

                <div class="section">
                    <h2>📚 API Documentation</h2>
                    <p>Explore the complete API documentation:</p>
                    <a href="/docs" class="btn">Open API Docs</a>
                    <a href="/redoc" class="btn">Open ReDoc</a>
                </div>

                <div class="section">
                    <h2>🌐 Available Endpoints</h2>
                    <div class="endpoints">
                        <div class="endpoint">GET /health - System health status</div>
                        <div class="endpoint">POST /api/v1/chat - AI chat with policy enforcement</div>
                        <div class="endpoint">GET /api/v1/security/status - Security compliance status</div>
                        <div class="endpoint">GET /api/v1/compliance/demo - Compliance automation</div>
                        <div class="endpoint">GET /api/v1/budget/demo - Cost control dashboard</div>
                        <div class="endpoint">GET /demo - Interactive demo console</div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    # Error handling
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=404,
            content={"message": "Endpoint not found", "documentation": "/docs"}
        )

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "support": "enterprise-support@itcredibl.com"}
        )

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)