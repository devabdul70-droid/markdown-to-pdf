"""
Vercel serverless handler for FastAPI application.
This file is the entry point for Vercel deployments.
"""
import os
import sys
import logging

# Set up basic logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the parent directory (project root) to sys.path
# This ensures that 'app' can be imported correctly.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

try:
    logger.info("Attempting to import app.main...")
    from app.main import app
    # Export for Vercel
    handler = app
    logger.info("App imported successfully.")
except Exception as e:
    logger.error(f"Failed to load application: {str(e)}")
    # If we fail here, we can't return a FastAPI response, 
    # but Vercel will show the log in the dashboard.
    raise e

# Vercel needs the app object to be named 'app'
app = handler


