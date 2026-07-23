"""
Vercel serverless handler for FastAPI application.
This file is the entry point for Vercel deployments.
"""
import os
import sys

# Add the parent directory (project root) to sys.path
# This ensures that 'app' can be imported correctly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

# Export for Vercel
# Vercel needs the app object to be exposed in the file
# that is the target of the rewrite/route.
app = app

