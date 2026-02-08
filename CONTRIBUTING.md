# Contributing to Timeline Fishbone Generator

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

### Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/tyeclipse/timeline-fishbone.git
cd timeline-fishbone
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=timeline_fishbone --cov-report=html

# Run specific test file
pytest tests/test_config.py

# Run with verbose output
pytest -v
```

### Code Formatting

We use `black` for code formatting and `isort` for import sorting:

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check without modifying
black --check src/ tests/
isort --check-only src/ tests/
```

### Linting

```bash
# Run flake8
flake8 src/ tests/

# Run mypy for type checking
mypy src/timeline_fishbone
```

### Pre-commit Checks

Before committing, ensure:

1. All tests pass: `pytest`
2. Code is formatted: `black src/ tests/`
3. Imports are sorted: `isort src/ tests/`
4. No linting errors: `flake8 src/ tests/`
5. Type hints are correct: `mypy src/`

## Making Changes

### Adding New Features

1. Write tests first (TDD approach recommended)
2. Implement the feature
3. Update documentation
4. Add examples if applicable
5. Update CHANGELOG.md

### Fixing Bugs

1. Add a test that reproduces the bug
2. Fix the bug
3. Ensure the test passes
4. Update documentation if needed

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use pytest fixtures for common setup
- Aim for >85% code coverage
- Test edge cases and error conditions

Example test:
```python
def test_config_validation():
    """Test configuration validation."""
    config = LayoutConfig(year_spacing=-1)
    with pytest.raises(ValidationError):
        validate_config(config)
```

### Documentation

- Update docstrings for new/modified functions
- Follow Google-style docstrings
- Update README.md for user-facing changes
- Add examples for new features

Example docstring:
```python
def generate_timeline(input_file: str, output_file: str) -> str:
    """
    Generate timeline from data file.
    
    Args:
        input_file: Path to CSV or JSON data file
        output_file: Path for output LaTeX file
        
    Returns:
        Generated LaTeX code as string
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValidationError: If data is invalid
        
    Example:
        >>> latex = generate_timeline("data.csv", "output.tex")
    """
```

## Pull Request Process

1. **Update Documentation**: Ensure all documentation is current
2. **Add Tests**: Include tests for new functionality
3. **Pass CI**: All CI checks must pass
4. **Code Review**: Address review feedback promptly
5. **Squash Commits**: Consider squashing before merge

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code formatted (black, isort)
- [ ] No linting errors
- [ ] Version bumped (if needed)
```

## Versioning

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## Release Process

1. Update version in `pyproject.toml` and `__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag -a v0.2.0 -m "Release 0.2.0"`
4. Push tag: `git push --tags`
5. Create GitHub release
6. Publish to PyPI (automated via GitHub Actions)

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use descriptive variable names
- Add comments for complex logic

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore`

### Import Organization

1. Standard library
2. Third-party packages
3. Local imports

```python
import sys
from pathlib import Path

import pandas as pd
import yaml

from .core import Config
```

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues/PRs first

Thank you for contributing! 🎉
