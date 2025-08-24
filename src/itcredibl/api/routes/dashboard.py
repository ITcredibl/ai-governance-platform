# src/itcredibl/api/routes/dashboard.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

router = APIRouter(tags=["dashboard"])

# Setup templates
current_dir = Path(__file__).parent
templates_path = current_dir / ".." / ".." / "templates"
templates = Jinja2Templates(directory=str(templates_path))

@router.get("/", response_class=HTMLResponse)
async def executive_dashboard(request: Request):
    """Main executive dashboard"""
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "company_name": "ITCREDIBL Enterprise",
            "version": "2.0.0"
        }
    )

@router.get("/demo", response_class=HTMLResponse)
async def demo_console(request: Request):
    """Interactive demo console"""
    return templates.TemplateResponse(
        "demo_console.html", 
        {"request": request}
    )