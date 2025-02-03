#!/bin/env python3

import fitz  # PyMuPDF
from pdfrw import PdfReader, PdfWriter, PageMerge
from pdfrw.buildxobj import pagexobj

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
    input_file = "docs/clean_iching.pdf"
    output_file = "docs/reorg.pdf"

    try:
        pages_added = process_pdf_iteratively(input_file, output_file)
    except Exception as e:
        print(f"An error occurred: {str(e)}")