#!/usr/bin/env python3

"""
=============================================================================
make_doc_sh.py - Shell Script Documentation Collector
=============================================================================

Description:
  This script scans the current directory for shell script files (*.sh), extracts
  their documentation comments, and compiles them into a single markdown file
  with an index of script usages at the top.

Usage:
  ./make_doc_sh.py

Process:
  1. Scans current directory for *.sh files
  2. For each shell script file:
     - Extracts the comment block at the top of the file
     - Extracts usage information
     - Converts to markdown format
  3. Creates script list and usage index
  4. Combines all sections into doc_sh.md

Output:
  - doc_sh.md: Combined markdown documentation with script list and usage index

Author: Assistant
Last Updated: 2024
=============================================================================
"""

import os
import re

def extract_doc_comment(file_path):
    """Extract the documentation comment from a shell script file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            # Skip shebang line if present
            start = 0
            if lines and lines[0].startswith('#!'):
                start = 1

            # Collect all comment lines until first non-comment or non-empty line
            doc_lines = []
            for line in lines[start:]:
                stripped = line.strip()
                # Stop at first line that's not a comment or empty
                if stripped and not stripped.startswith('#'):
                    break
                if stripped.startswith('#'):
                    # Remove leading '#' and optional space
                    doc_line = line.lstrip('#').strip()
                    doc_lines.append(doc_line)

            if doc_lines:
                return '\n'.join(doc_lines)

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
    # Get all shell script files in current directory
    sh_files = [f for f in os.listdir('.') if f.endswith('.sh')]

    # Collect all documentation and usages
    all_docs = []
    usages = {}

    # Process each shell script file
    for sh_file in sorted(sh_files):
        print(f"Processing {sh_file}...")
        doc_comment = extract_doc_comment(sh_file)
        if doc_comment:
            # Extract usage and store documentation
            usages[sh_file] = extract_usage(doc_comment)
            markdown = convert_to_markdown(sh_file, doc_comment)
            all_docs.append(markdown)
        else:
            print(f"No documentation found in {sh_file}")

    # Create complete documentation
    # Start with just the list of filenames, no headers or formatting
    full_doc = ""
    for filename in sorted(sh_files):
        full_doc += f"{filename}\n"

    # Add two blank lines after the list
    full_doc += "\n\n"

    # Add the rest of the documentation
    full_doc += """# Shell Scripts Documentation

This document contains the documentation for all shell scripts in the current directory.

---

"""
    # Add usage index
    full_doc += create_usage_index(usages)

    # Add full documentation sections
    full_doc += "# Script Documentation\n\n"
    full_doc += ''.join(all_docs)

    # Write combined documentation to file
    with open('doc_sh.md', 'w', encoding='utf-8') as f:
        f.write(full_doc)

    print("\nDocumentation has been compiled into doc_sh.md")

if __name__ == "__main__":
    main()