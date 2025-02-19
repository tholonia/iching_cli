#!/usr/bin/env python
import fitz  # PyMuPDF
import re
import glob
import os
import json
from pprint import pprint  # For debug printing

"""
=============================================================================
regen_TOC.py - Table of Contents Generator for I Ching Book
=============================================================================

Description:
    Generates a formatted HTML table of contents for the I Ching book by:
    1. Extracting page numbers from PDF where hexagram images appear
    2. Reading hexagram titles and codes from JSON files
    3. Creating a three-column HTML layout with dotted leaders

Usage:
    ./regen_TOC.py

Input Files:
    - ../includes/iching.pdf : Source PDF file
    - ../regen/*.json : Hexagram JSON files containing titles and codes

Output:
    - ../includes/TOC.html : Generated table of contents in HTML format

Format:
    Three-column layout with:
    - Hexagram number (01-64)
    - Unicode hexagram symbol
    - Hexagram name
    - Dotted leader
    - Page number

Functions:
    extract_page_numbers(pdf_path)
        - Extracts page numbers from PDF pages containing hexagram images

    get_hexagram_titles(directory)
        - Reads hexagram data from JSON files

    create_toc_html(titles, pages)
        - Generates formatted HTML with three-column layout

    generate_toc(titles, pages, output_file)
        - Main function to create and save TOC file

Dependencies:
    - PyMuPDF (fitz)
    - json
    - glob
    - os
    - re

Author: JW
Last Updated: 2024
=============================================================================
"""

def create_toc_html(titles, pages_with_images):
    # Start with HTML header including CSS styles
    html = """<!DOCTYPE html>
<html>
<head>
    <style>
        .container {
            display: flex;
            justify-content: space-between;
            max-width: 1200px;  /* Increased max-width for three columns */
            margin: 0 auto;
            font-family: serif;
        }

        .column {
            width: 32%;  /* Changed from 48% to 32% for three columns */
        }

        .toc-entry {
            display: flex;
            align-items: baseline;
            margin: 8px 0;
            font-size: 10pt;
        }

        .title {
            white-space: nowrap;
        }

        .dots {
            border-bottom: 1px dotted #000;
            flex: 1;
            margin: 0 8px;
        }

        .page {
            white-space: nowrap;
        }

        h1 {
            text-align: center;
            color: #333;
            font-family: serif;
        }

    </style>
</head>
<body>
    <div style="page-break-before: always;"></div>
    <h1>Table of Contents</h1>
    <div class="container">"""

    # Collect all valid entries
    entries = []
    for i in range(0, 65):
        if i in pages_with_images and (i+1) in titles:
            entries.append((i, titles[i+1], pages_with_images[i]))

    # Calculate the number of entries per column
    entries_per_column = len(entries) // 3
    if len(entries) % 3 != 0:
        entries_per_column += 1  # Round up to ensure all entries are included

    # Generate all three columns
    for col in range(3):
        start_idx = col * entries_per_column
        end_idx = min((col + 1) * entries_per_column, len(entries))

        html += '<div class="column">'
        for i, title, page in entries[start_idx:end_idx]:
            html += f'''
                <div class="toc-entry">
                    <span class="title">{i+1:02d} {title['hex']} {title['name']}</span>
                    <span class="dots"></span>
                    <span class="page">{page}</span>
                </div>'''
        html += '</div>'

    html += '</div></body></html>'
    return html




def extract_page_numbers(pdf_path):
    """Extracts page numbers from pages containing images."""
    doc = fitz.open(pdf_path)
    image_pages = {}
    index = 0  # Counter for dictionary keys

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)  # Get all images on the page
        # pprint(images)


        if images:  # If images exist on the page
            text = page.get_text()
            # Look for "Page X of Y" pattern
            match = re.search(r'Page (\d+) of \d+', text)
            if match:
                actual_page = int(match.group(1))
                image_pages[index] = actual_page
                index += 1

    return dict(sorted(image_pages.items()))

def get_hexagram_titles(directory="../regen"):
    """
    Extracts titles from hexagram JSON files.

    Args:
        directory (str): Path to directory containing JSON files

    Returns:
        dict: Dictionary with hexagram IDs as keys and names as values
    """
    titles = {}

    # Get all JSON files in the directory
    json_files = glob.glob(os.path.join(directory, "*.json"))

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Get the id and name from the nested structure
                titles[data['id']] = {
                    'name': data['name'],
                    'hex': data['hexagram_code']
                }
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading {file_path}: {e}")
            continue

    # Remove key 0 if it exists
    return dict(sorted(titles.items()))

# Example usage
# pdf_file = "../includes/FINAL_iching.pdf"  # Change this to your actual file path
pdf_file = "../includes/iching.pdf"  # Change this to your actual file path
pages_with_images = extract_page_numbers(pdf_file)

# Print results
# print("Pages with images:", pages_with_images)

# Get and print hexagram titles
titles = get_hexagram_titles()
# print("\nHexagram titles:", titles)



# Usage example:
def generate_toc(titles, pages_with_images, output_file):
    html_content = create_toc_html(titles, pages_with_images)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

# Example usage:
# Assuming you have your titles and pages_with_images dictionaries:
# generate_toc(titles, pages_with_images, "table_of_contents.html")



generate_toc(titles, pages_with_images, "../includes/TOC.html")
print("TOC generated in ../includes/TOC.html")

pprint(pages_with_images)
pprint(titles)


# with open("../includes/TOC.md", "w", encoding="utf-8") as f:
#     f.write("# Table of Contents\n\n")
#     f.write("| Hexagram | Page |\n")
#     f.write("|:---------|-----:|\n")
#     for i in range(0, 65):
#         if i in pages_with_images and i in titles:
#             title = f"Hexagram {i+1:02d}: {titles[i+1]}"
#             # Make the dots fill the entire remaining space (adjust 60 to match your desired width)
#             dots = '.' * (60 - len(title) - len(str(pages_with_images[i])))
#             f.write(f"| {title}{dots} | {pages_with_images[i]} |\n")

# for i in range(0, 65):
#     if i in pages_with_images and i in titles:
#         # print(f"Hexagram {i+1:02d}: {titles[i+1]:40s} {pages_with_images[i]}")
#         print(f"Hexagram {i+1:02d}: {titles[i+1]}{('.' * (30 - len(titles[i+1])))} {pages_with_images[i]}")
