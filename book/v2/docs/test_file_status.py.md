# compare_json_dirs.py

## JSON Directory Comparison Tool

### Description
Compares JSON files between two directories, showing differences only for files that don't match. Looks for files with matching names and compares their contents.

### Usage
```bash
./compare_json_dirs.py <comparison_dir> [--short]
```

### Arguments
- `comparison_dir` : Directory to compare against `../regen/`
- `--short` : Only print filenames of differing files

### Output
Prints filenames and their differences when found (or just names with `--short`). Silent for matching files.

*Author:* Assistant  
*Last Updated:* 03-24-2024 15:30

---

