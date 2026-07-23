@echo off
REM Development setup script for Markdown to PDF Converter (Windows)

echo.
echo 🚀 Setting up Markdown to PDF Converter Development Environment
echo ===============================================================

REM Check Python version
echo ✓ Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo ✓ Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ✓ Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1

REM Install dependencies
echo ✓ Installing production dependencies...
pip install -r requirements.txt >nul 2>&1

REM Install development dependencies
echo ✓ Installing development dependencies...
pip install -r requirements-dev.txt >nul 2>&1

REM Create .env if it doesn't exist
if not exist ".env" (
    echo ✓ Creating .env file...
    copy .env.example .env
    echo   Edit .env with your configuration
)

REM Create logs directory
if not exist "logs" mkdir logs

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo   1. Activate virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Start the development server:
echo      uvicorn app.main:app --reload
echo.
echo   3. Open in browser:
echo      http://localhost:8000/docs
echo.
echo   4. Run tests:
echo      pytest tests/ -v
echo.
pause
