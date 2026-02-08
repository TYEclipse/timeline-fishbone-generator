#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Release automation script for Timeline Fishbone Generator.

Automates version bumping, changelog generation, and release preparation.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def get_current_version() -> str:
    """Get current version from __init__.py."""
    init_file = Path("src/timeline_fishbone/__init__.py")
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find __version__ in __init__.py")
    return match.group(1)


def bump_version(version: str, part: str) -> str:
    """Bump version number."""
    major, minor, patch = map(int, version.split('.'))
    
    if part == 'major':
        return f"{major + 1}.0.0"
    elif part == 'minor':
        return f"{major}.{minor + 1}.0"
    elif part == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid part: {part}")


def update_version(new_version: str) -> None:
    """Update version in all relevant files."""
    # Update __init__.py
    init_file = Path("src/timeline_fishbone/__init__.py")
    content = init_file.read_text()
    content = re.sub(
        r'__version__\s*=\s*["\'][^"\']+["\']',
        f'__version__ = "{new_version}"',
        content
    )
    init_file.write_text(content)
    
    # Update pyproject.toml
    pyproject = Path("pyproject.toml")
    content = pyproject.read_text()
    content = re.sub(
        r'version\s*=\s*["\'][^"\']+["\']',
        f'version = "{new_version}"',
        content,
        count=1
    )
    pyproject.write_text(content)


def run_tests() -> bool:
    """Run test suite."""
    print("Running tests...")
    result = subprocess.run(["pytest"], capture_output=True)
    return result.returncode == 0


def build_package() -> None:
    """Build distribution packages."""
    print("Building package...")
    subprocess.run(["python", "-m", "build"], check=True)


def main() -> int:
    """Main release workflow."""
    if len(sys.argv) < 2:
        print("Usage: python release.py [major|minor|patch]")
        return 1
    
    part = sys.argv[1]
    if part not in ['major', 'minor', 'patch']:
        print("Error: part must be 'major', 'minor', or 'patch'")
        return 1
    
    # Get current version
    current_version = get_current_version()
    print(f"Current version: {current_version}")
    
    # Bump version
    new_version = bump_version(current_version, part)
    print(f"New version: {new_version}")
    
    # Confirm
    response = input(f"Bump version from {current_version} to {new_version}? [y/N] ")
    if response.lower() != 'y':
        print("Aborted.")
        return 0
    
    # Run tests
    if not run_tests():
        print("✗ Tests failed. Aborting release.")
        return 1
    print("✓ Tests passed")
    
    # Update version
    update_version(new_version)
    print(f"✓ Updated version to {new_version}")
    
    # Build package
    build_package()
    print("✓ Package built")
    
    print(f"""
✓ Release preparation complete!

Next steps:
1. Review changes
2. Commit: git add -A && git commit -m "Bump version to {new_version}"
3. Tag: git tag -a v{new_version} -m "Release {new_version}"
4. Push: git push && git push --tags
5. Create GitHub release
6. Publish to PyPI: twine upload dist/*
    """)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
