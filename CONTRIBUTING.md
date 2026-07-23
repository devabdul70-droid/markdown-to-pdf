# Contributing Guide

Thank you for your interest in contributing to the Markdown to PDF Converter!

## Code of Conduct

Be respectful and professional in all interactions.

## How to Contribute

### 1. Fork and Clone
```bash
git clone https://github.com/yourusername/markdown-to-pdf.git
cd markdown-to-pdf
```

### 2. Set Up Development Environment
```bash
# On Linux/macOS
./setup.sh

# On Windows
setup.bat
```

### 3. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes

- Follow PEP 8 style guide
- Add tests for new functionality
- Update documentation
- Commit with clear messages

### 5. Run Tests and Quality Checks
```bash
# Run tests
pytest tests/ -v

# Format code
black app tests
isort app tests

# Check code quality
flake8 app tests
mypy app
```

### 6. Submit Pull Request

- Describe changes clearly
- Reference any related issues
- Ensure all tests pass
- Request review from maintainers

## Development Workflow

### Project Structure
- **app/main.py** - FastAPI application entry point
- **app/core/** - Configuration and logging
- **app/api/routes/** - API endpoint handlers
- **app/services/** - Business logic
- **app/models/** - Pydantic schemas
- **app/utils/** - Utilities and validators
- **tests/** - Test suite

### Adding a New Theme

1. Create `app/themes/mytheme.css`
2. Update `app/services/theme_service.py` THEME_METADATA
3. Add tests in `tests/test_themes.py`

### Adding a New Endpoint

1. Create route handler in `app/api/routes/`
2. Define Pydantic models in `app/models/schemas.py`
3. Add service logic in `app/services/`
4. Add tests in `tests/`
5. Update documentation in `README.md` and `API.md`

### Database/Persistence

Currently, the API is stateless. If adding persistence:
- Use SQLAlchemy for ORM
- Add database connection handling
- Create migration scripts
- Update requirements.txt

## Code Quality Standards

### PEP 8 Compliance
```bash
black --line-length 100 app tests
```

### Type Hints
All functions should have type hints:
```python
def process_markdown(text: str) -> str:
    """Process markdown text."""
    return markdown.convert(text)
```

### Docstrings
Use Google-style docstrings:
```python
def function(param: str) -> str:
    """Brief description.
    
    Longer description if needed.
    
    Args:
        param: Parameter description
        
    Returns:
        Return value description
        
    Raises:
        CustomException: When this error occurs
    """
```

### Comments
Add comments for complex logic:
```python
# Extract and validate CSS variables from theme
variables = cls.extract_css_variables(css_content)
```

## Testing Requirements

### Test Coverage
- Aim for >80% code coverage
- Test happy paths and error cases
- Test edge cases

### Test Organization
```python
class TestConvertText:
    def test_basic_conversion(self):
        """Test description."""
        
    def test_with_custom_theme(self):
        """Test description."""
        
    def test_error_handling(self):
        """Test description."""
```

### Run Tests
```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Specific test
pytest tests/test_convert.py::TestConvertText::test_basic_conversion -v
```

## Documentation

### Update README.md for:
- New features
- Configuration changes
- New dependencies

### Update API.md for:
- New endpoints
- Request/response changes
- New fields

### Update QUICKSTART.md for:
- New setup steps
- Example changes

## Common Tasks

### Add a New Python Dependency
```bash
# Add to requirements.txt
pip install newpackage
pip freeze | grep newpackage >> requirements.txt
```

### Add Development Dependency
```bash
# Add to requirements-dev.txt
pip install devpackage
pip freeze | grep devpackage >> requirements-dev.txt
```

### Fix Code Formatting
```bash
# Format all code
black app tests
isort app tests

# Check what needs fixing
flake8 app tests
```

### Add Type Hints to File
```bash
mypy app/services/markdown_service.py --strict
```

## Release Process

### Before Release
1. Update version in `app/core/config.py`
2. Update `CHANGELOG.md` with changes
3. Ensure all tests pass
4. Update `README.md` if needed

### Tag Release
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Build Docker Image
```bash
docker build -t markdown-to-pdf:v1.0.0 .
docker push yourreg/markdown-to-pdf:v1.0.0
```

## Performance Considerations

### Optimization Tips
- Cache theme CSS files
- Use in-memory BytesIO for files
- Consider async file uploads for large files
- Profile with included profiling tools

### Scaling
- Add request queuing for high load
- Implement caching layer
- Use multiple workers
- Monitor PDF generation time

## Security Considerations

### Input Validation
- Always validate markdown input
- Check file types and sizes
- Sanitize HTML output
- Validate hex color codes

### Dependency Updates
```bash
pip list --outdated
pip install --upgrade package
```

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Reinstall package
pip install -e .
```

**Test failures:**
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

**WeasyPrint issues:**
```bash
# Reinstall with clean build
pip install --no-cache-dir --force-reinstall weasyprint
```

## Getting Help

- Check existing issues and discussions
- Review code comments and docstrings
- Ask in pull request reviews
- Check test files for usage examples

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md
- GitHub contributors page
- Release notes

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

Thank you for helping improve this project! 🎉
