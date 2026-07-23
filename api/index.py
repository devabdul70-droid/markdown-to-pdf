"""
Vercel serverless handler for FastAPI application.
This file is the entry point for Vercel deployments.
"""

from app.main import app

# ASGI application for Vercel
asgi_app = app
