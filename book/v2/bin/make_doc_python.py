#!/usr/bin/env python3

"""
=============================================================================
make_doc_python.py - Python Documentation Processor
=============================================================================

Description:
  This script provides three main functions:
  1. Processes a single Python file and converts its documentation to markdown
  2. Checks Python files for 'Last Updated' field in their docstrings
  3. Combines individual markdown files into a single document

Usage:
  Process single file:
    ./make_doc_python.py <filename.py>
    ./make_doc_python.py <filename.py> --create-doc

  Check Last Updated:
    ./make_doc_python.py --check-dates

  Join Documentation:
    ./make_doc_python.py --join-docs

Process:
  1. Takes a single Python file as input
  2. For the specified file:
     - Extracts the docstring between first set of triple quotes
     - Optionally converts to markdown using AI (with --create-doc)
     - Saves markdown file to ../docs/
  3. Optional:
     - Combines all markdown files in ../docs/ into python_docs.md

Output:
  - Individual .md file in ../docs/ (named after source file)
  - Optional combined python_docs.md when using --join-docs
  - Console output for missing Last Updated fields

Arguments:
  filename.py      Python file to process
  --create-doc     Use AI to create formatted markdown documentation
  --check-dates    Check all Python files for Last Updated field
  --join-docs      Join all markdown files in ../docs into one file

Dependencies:
  - Python 3.x
  - funcs_lib
  - colorama

Author: Assistant
Last Updated: 2024-03-21
MODIFIED
=============================================================================
"""

import os
import re
import funcs_lib as flib
from colorama import Fore, Style
import argparse
import sys

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

def convert_to_markdown_api(myprompt):

    # Get the API response
    response = flib.call_ai_api(
        prompt=myprompt,
        system_message="You are an expert assistant.",
        model="gpt-4o",
        provider="openai"
    )

    # Return the API response
    # print(response)

    # input(f"Press Enter to continue...")
    return response + "\n\n---\n\n"


def convert_to_markdown_local(filename, doc_comment):
    """Convert doc comment to markdown format."""
    if not doc_comment:
        return ""

    # Create markdown section
    markdown = f"## {filename}\n\n"
    markdown += doc_comment
    markdown += "\n\n---\n\n"
    return markdown

def check_last_updated():
    """Check all Python files in current directory for Last Updated field."""
    print("\nChecking Python files for 'Last Updated' field...")
    missing_count = 0

    # Get all Python files in current directory (non-recursively)
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]

    # Process each Python file
    for py_file in sorted(py_files):
        doc_comment = extract_doc_comment(py_file)
        if doc_comment and 'Last Updated' not in doc_comment:
            print(f"Missing 'Last Updated' in: {py_file}")
            missing_count += 1

    if missing_count:
        print(f"\nFound {missing_count} files missing 'Last Updated' field")
    else:
        print("\nAll files have 'Last Updated' field")

def main():
    parser = argparse.ArgumentParser(description='Extract documentation from Python file')
    parser.add_argument('filename', type=str, nargs='?',
                       help='Python file to process')
    parser.add_argument('--check-dates', action='store_true',
                       help='Check all Python files for Last Updated field')
    parser.add_argument('--join-docs', action='store_true',
                       help='Join all markdown files in ../docs into one file')
    parser.add_argument('--create-doc', action='store_true',
                       help='Create markdown documentation using AI API')
    args = parser.parse_args()

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.check_dates:
        check_last_updated()
        return

    if args.join_docs:
        docs_dir = "../docs"
        combined_doc = []

        # Get all markdown files in docs directory
        md_files = sorted([f for f in os.listdir(docs_dir) if f.endswith('.md')])

        print("\nJoining markdown files...")
        for md_file in md_files:
            file_path = os.path.join(docs_dir, md_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_doc.append(content)
                print(f"Added {md_file}")
            except Exception as e:
                print(f"Error reading {md_file}: {e}")

        # Write combined documentation
        output_path = os.path.join(docs_dir, "python_docs.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n\n".join(combined_doc))

        print(f"\nCombined documentation written to {output_path}")
        return

    # Check if filename was provided for processing
    if not args.filename:
        parser.error("filename argument is required when not using --check-dates or --join-docs")

    # Create ../docs directory if it doesn't exist
    docs_dir = "../docs"
    os.makedirs(docs_dir, exist_ok=True)

    # Verify file exists and is a Python file
    if not os.path.exists(args.filename):
        print(Fore.RED + f"Error: File '{args.filename}' not found" + Style.RESET_ALL)
        return
    if not args.filename.endswith('.py'):
        print(Fore.RED + f"Error: File '{args.filename}' is not a Python file" + Style.RESET_ALL)
        return

    print(Fore.GREEN + f"Processing file '{args.filename}'..." + Style.RESET_ALL)
    doc_comment = extract_doc_comment(args.filename)

    if doc_comment:
        if args.create_doc:
            # Use AI API to create markdown
            prompt = f"""
Convert the following docstring to markdown format: {doc_comment}.  Set the 'Last Updated' value to MM-DD-YYYY HH:MM format

Use the following template to create the markdown:

# {{program name}}

## {{program subtitle}}

{{ for ever H3 or '###' tag in the docstring, create a new section in the markdown with the following format:}}
### {{H3 tag or '###' tag content}}
{{content under the H3 tag or '###' tag}}

{{endfor}}
*Last Updated:* {{MM-DD-YYYY HH:MM}}
"""
            markdown = convert_to_markdown_api(prompt)
        else:
            # Simple conversion without AI
            markdown = f"# {args.filename}\n\n{doc_comment}\n"

        # Write individual markdown file - keep .py in filename
        doc_filename = args.filename + '.md'
        doc_path = os.path.join(docs_dir, doc_filename)
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"Documentation written to {doc_path}")
    else:
        print(Fore.RED + f"No documentation found in {args.filename}" + Style.RESET_ALL)

    # print(f"\nDocumentation file has been written to {docs_dir}/")

if __name__ == "__main__":
    main()