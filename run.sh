#!/bin/bash
# Quick start script for ITCREDIBL AI Governance Platform

# Kill any existing process on port 8000
kill -9 $(lsof -ti:8000) 2>/dev/null || true

# Set Python path
export PYTHONPATH=$(pwd)

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements_simple.txt
fi

# Activate virtual environment
source .venv/bin/activate

# Run the application
uvicorn src.itcredibl.api.main:app --reload --port 8000
