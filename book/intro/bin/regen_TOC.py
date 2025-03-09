#!/usr/bin/env python
import fitz  # PyMuPDF
import re
import glob
import os
import json
from pprint import pprint  # For debug printing
from colorama import Fore, Style, init  # For colored terminal output

# Initialize colorama
init()

"""
=============================================================================
regen_TOC.py - Table of Contents Generator for I Ching Book
=============================================================================

Description:
    Generates a formatted HTML table of contents for the I Ching book by:
    1. Extracting page numbers from PDF where hexagram images appear
    2. Reading hexagram titles and codes from JSON files
    3. Creating a three-column HTML layout with dotted leazders

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

def create_toc_html(pages_with_data):
    # Start with HTML header including CSS styles
    html = """<!DOCTYPE html>
<html>
<div style="page-break-before: always;"></div>
<head>
    <style>
        .container {
            max-width: 800px;
            margin: 0 auto;
            font-family: serif;
        }

        .column {
            width: 100%;
        }

        .toc-entry {
            display: flex;
            align-items: baseline;
            margin: 8px 0;
            font-size: 10pt;
        }

        .title {
            white-space: nowrap;
            max-width: 80%;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .title-main {
            font-weight: bold;
        }

        .title-sub {
            font-weight: normal;
            margin-left: 15px;
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

    # Use the extracted page data directly
    entries = []
    for idx, data in pages_with_data.items():
        entries.append((data["title"], data["page"], data.get("type", "title")))

    # Sort entries by page number
    entries.sort(key=lambda x: x[1])

    # Single column - no need to divide entries
    html += '<div class="column">'
    for title, page, entry_type in entries:
        title_class = "title-main" if entry_type == "title" else "title-sub"
        html += f'''
            <div class="toc-entry">
                <span class="title {title_class}">{title}</span>
                <span class="dots"></span>
                <span class="page">{page}</span>
            </div>'''
    html += '</div>'

    html += '</div></body></html>'
    return html

def extract_page_numbers(pdf_path):
    """Extracts page numbers and titles from PDF pages using specific font size."""
    doc = fitz.open(pdf_path)
    page_data = {}
    index = 0  # Counter for dictionary keys

    # Define the font sizes for titles and subtitles
    title_size = 22  # Font size for main titles
    subtitle_size = 18  # Font size for subtitles

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        # Extract title based on specific font size range
        blocks = page.get_text("dict")["blocks"]

        # Get the page number first
        match = re.search(r'Page (\d+) of \d+', text)
        if not match:
            continue

        actual_page = int(match.group(1))

        # Track separate titles on the same page
        titles_on_page = []
        current_title = []
        current_font_size = 0
        last_y = -1

        # Find text with title or subtitle font size
        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_has_heading = False
                line_text = []
                line_font_size = 0

                for span in line["spans"]:
                    # Check if font size is title or subtitle and doesn't contain "Untitled"
                    if ((span["size"] == title_size or span["size"] == subtitle_size) and
                        span["text"].strip() and
                        "Untitled" not in span["text"]):
                        line_text.append(span["text"].strip())
                        line_has_heading = True
                        line_font_size = span["size"]  # Save font size for categorization

                # If this line has title text
                if line_has_heading:
                    # If y position changed significantly or font size changed, it's a new heading
                    y = line["bbox"][1]  # y-coordinate of the line
                    if (last_y != -1 and (abs(y - last_y) > 20 or current_font_size != line_font_size)):
                        if current_title:
                            titles_on_page.append({
                                "text": " ".join(current_title),
                                "type": "title" if current_font_size == title_size else "subtitle"
                            })
                            current_title = []

                    current_title.extend(line_text)
                    current_font_size = line_font_size
                    last_y = y

        # Add the last title if there is one
        if current_title:
            titles_on_page.append({
                "text": " ".join(current_title),
                "type": "title" if current_font_size == title_size else "subtitle"
            })

        # Add each title as a separate entry with the same page number
        for heading in titles_on_page:
            page_data[index] = {
                "page": actual_page,
                "title": heading["text"],
                "type": heading["type"]
            }
            index += 1

    return dict(sorted(page_data.items()))

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

def generate_toc(pages_with_data, output_file):
    html_content = create_toc_html(pages_with_data)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

# Example usage
# pdf_file = "../includes/FINAL_iching.pdf"  # Change this to your actual file path
pdf_file = "../Latest/iching_intro.pdf"  # Change this to your actual file path
pages_with_images = extract_page_numbers(pdf_file)

# Print results
# print("Pages with images:", pages_with_images)

# Get and print hexagram titles
titles = get_hexagram_titles()
# print("\nHexagram titles:", titles)

generate_toc(pages_with_images, "../Latest/TOC.html")
print("TOC generated in ../Latest/TOC.html")

pprint(pages_with_images)
pprint(titles)

