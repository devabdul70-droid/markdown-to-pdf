"""
Vercel serverless handler for FastAPI application.
This file is the entry point for Vercel deployments.
"""
import os
import sys

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

# Export for Vercel
handler = app



