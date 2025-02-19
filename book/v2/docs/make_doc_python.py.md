# make_doc_python.py

## Python Documentation Processor

### Description
This script provides three main functions:
1. Processes a single Python file and converts its documentation to markdown
2. Checks Python files for 'Last Updated' field in their docstrings
3. Combines individual markdown files into a single document

### Usage
- Process single file:
  ```bash
  ./make_doc_python.py <filename.py>
  ./make_doc_python.py <filename.py> --create-doc
  ```

- Check Last Updated:
  ```bash
  ./make_doc_python.py --check-dates
  ```

- Join Documentation:
  ```bash
  ./make_doc_python.py --join-docs
  ```

### Process
1. Takes a single Python file as input
2. For the specified file:
   - Extracts the docstring between the first set of triple quotes
   - Optionally converts to markdown using AI (with --create-doc)
   - Saves markdown file to ../docs/
3. Optional:
   - Combines all markdown files in ../docs/ into python_docs.md

### Output
- Individual .md file in ../docs/ (named after source file)
- Optional combined python_docs.md when using --join-docs
- Console output for missing Last Updated fields

### Arguments
- `filename.py`: Python file to process
- `--create-doc`: Use AI to create formatted markdown documentation
- `--check-dates`: Check all Python files for Last Updated field
- `--join-docs`: Join all markdown files in ../docs into one file

### Dependencies
- Python 3.x
- funcs_lib
- colorama

*Last Updated:* 03-21-2024 00:00

---

