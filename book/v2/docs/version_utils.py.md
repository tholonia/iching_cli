# version_utils.py

## Version Management Utilities

### Description
This script provides utility functions for managing semantic versioning in the project. It handles reading, incrementing, and updating version numbers stored in a VERSION file.

### Functions
- `read_version()`: Reads current version from VERSION file
- `increment_version(version_str)`: Increments patch version number
- `update_version()`: Updates VERSION file with incremented version

### Version Format
major.minor.patch (e.g., 1.2.3)
- Patch increments normally (0-99)
- Minor increments when patch > 99
- Major increments when minor > 99

### Dependencies
- Python 3.x standard library (os, pathlib)

### File Structure
- VERSION file in parent directory

*Author:* JW  
*Last Updated:* 10-24-2023 12:00

---

