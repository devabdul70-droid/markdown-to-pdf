#!/usr/bin/env bash
# Development setup script for Markdown to PDF Converter

set -e

echo "🚀 Setting up Markdown to PDF Converter Development Environment"
echo "=============================================================="

# Check Python version
echo "✓ Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
required_version="3.11"
if [[ "$python_version" < "$required_version" ]]; then
    echo "❌ Python $required_version+ required, found $python_version"
    exit 1
fi
echo "  Using Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || true

# Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1

# Install dependencies
echo "✓ Installing production dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

# Install development dependencies
echo "✓ Installing development dependencies..."
pip install -r requirements-dev.txt > /dev/null 2>&1

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file..."
    cp .env.example .env
    echo "  Edit .env with your configuration"
fi

# Create logs directory
mkdir -p logs

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Start the development server:"
echo "     uvicorn app.main:app --reload"
echo ""
echo "  3. Open in browser:"
echo "     http://localhost:8000/docs"
echo ""
echo "  4. Run tests:"
echo "     pytest tests/ -v"
echo ""
