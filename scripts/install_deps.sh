#!/bin/bash
# Install dependencies for Timeline Fishbone Generator

set -e

echo "Installing Timeline Fishbone Generator dependencies..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install package in editable mode with dev dependencies
echo "Installing package with development dependencies..."
pip install -e ".[dev]"

echo ""
echo "✓ Installation complete!"
echo ""
echo "Run tests with: pytest"
echo "Format code with: black src/ tests/"
echo "Check types with: mypy src/"
echo ""
