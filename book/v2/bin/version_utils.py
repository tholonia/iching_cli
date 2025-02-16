#!/usr/bin/env python3
"""
=============================================================================
version_utils.py - Version Management Utilities
=============================================================================

Description:
  This script provides utility functions for managing semantic versioning
  in the project. It handles reading, incrementing, and updating version
  numbers stored in a VERSION file.

Functions:
  - read_version(): Reads current version from VERSION file
  - increment_version(version_str): Increments patch version number
  - update_version(): Updates VERSION file with incremented version

Version Format:
  major.minor.patch (e.g., 1.2.3)
  - Patch increments normally (0-99)
  - Minor increments when patch > 99
  - Major increments when minor > 99

Dependencies:
  - Python 3.x standard library (os, pathlib)

File Structure:
  - VERSION file in parent directory

Author: JW
Last Updated: 2024
=============================================================================
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
