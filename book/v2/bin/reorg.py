#!/bin/env python3

"""
PDF Page Reorganizer for I Ching Book

This script processes a PDF file containing I Ching hexagram entries and adds blank pages
before each hexagram to ensure proper double-sided printing layout. It's specifically
designed for book printing where hexagrams should start on right-hand (odd-numbered) pages.

Features:
1. Detects hexagram entries by looking for:
   - Unicode hexagram symbols (U+4DC0 to U+4DFF)
   - Large font titles in format "1 ䷀ 63 - Creation"
2. Inserts blank pages before hexagrams to ensure proper layout
3. Preserves first 3 pages (table of contents)
4. Only checks odd-numbered pages for hexagrams
5. Processes the PDF iteratively to handle large files
6. Maintains PDF dimensions and properties

Input:
    - PDF file with I Ching hexagram entries
    - Each hexagram entry starts with a title containing hexagram symbol
    - First 3 pages contain table of contents

Output:
    - Modified PDF with blank pages inserted
    - Hexagrams start on right-hand pages
    - Original content unchanged except for page positioning

Usage:
    reorg.py [-h] input_pdf output_pdf

    positional arguments:
      input_pdf    Path to input PDF file
      output_pdf   Path to output PDF file

Example:
    reorg.py docs/clean_iching.pdf docs/reorg.pdf

Dependencies:
    - PyMuPDF (fitz) for PDF content analysis
    - pdfrw for PDF manipulation
"""

import fitz  # PyMuPDF
from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfrw.buildxobj import pagexobj
import argparse

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Add blank pages before hexagrams in PDF for proper double-sided printing.'
    )
    parser.add_argument(
        'input_pdf',
        help='Path to input PDF file'
    )
    parser.add_argument(
        'output_pdf',
        help='Path to output PDF file'
    )
    return parser.parse_args()

def has_large_hexagram(page):
    """
    Check if a PDF page contains a hexagram title in the format:
    "1 ䷀ 63 - Creation" with font size > 20 and bold.

    Args:
        page: A PyMuPDF page object
    Returns:
        bool: True if the page contains a hexagram title
    """
    # Get all text blocks on the page
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    # Check for large bold font
                    if span["size"] > 20 and "bold" in span["font"].lower():
                        text = span["text"]
                        # Check for pattern: number + hexagram + number + hyphen + text
                        # First, check if there's a hexagram character
                        has_hexagram = any(0x4DC0 <= ord(c) <= 0x4DFF for c in text)
                        if has_hexagram:
                            # Then check if it matches our pattern
                            import re
                            pattern = r'^\d+\s+[\u4DC0-\u4DFF]\s+\d+\s+-\s+.+'
                            if re.match(pattern, text):
                                print(f"Found hexagram title: {text}")
                                return True
    return False

def create_blank_page(template_page):
    """
    Create a blank page with the same dimensions as the template page.

    Args:
        template_page: A pdfrw page object to use as a template for dimensions
    Returns:
        pdfrw.objects.pdfdict.PdfDict: A blank page with matching dimensions
    """
    try:
        # Get dimensions from template page
        template = pagexobj(template_page)
        width = float(template.BBox[2])
        height = float(template.BBox[3])

        # Create blank page with same dimensions
        blank = PageMerge()
        blank.mbox = (0, 0, width, height)
        return blank.render()
    except Exception as e:
        print(f"Error creating blank page: {str(e)}")
        raise

def has_notes_heading(page):
    """
    Check if a PDF page contains "Notes" as a heading.
    In the hexagram entries, "Notes" appears as a section header
    at the end of each 4-page hexagram entry.

    Args:
        page: A PyMuPDF page object
    Returns:
        bool: True if the page contains a Notes heading
    """
    # Get all text blocks on the page
    blocks = page.get_text("dict")["blocks"]

    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text == "Notes":
                        print(f"Found Notes heading")
                        return True
    return False

def has_hexagram_symbol(page):
    """
    Check if a PDF page contains any hexagram Unicode symbol (U+4DC0 to U+4DFF).
    Only reports the first hexagram found on the page.

    Args:
        page: A PyMuPDF page object
    Returns:
        bool: True if the page contains a hexagram symbol
    """
    blocks = page.get_text("dict")["blocks"]

    found_on_page = False
    for block in blocks:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"]
                    if any(0x4DC0 <= ord(c) <= 0x4DFF for c in text):
                        if not found_on_page:  # Only print first hexagram found
                            print(f"Found hexagram symbol: {text}")
                            found_on_page = True
                        return True  # Exit after finding first hexagram
    return False

def process_pdf_iteratively(input_path, output_path):
    """
    Process PDF file one hexagram at a time, saving and reopening between each change.
    Skips first 3 pages (table of contents).
    Only checks odd-numbered pages for hexagrams.
    """
    print(f"Starting with input PDF: {input_path}")

    # Make initial copy
    current_file = input_path
    temp_file = "docs/temp_working.pdf"
    final_file = output_path

    total_pages_added = 0
    hexagrams_found = 0

    while True:
        try:
            # Open current version of the PDF
            reader = PdfReader(current_file)
            doc = fitz.open(current_file)
            writer = PdfWriter()

            found_hexagram = False

            # Process each page
            for i in range(len(reader.pages)):
                current_page = i + 1

                # Skip first 3 pages and even pages
                if i < 3 or current_page % 2 == 0:
                    writer.addpage(reader.pages[i])
                    continue

                # Only check odd pages for hexagrams
                if not found_hexagram and has_hexagram_symbol(doc[i]):
                    hexagrams_found += 1
                    print(f"Found hexagram #{hexagrams_found} on page {current_page}")
                    print(f"Adding blank page before odd page {current_page}")
                    blank_page = create_blank_page(reader.pages[i])
                    writer.addpage(blank_page)
                    total_pages_added += 1
                    found_hexagram = True

                # Add the current page
                writer.addpage(reader.pages[i])

            # Save to temp file
            writer.write(temp_file)
            doc.close()

            # If we didn't find any hexagrams, we're done
            if not found_hexagram:
                print("\nNo more hexagrams found")
                # Move temp file to final output
                import shutil
                shutil.move(temp_file, final_file)
                break

            # Otherwise, continue with temp file as input
            current_file = temp_file

        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            raise

    print(f"\nFinal Summary:")
    print(f"Total hexagrams found: {hexagrams_found}")
    print(f"Total blank pages added: {total_pages_added}")
    print(f"Processing complete. Output saved to: {final_file}")
    return total_pages_added

if __name__ == "__main__":
    args = parse_args()
    try:
        pages_added = process_pdf_iteratively(args.input_pdf, args.output_pdf)
    except Exception as e:
        print(f"An error occurred: {str(e)}")