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

# Enable better error handling
set -o pipefail

# Parse command line arguments
FORMAT="PDF"  # Default to PDF if no format specified

# Check if a format was provided as an argument
if [ $# -ge 1 ]; then
    if [ "$1" = "BOOK" ] || [ "$1" = "PDF" ]; then
        FORMAT="$1"
    else
        echo -e "\033[31mError: Invalid format '$1'. Valid formats are BOOK or PDF.\033[0m"
        echo -e "Usage: $0 [BOOK|PDF]"
        exit 1
    fi
fi

# Constants and configuration
D="/home/jw/src/iching_cli/book/v2/bin"
CURRENT_SIZE="8.25x11"
BLANK="${D}/../includes/blank_${CURRENT_SIZE}.pdf"
TEMP_DIR="/tmp/iching_book_$$"  # Use PID for isolation

# Create required directories
mkdir -p "${TEMP_DIR}"

# Trap for cleaning up on exit
trap 'rm -rf "${TEMP_DIR}"' EXIT INT TERM

# Function to process HTML documents into PDFs
function process_document() {
    local DOCUMENT="$1"
    local CSS_FILE="${2:-iching.css}"

    echo -e "\033[35mProcessing ${DOCUMENT}\033[0m"

    # Verify input file exists
    if [ ! -f "${D}/../includes/${DOCUMENT}.html" ]; then
        echo -e "\033[31mError: Input file ${D}/../includes/${DOCUMENT}.html not found\033[0m"
        return 1
    fi

    # Create temporary HTML without calc() lines
    cp "${D}/../includes/${DOCUMENT}.html" "${TEMP_DIR}/current.html"
    grep -v "calc(" "${TEMP_DIR}/current.html" > "${D}/../includes/${DOCUMENT}.html"

    # Make PDF
    rm -f "${D}/../includes/${DOCUMENT}.pdf"

    echo -e "\033[36mConverting ${DOCUMENT} to PDF using ${CSS_FILE}...\033[0m"

    if prince-books \
        --style="${D}/../includes/${CSS_FILE}" \
        --media=print \
        -o "${D}/../includes/${DOCUMENT}.pdf" \
        "${D}/../includes/${DOCUMENT}.html"; then

        echo -e "\033[32m✓ Created ${DOCUMENT}.pdf\033[0m"
        return 0
    else
        echo -e "\033[31m✗ Failed to create ${DOCUMENT}.pdf\033[0m"
        return 1
    fi
}

# Cleanup previous files
function cleanup_previous_files() {
    echo -e "\033[33mCleaning up previous files...\033[0m"
    rm -f "${D}/../includes/FINAL_iching.pdf"
    rm -f "${D}/../includes/FINAL_iching_${FORMAT}.pdf"
    rm -f "${TEMP_DIR}/out.pdf"
    rm -f "${TEMP_DIR}/html.pdf"
    rm -f "${TEMP_DIR}/TOC_${FORMAT}.pdf"
    rm -f "${TEMP_DIR}/TOC_${FORMAT}-cut.pdf"
    rm -f "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf"
    rm -f "${TEMP_DIR}/COPYRIGHT_${FORMAT}-cut.pdf"
    rm -f "${TEMP_DIR}/BOOK_INTRO_${FORMAT}.pdf"
    rm -f "${TEMP_DIR}/BOOK_INTRO_${FORMAT}-cut.pdf"
    rm -f "${TEMP_DIR}/iching_${FORMAT}.pdf"
    rm -f "${TEMP_DIR}/iching_${FORMAT}-cut.pdf"
    rm -f "${D}/../includes/FINAL_TOC_${FORMAT}.pdf"
    rm -f "${D}/../includes/COPYRIGHT_PAGE_v1_${FORMAT}.pdf"
    rm -f "${D}/../includes/BOOK_INTRO_${FORMAT}.pdf"
    rm -f "${D}/../includes/iching_${FORMAT}.pdf"
}

# Process all documents for the selected format
function process_documents() {
    local status=0

    echo -e "\033[1;34mProcessing documents for ${FORMAT} format\033[0m"

    # Process TOC
    echo -e "\033[34mProcessing Table of Contents...\033[0m"
    if ! process_document "TOC" "iching_nopage.css"; then
        echo -e "\033[31mFailed to process TOC\033[0m"
        status=1
    else
        cp "${D}/../includes/TOC.pdf" "${TEMP_DIR}/TOC_${FORMAT}.pdf"
        pdftk "${TEMP_DIR}/TOC_${FORMAT}.pdf" cat 3-end output "${TEMP_DIR}/TOC_${FORMAT}-cut.pdf"
        pdftk "${BLANK}" "${TEMP_DIR}/TOC_${FORMAT}-cut.pdf" cat output "${D}/../includes/FINAL_TOC_${FORMAT}.pdf"
    fi

    # Process COPYRIGHT
    echo -e "\033[34mProcessing Copyright Page...\033[0m"
    # if ! process_document "COPYRIGHT" "iching_nopage.css"; then
    #     echo -e "\033[31mFailed to process COPYRIGHT\033[0m"
    #     status=1
    # else
    cp "${D}/../includes/COPYRIGHT.pdf" "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf"
    pdftk "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf" cat 2-end output "${TEMP_DIR}/COPYRIGHT_${FORMAT}-cut.pdf"

    if [ "${FORMAT}" = "PDF" ]; then
        pdftk "${BLANK}" "${TEMP_DIR}/COPYRIGHT_${FORMAT}-cut.pdf" cat output "${D}/../includes/COPYRIGHT_${FORMAT}.pdf"
    else
        cp "${TEMP_DIR}/COPYRIGHT_${FORMAT}-cut.pdf" "${D}/../includes/COPYRIGHT_${FORMAT}.pdf"
    fi
    # fi

    # Process BOOK_INTRO
    echo -e "\033[34mProcessing Book Introduction...\033[0m"
    if ! process_document "BOOK_INTRO"; then
        echo -e "\033[31mFailed to process BOOK_INTRO\033[0m"
        status=1
    else
        cp "${D}/../includes/BOOK_INTRO.pdf" "${TEMP_DIR}/BOOK_INTRO_${FORMAT}.pdf"
        pdftk "${TEMP_DIR}/BOOK_INTRO_${FORMAT}.pdf" cat 3-end output "${TEMP_DIR}/BOOK_INTRO_${FORMAT}-cut.pdf"
        pdftk "${BLANK}" "${TEMP_DIR}/BOOK_INTRO_${FORMAT}-cut.pdf" cat output "${D}/../includes/BOOK_INTRO_${FORMAT}.pdf"
    fi

    # Process main content
    echo -e "\033[34mProcessing Main Content...\033[0m"
    if ! process_document "iching"; then
        echo -e "\033[31mFailed to process iching\033[0m"
        status=1
    else
        cp "${D}/../includes/iching.pdf" "${TEMP_DIR}/iching_${FORMAT}.pdf"
        pdftk "${TEMP_DIR}/iching_${FORMAT}.pdf" cat 3-end output "${TEMP_DIR}/iching_${FORMAT}-cut.pdf"
        pdftk "${BLANK}" "${TEMP_DIR}/iching_${FORMAT}-cut.pdf" cat output "${D}/../includes/iching_${FORMAT}.pdf"
    fi

    return $status
}

# Merge all components into final PDF
function merge_documents() {
    echo -e "\033[33mMerging documents into final PDF...\033[0m"

    # Define component files
    COVER="${D}/../includes/_COVER_v2_${CURRENT_SIZE}.pdf"
    COPYRIGHT="${D}/../includes/COPYRIGHT_${FORMAT}.pdf"
    BOOK="${D}/../includes/BOOK_INTRO_${FORMAT}.pdf"
    Q8="${D}/../includes/_q8_iching_${CURRENT_SIZE}_png.pdf"
    BIN="${D}/../includes/_binhex4col_${CURRENT_SIZE}_png.pdf"
    PATHS="${D}/../includes/_32paths_${CURRENT_SIZE}_png.pdf"
    TOC="${D}/../includes/FINAL_TOC_${FORMAT}.pdf"
    ICHING="${D}/../includes/iching_${FORMAT}.pdf"
    OUTPUT="${D}/../includes/FINAL_iching_${FORMAT}.pdf"



    if [ "${FORMAT}" = "BOOK" ]; then
        echo -e "\033[33mSkipping cover page for BOOK format\033[0m"
        COVER=""
    fi



    # Verify all files exist
    for file in  "${COPYRIGHT}" "${BOOK}" "${Q8}" "${BIN}" "${PATHS}" "${TOC}" "${ICHING}"; do
        if [ ! -f "$file" ]; then
            echo -e "\033[31mError: Required file |$file| not found\033[0m"
            return 1
        else
            echo -e "\033[32m✓ Found file |$file|\033[0m"
        fi
    done



    set -x


    # Merge files
    if pdftk \
        ${COVER} \
        ${COPYRIGHT} \
        ${BOOK} \
        ${Q8} \
        ${BIN} \
        ${PATHS} \
        ${TOC} \
        ${ICHING} \
        cat output "${OUTPUT}"; then

        echo -e "\033[32mSuccessfully created ${OUTPUT}\033[0m"
        return 0
    else
        echo -e "\033[31mFailed to create final document\033[0m"
        return 1
    fi
    set +x
}

# Open the final PDF
function display_document() {
    local PDF_FILE="${D}/../includes/FINAL_iching_${FORMAT}.pdf"

    if [ ! -f "${PDF_FILE}" ]; then
        echo -e "\033[31mError: Final PDF ${PDF_FILE} not found\033[0m"
        return 1
    fi

    echo -e "\033[33mOpening document for preview...\033[0m"
    if command -v okular >/dev/null 2>&1; then
        okular "${PDF_FILE}" &
        return 0
    else
        echo -e "\033[33mOkular not found. PDF is at: ${PDF_FILE}\033[0m"
        return 1
    fi
}

# Main execution flow
function main() {
    local status=0

    # Start processing
    echo -e "\033[1;34mStarting I Ching Book PDF generation\033[0m"
    echo -e "\033[34mPage size: ${CURRENT_SIZE}, Format: ${FORMAT}\033[0m"

    # Clean up previous files
    cleanup_previous_files

    # Process documents
    if ! process_documents; then
        echo -e "\033[31mWarning: Some documents failed to process\033[0m"
        status=1
    fi

    # Merge documents
    if ! merge_documents; then
        echo -e "\033[31mError: Failed to merge documents\033[0m"
        status=1
    else
        # Display the final document
        if ! display_document; then
            echo -e "\033[33mWarning: Could not open PDF viewer\033[0m"
            # Don't fail the script just because viewer didn't open
        fi
    fi

    if [ $status -eq 0 ]; then
        echo -e "\033[1;32mI Ching Book PDF generation complete\033[0m"
    else
        echo -e "\033[1;31mI Ching Book PDF generation completed with errors\033[0m"
    fi

    return $status
}

# Run the main function
main
exit $?

