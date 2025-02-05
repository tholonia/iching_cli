#!/usr/bin/env python3
"""
Utility functions for version management.
"""

import os
from pathlib import Path

VERSION_FILE = Path(__file__).parent.parent / "VERSION"

def read_version():
    """Read the current version from VERSION file."""
    if not VERSION_FILE.exists():
        return "0.0.0"
    return VERSION_FILE.read_text().strip()

def increment_version(version_str):
    """Increment the patch version number."""
    major, minor, patch = map(int, version_str.split('.'))
    patch += 1
    if patch > 99:
        patch = 0
        minor += 1
        if minor > 99:
            minor = 0
            major += 1
    return f"{major}.{minor}.{patch}"

def update_version():
    """Read current version, increment it, and save it back."""
    current = read_version()
    new_version = increment_version(current)
    VERSION_FILE.write_text(new_version)
    return new_version

if __name__ == "__main__":
    print(update_version())
