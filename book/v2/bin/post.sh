#!/bin/bash

# =============================================================================
# post.sh - I Ching Book PDF Generation Script
# =============================================================================
#
# Description:
#   This script automates the process of generating a final PDF document for
#   the I Ching book. It handles HTML to PDF conversion, table of contents
#   generation, and merging of various document sections.
#
# Process:
#   1. Removes any existing final PDF to ensure a clean build
#   2. Uses Prince to convert HTML content into PDF with:
#      - Proper page styling
#      - Automatic table of contents generation
#      - Bookmark levels for navigation
#   3. Merges additional pages into the final PDF using pdftk
#   4. Opens the final PDF in Okular for review
#
# Usage:
#   ./post.sh
#
# Dependencies:
#   - Prince: HTML to PDF conversion with TOC support
#     Required flags: --prince-toc for TOC generation
#   - pdftk: PDF manipulation tool
#   - Okular: PDF viewer
#
# Input Files:
#   - COVER_PAGE.pdf: Book cover
#   - COPYRIGHT_PAGE.pdf: Copyright information
#   - iching.html: Main content with TOC nav element
#   - iching.css: Styling with Prince-specific TOC properties
#
# Output:
#   - FINAL_iching.pdf: Complete book with:
#     - Cover page
#     - Copyright page
#     - Table of contents
#     - Main content
#
# TOC Requirements:
#   - HTML must include nav element with role="doc-toc"
#   - CSS must define prince-bookmark-level for headings
#   - Prince must be run with --prince-toc flag
#
# Example TOC Structure:
#   <nav role="doc-toc">
#     <h1>Table of Contents</h1>
#     <ol>
#       <li><a href="#chapter-1">Chapter 1</a></li>
#     </ol>
#   </nav>
#
# Author: JW
# Last Updated: 2024
# =============================================================================

#./makeallmd.py
#typora docs/iching.md

# makebook_postonly.sh

# This script automates the process of generating a final PDF document for the I Ching book.
# It performs the following steps:
# 1. Removes any existing final PDF to ensure a clean build.
# 2. Uses Prince to convert HTML content into a PDF, applying specific styles for print.
# 3. Merges additional pages (cover and copyright) into the final PDF using pdftk.
# 4. Opens the final PDF in Okular for review.

# Steps:
# 1. Remove the existing FINAL_iching.pdf to avoid conflicts with previous builds.
# 2. Use Prince to convert iching.html to iching.pdf, applying styles from iching.css.
# 3. Merge COVER_PAGE.pdf and COPYRIGHT_PAGE.pdf with iching.pdf to create FINAL_iching.pdf.
# 4. Open the resulting FINAL_iching.pdf in Okular for viewing.

# Usage:
# Run this script from the command line to generate and view the final I Ching book PDF.

# Dependencies:
# - Prince: A tool for converting HTML and CSS to PDF.
# - pdftk: A tool for manipulating PDF documents.
# - Okular: A PDF viewer for reviewing the final document.

# Note:
# Ensure all input files (COVER_PAGE.pdf, COPYRIGHT_PAGE.pdf, iching.html) are present in the expected directories.

D="/home/jw/src/iching_cli/book/v2/bin"
BREAK='<div style="page-break-before: always;"></div>'

# Function to process HTML documents into PDFs
#
# This function processes an HTML document by:
# 1. Creating a temporary copy of the HTML file
# 2. Removing any 'calc()' lines that might cause issues
# 3. Generating a PDF using prince-books with specified styling
#
# Usage:
#   process_document "document_name" ["style_file"]
#
# Parameters:
#   $1 - Document name without extension (required)
#   $2 - CSS style file name (optional, defaults to iching.css)
#
# Example:
#   process_document "COPYRIGHT_PAGE_v1" "iching_nopage.css"
#   process_document "BOOK_INTRO"


#BLANK=${D}/../includes/blank_8.3x11.7.pdf
BLANK=${D}/../includes/blank_8.5x11.pdf

function process_document() {
    local DOCUMENT="$1"

    echo -e "\033[35mProcessing ${DOCUMENT}\033[0m"

    # delete calc() line
    cp ${D}/../includes/${DOCUMENT}.html /tmp/html.tmp
    cat /tmp/html.tmp | grep -v "calc(" > ${D}/../includes/${DOCUMENT}.html

    # make PDF
    rm -f ${D}/../includes/${DOCUMENT}.pdf
    set -x
    prince-books \
        --style=${D}/../includes/${2:-iching.css} \
        --media=print \
        -o ${D}/../includes/${DOCUMENT}.pdf \
        ${D}/../includes/${DOCUMENT}.html #2>> /tmp/prince.log
    set +x
}

rm -f ${D}/../includes/FINAL_iching.pdf
rm -f /tmp/out.pdf
rm -f /tmp/html.pdf

#^ PROCESS: TOC.html > TOC.pdf
#! make sure the HTML output was generated with teh 'nopages' CSS to avoid page numbers
process_document "TOC" "iching_nopage.css" # make PDF from HTML
cp ${D}/../includes/TOC.pdf /tmp/TOC.pdf
pdftk /tmp/TOC.pdf cat 3-end output  /tmp//TOC-cut.pdf
# insert 2 blank pages
pdftk ${BLANK} /tmp/TOC-cut.pdf cat output ${D}/../includes/FINAL_TOC.pdf

#^ PROCESS: COPYRIGHT_PAGE_v1.html > COPYRIGHT_PAGE_v1.pdf
#! make sure the HTML output was generated with teh 'nopages' CSS to avoid page numbers
process_document "COPYRIGHT_PAGE_v1" "iching_nopage.css"
cp ${D}/../includes/COPYRIGHT_PAGE_v1.pdf /tmp/COPYRIGHT_PAGE_v1.pdf
pdftk /tmp/COPYRIGHT_PAGE_v1.pdf cat 5-end output  /tmp//COPYRIGHT_PAGE_v1-cut.pdf
# insert 2 blank pages
pdftk ${BLANK} /tmp/COPYRIGHT_PAGE_v1-cut.pdf cat output ${D}/../includes/COPYRIGHT_PAGE_v1.pdf


#^ PROCESS: BOOK_INTRO.html > BOOK_INTRO.pdf
#! make sure the HTML output was generated with teh 'nopages' CSS to avoid page numbers
process_document "BOOK_INTRO"
cp ${D}/../includes/BOOK_INTRO.pdf /tmp/BOOK_INTRO.pdf
pdftk /tmp/BOOK_INTRO.pdf cat 3-end output  /tmp/BOOK_INTRO-cut.pdf
# insert 1 blank pages
pdftk ${BLANK} /tmp/BOOK_INTRO-cut.pdf cat output ${D}/../includes/BOOK_INTRO.pdf

#^ PROCESS: iching.html > iching.pdf
process_document "iching"
cp ${D}/../includes/iching.pdf /tmp/iching.pdf
pdftk /tmp/iching.pdf cat 3-end output  /tmp/iching-cut.pdf
# insert 1 blank pages

pdftk ${BLANK} /tmp/iching-cut.pdf cat output ${D}/../includes/iching.pdf



#~-----------------------------------------------------------------------------------
echo -e "\033[33mMerging...\033[0m"

#COVER=${D}/../includes/COVER_PAGE_8.5x11.pdf
#COVER=${D}/../includes/COVER_v1.pdf
COVER=${D}/../includes/COVER_v2.pdf

# add copyright and cover to PDF
# - q8_iching_png.pdf and bin/q8_iching_png.pdf are premade from PNG/PSD files

pdftk \
    ${COVER} \
    ${D}/../includes/COPYRIGHT_PAGE_v1.pdf \
    ${D}/../includes/BOOK_INTRO.pdf \
    ${D}/../includes/q8_iching_png.pdf \
    ${D}/../includes/binhex4col_png.pdf \
    ${D}/../includes/FINAL_TOC.pdf \
    ${D}/../includes/iching.pdf \
    cat output ${D}/../includes/FINAL_iching.pdf

# pdftk \
#     ${D}/../includes/COVER_PAGE_8.5x11.pdf \
#     ${D}/../includes/COPYRIGHT_PAGE_v1.pdf \
#     ${D}/../includes/BOOK_INTRO.pdf \
#     ${D}/../includes/FINAL_TOC.pdf \
#     ${D}/../includes/iching.pdf \
#     cat output ${D}/../includes/FINAL_iching.pdf

okular ${D}/../includes/FINAL_iching.pdf

