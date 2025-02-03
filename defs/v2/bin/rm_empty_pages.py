#!/bin/env python

"""
This script removes empty pages from PDF files while preserving the document structure.
Key features:
- Detects and removes pages that contain no text
- Preserves PDF outline/bookmarks, updating page references
- Maintains original metadata
- Creates a new PDF with 'clean_' prefix
- Prints information about removed pages

"""

from PyPDF2 import PdfReader, PdfWriter
import os
import sys

def remove_empty_pages(input_path, output_path):
    """
    Remove empty pages from a PDF file while preserving the outline/bookmarks.

    Args:
        input_path (str): Path to input PDF file
        output_path (str): Path to save the output PDF file
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # Create a mapping of old page numbers to new page numbers
    page_map = {}
    new_page_num = 0

    for old_page_num, page in enumerate(reader.pages):
        # Extract text from the page
        text = page.extract_text().strip()

        # Check if page has any text content
        if len(text) > 0:
            writer.add_page(page)
            page_map[old_page_num] = new_page_num
            new_page_num += 1
        else:
            print(f"Empty page found: {old_page_num}")

    # Get the outline from the original PDF
    outline = reader.outline
    if outline:
        # Function to update page numbers in outline items
        def update_outline_page_numbers(outline_item):
            if isinstance(outline_item, list):
                return [update_outline_page_numbers(item) for item in outline_item]

            if hasattr(outline_item, '_page'):
                # Find the original page number
                original_page_num = outline_item._page.page_number
                # Update to new page number if it exists in the mapping
                if original_page_num in page_map:
                    outline_item._page = writer.pages[page_map[original_page_num]]
                    return outline_item
                return None
            return outline_item

        # Update the outline with new page numbers
        updated_outline = update_outline_page_numbers(outline)
        # Remove None entries (bookmarks pointing to removed pages)
        def clean_outline(outline_items):
            if not isinstance(outline_items, list):
                return outline_items
            return [clean_outline(item) for item in outline_items if item is not None]

        cleaned_outline = clean_outline(updated_outline)
        writer.outline = cleaned_outline

    # Preserve metadata from the original PDF
    metadata = reader.metadata
    if metadata:
        writer.add_metadata(metadata)

    # Save the new PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input.pdf")
        sys.exit(1)

    input_file = sys.argv[1]

    # Get the directory and filename
    directory = os.path.dirname(input_file)
    filename = os.path.basename(input_file)

    # Create output filename with 'clean_' prefix
    output_file = os.path.join(directory, f"clean_{filename}")

    try:
        remove_empty_pages(input_file, output_file)
        print(f"Successfully created: {output_file}")
    except Exception as e:
        print(f"Error processing PDF: {e}")
        sys.exit(1)