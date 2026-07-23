# Quick Start Guide

## Local Development Setup (5 minutes)

### 1. Clone and Enter Project
```bash
cd markdown-to-pdf
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at: **http://localhost:8000**

## Testing

### Install Test Dependencies
```bash
pip install -r requirements-dev.txt
```

### Run Tests
```bash
pytest tests/ -v
```

### Run Specific Test
```bash
pytest tests/test_convert.py::TestConvertText::test_convert_text_minimal -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

## API Quick Reference

### Convert Markdown Text to PDF
```bash
curl -X POST http://localhost:8000/convert/text \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Hello\n\n**Bold** text",
    "theme": "default"
  }' \
  --output document.pdf
```

### Convert Markdown File to PDF
```bash
curl -X POST http://localhost:8000/convert/file \
  -F "file=@myfile.md" \
  -F "theme=dark" \
  --output output.pdf
```

### List Available Themes
```bash
curl http://localhost:8000/themes | jq
```

### Get Theme Details
```bash
curl http://localhost:8000/themes/academic | jq
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Documentation

- **Interactive API Docs:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## Docker Development

### Build Development Image
```bash
docker build -f Dockerfile-dev -t markdown-to-pdf:dev .
```

### Run Development Container
```bash
docker run -p 8000:8000 -v $(pwd)/app:/app/app markdown-to-pdf:dev
```

### Build Production Image
```bash
docker build -t markdown-to-pdf:latest .
```

### Run Production Container
```bash
docker run -p 8000:8000 markdown-to-pdf:latest
```

## Docker Compose

### Start Services
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f markdown-to-pdf
```

### Stop Services
```bash
docker-compose down
```

## Configuration

### Environment Variables
Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
DEBUG=False
MAX_FILE_SIZE=5242880
MAX_MARKDOWN_LENGTH=500000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
DEFAULT_PAGE_SIZE=A4
DEFAULT_MARGIN=2cm
```

## Troubleshooting

### WeasyPrint Installation Issues

**macOS:**
```bash
brew install libffi libssl
pip install --upgrade weasyprint
```

**Ubuntu/Debian:**
```bash
sudo apt-get install libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0
pip install --upgrade weasyprint
```

**Windows:**
```bash
pip install --only-binary :all: weasyprint
```

### Module Import Errors
```bash
# Make sure you're in the project root directory
# and the virtual environment is activated
python -c "from app.main import app; print('OK')"
```

### Connection Refused
```bash
# Check if port 8000 is already in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

## Code Quality

### Format Code
```bash
black app tests
```

### Sort Imports
```bash
isort app tests
```

### Lint Code
```bash
flake8 app tests
```

### Type Check
```bash
mypy app
```

## Project Structure
```
markdown-to-pdf/
├── app/
│   ├── main.py              # FastAPI app
│   ├── core/                # Configuration & logging
│   ├── api/                 # Route handlers
│   ├── services/            # Business logic
│   ├── models/              # Pydantic schemas
│   ├── utils/               # Validators & exceptions
│   ├── themes/              # CSS theme files
│   └── templates/           # Jinja2 templates
├── tests/                   # Test files
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── Dockerfile               # Production container
├── Dockerfile-dev           # Development container
├── docker-compose.yml       # Docker orchestration
├── pytest.ini               # Pytest configuration
└── README.md                # Full documentation
```

## Next Steps

1. **Read the README:** Full API documentation and examples
2. **Explore the Docs:** Open http://localhost:8000/docs
3. **Run Tests:** `pytest tests/ -v`
4. **Try Examples:** Use curl commands above to test endpoints
5. **Customize:** Add your own themes or extend functionality

## Support

For issues or questions:
1. Check the README.md for detailed documentation
2. Review API docs at /docs endpoint
3. Check application logs: `docker-compose logs markdown-to-pdf`
4. Examine test files for usage examples

Happy converting! 🎉
