#!/usr/bin/env python3

"""
=============================================================================
make_doc_py.py - Python Documentation Collector with Usage Index
=============================================================================

Description:
  This script scans the current directory for Python files (*.py), extracts
  their documentation comments, and compiles them into a single markdown file
  with an index of script usages at the top.

Usage:
  ./make_doc_py.py

Process:
  1. Scans current directory for *.py files
  2. For each Python file:
     - Extracts the docstring between first set of triple quotes
     - Extracts usage information
     - Converts to markdown format
  3. Creates script list and usage index
  4. Combines all sections into doc_py.md

Output:
  - doc_py.md: Combined markdown documentation with script list and usage index

Author: Assistant
Last Updated: 2024
=============================================================================
"""

import os
import re

def extract_doc_comment(file_path):
    """Extract the documentation comment from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Find content between first set of triple quotes
            match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if match:
                return match.group(1).strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def extract_usage(doc_comment):
    """Extract usage information from doc comment."""
    if not doc_comment:
        return None

    # Look for Usage section
    usage_match = re.search(r'Usage:\s*(.*?)(?=\n\n|\Z)', doc_comment, re.DOTALL)
    if usage_match:
        return usage_match.group(1).strip()
    return None

def convert_to_markdown(filename, doc_comment):
    """Convert doc comment to markdown format."""
    if not doc_comment:
        return ""

    # Create markdown section
    markdown = f"## {filename}\n\n"
    markdown += doc_comment
    markdown += "\n\n---\n\n"
    return markdown

def create_script_list(filenames):
    """Create a simple list of all scripts."""
    script_list = """# Available Scripts

"""
    for filename in sorted(filenames):
        script_list += f"{filename}\n"

    script_list += "\n---\n\n"
    return script_list

def create_usage_index(usages):
    """Create markdown index of script usages."""
    if not usages:
        return ""

    index = """# Script Usage Index

Detailed usage instructions for each script:

"""
    for filename, usage in sorted(usages.items()):
        if usage:
            # Create link to script section and include usage
            index += f"- [{filename}](#{filename.lower()})\n"
            index += f"  ```\n  {usage}\n  ```\n\n"

    index += "---\n\n"
    return index

def main():
    # Get all Python files in current directory
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]

    # Collect all documentation and usages
    all_docs = []
    usages = {}

    # Process each Python file
    for py_file in sorted(py_files):
        print(f"Processing {py_file}...")
        doc_comment = extract_doc_comment(py_file)
        if doc_comment:
            # Extract usage and store documentation
            usages[py_file] = extract_usage(doc_comment)
            markdown = convert_to_markdown(py_file, doc_comment)
            all_docs.append(markdown)
        else:
            print(f"No documentation found in {py_file}")

    # Create complete documentation
    # Start with just the list of filenames, no headers or formatting
    full_doc = ""
    for filename in sorted(py_files):
        full_doc += f"{filename}\n"

    # Add two blank lines after the list
    full_doc += "\n\n"

    # Add the rest of the documentation
    full_doc += """# Python Scripts Documentation

This document contains the documentation for all Python scripts in the current directory.

---

"""
    # Add usage index
    full_doc += create_usage_index(usages)

    # Add full documentation sections
    full_doc += "# Script Documentation\n\n"
    full_doc += ''.join(all_docs)

    # # Write the initial list of filenames
    # with open('doc_py.md', 'w', encoding='utf-8') as f:
    #     # Write just the filenames at the start
    #     for filename in sorted(py_files):
    #         f.write(f"{filename}\n")
    #     f.write("\n\n")

    # Append the rest of the documentation
    # Write combined documentation to file
    with open('doc_py.md', 'w', encoding='utf-8') as f:
        f.write(full_doc)

    print("\nDocumentation has been compiled into doc_py.md")

if __name__ == "__main__":
    main()