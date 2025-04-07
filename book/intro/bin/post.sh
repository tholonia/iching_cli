#!/bin/bash
# =============================================================================
# post.sh - I Ching Introduction Document Post-Processing Script
# =============================================================================
#
# Description:
#     Post-processes the I Ching introduction document by converting HTML
#     files to PDF format, merging multiple PDF files, and creating the final
#     document. This script handles PDF generation, page manipulation, and
#     document assembly.
#
# Usage:
#     ./post.sh [BOOK|PDF] [--small]
#
# Options:
#     BOOK|PDF   - Output format (defaults to PDF if not specified)
#     --small    - Use small image version (iching_intro_sm.md) as input
#
# Process:
#     1. HTML Cleaning - Removes calc() lines that might cause issues
#     2. PDF Generation - Converts HTML to PDF using prince-books
#     3. Page Manipulation - Adjusts page ordering with pdftk
#     4. Document Assembly - Merges component PDFs into final document
#     5. Document Preview - Opens final PDF in viewer
#
# Files Processed:
#     - iching_intro.html → iching_intro.pdf (or iching_intro_sm.html if --small)
#     - COPYRIGHT.html → COPYRIGHT.pdf
#     - Various cover and content PDFs merged into final document
#
# Dependencies:
#     - prince-books: HTML to PDF converter
#     - pdftk: PDF manipulation tool
#     - okular: PDF viewer
#
# Directory Structure:
#     - ../Latest/: Contains generated HTML and PDF files
#     - ../Styles/: Contains CSS style files
#     - ../content/: Contains cover pages and other assets
#
# Notes:
#     - Uses blank page templates for proper pagination
#     - Page size is determined by CURRENT_SIZE variable (8.25x11)
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Parse command line arguments
FORMAT="PDF"  # Default to PDF if no format specified
SMALL=false   # Default to standard version

# Parse all arguments
for arg in "$@"; do
  case $arg in
    BOOK|PDF)
      FORMAT="$arg"
      ;;
    --small)
      SMALL=true
      ;;
    *)
      echo -e "\033[31mError: Invalid argument '$arg'. Valid formats are BOOK or PDF with optional --small.\033[0m"
      echo -e "Usage: $0 [BOOK|PDF] [--small]"
      exit 1
      ;;
  esac
done

# Set input file based on --small flag
if [ "$SMALL" = true ]; then
  INPUT_BASE="iching_intro_sm"
  echo -e "\033[34mUsing small image version: ${INPUT_BASE}\033[0m"
else
  INPUT_BASE="iching_intro"
fi

# Constants and configuration

#! the size is just for file names, the actual size is 6.69x9.61
#! Only change size in LESS file to change output size
PROD_PAGE_SIZE="6.69x9.61"

PAGE_SIZE="${PROD_PAGE_SIZE}"
BASE_DIR="/home/jw/src/iching_cli/book/intro"
SCRIPT_DIR="${BASE_DIR}/bin"
CONTENT_DIR="${BASE_DIR}/content"
LATEST_DIR="${BASE_DIR}/Latest"
STYLES_DIR="${BASE_DIR}/Styles"
BLANK_PAGE="${CONTENT_DIR}/blank_${PAGE_SIZE}.pdf"
OUTPUT_NAME="FINAL_iching_intro"
if [ "$SMALL" = true ]; then
  OUTPUT_NAME="FINAL_iching_intro_sm"
fi
TEMP_DIR="/tmp"

# Create required directories
mkdir -p "${LATEST_DIR}"

function rmx() {
    echo "Deleting: ${1}"
    rm -f "${1}"
}

# Cleanup previous run
function cleanup_previous_files() {
    echo -e "\033[33mCleaning up previous files...\033[0m"
    rmx "${LATEST_DIR}/${OUTPUT_NAME}_${FORMAT}.pdf"
    rmx "${TEMP_DIR}/out.pdf"
    rmx "${TEMP_DIR}/html.pdf"
    rmx "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf"
    rmx "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf"
    rmx "${TEMP_DIR}/TOC_${FORMAT}.pdf"
    rmx "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf-cut.pdf"
    rmx "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf-cut.pdf"
    rmx "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf"
    rmx "${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    rmx "${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"
}

# Process an HTML document into PDF
function process_document() {
    local DOCUMENT="$1"
    local CSS_FILE="${2:-iching_intro.css}"
    local INPUT_HTML="${LATEST_DIR}/${DOCUMENT}.html"
    local OUTPUT_PDF="${LATEST_DIR}/${DOCUMENT}.pdf"
    local TEMP_HTML="${TEMP_DIR}/html.tmp"

    echo -e "\033[35mProcessing ${DOCUMENT}\033[0m"

    # Remove calc() line to prevent rendering issues
    cp "${INPUT_HTML}" "${TEMP_HTML}"
    grep -v "calc(" "${TEMP_HTML}" > "${INPUT_HTML}"


    # cp "${INPUT_HTML}" "${TEMP_HTML}"
    # sed -E ':a;N;$!ba;s/<svg[^>]*>.*?<\/svg>//g' "${TEMP_HTML}" > "${INPUT_HTML}"

    # # Remove SVG line to prevent rendering issues
    # cp "${INPUT_HTML}" "${TEMP_HTML}"
    # grep -v -i "svg" "${TEMP_HTML}" > "${INPUT_HTML}"

    # Convert HTML to PDF
    set -x
    echo -e "\033[36mConverting to PDF...\033[0m"
    prince-books --verbose --no-warn-css --debug --log=debug.log  \
        --fail-dropped-content --fail-missing-resources --fail-missing-glyphs  \
        --input=html \
        --style="${STYLES_DIR}/${CSS_FILE}" \
        --media=print \
        -o "${OUTPUT_PDF}" \
        "${INPUT_HTML}"
    set +x
    # Check if PDF was created successfully
    if [ ! -f "${OUTPUT_PDF}" ]; then
        echo -e "\033[31mError: Failed to create ${OUTPUT_PDF}\033[0m"
        return 1
    fi

    echo -e "\033[32mCreated ${OUTPUT_PDF}\033[0m"
    return 0
}

# Process documents based on format
function process_documents_for_format() {
    echo -e "\033[33mProcessing documents for ${FORMAT} format...\033[0m"

    # Process main content
    #!--------------------------------------------------------------
    process_document "${INPUT_BASE}"
    #!--------------------------------------------------------------
    cp "${LATEST_DIR}/${INPUT_BASE}.pdf" "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf"
    pdftk "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf" cat 3-end output "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf-cut.pdf"
    cp "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf-cut.pdf" "${LATEST_DIR}/${INPUT_BASE}_${FORMAT}.pdf"

    # Process copyright
    set -x
#    process_document "COPYRIGHT"
    cp "${LATEST_DIR}/COPYRIGHT.pdf" "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf"
    if [ "$FORMAT" = "BOOK" ]; then
        pdftk "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf" cat 2-end output "${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    else
        pdftk "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf" cat 1-end output "${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    fi
    set +x
    # Process TOC with no page numbers
    #!--------------------------------------------------------------
    process_document "TOC" "iching_intro_nopage.css"
    #!--------------------------------------------------------------
    cp "${LATEST_DIR}/TOC.pdf" "${TEMP_DIR}/TOC_${FORMAT}.pdf"
    pdftk "${TEMP_DIR}/TOC_${FORMAT}.pdf" cat 3-end output "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf"
    pdftk "${BLANK_PAGE}" "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf" cat output "${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"

    echo -e "\033[32mAll documents processed successfully\033[0m"
}

# Set file references based on format
function set_format_files() {
    if [ "$FORMAT" = "BOOK" ]; then
        COVER=""
        COPYRIGHT="${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    else
        COVER="${CONTENT_DIR}/COVER_${PAGE_SIZE}.pdf"
        COPYRIGHT="${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    fi
}

# Merge all documents into final PDF
function merge_documents() {
    echo -e "\033[33mMerging documents into final PDF...\033[0m"

#    TOC="${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"
    TOC=""

    ICHING="${LATEST_DIR}/${INPUT_BASE}_${FORMAT}.pdf"
    OUTPUT="${LATEST_DIR}/${OUTPUT_NAME}_${FORMAT}.pdf"

    pdftk \
        ${COVER} \
        ${COPYRIGHT} \
        ${TOC} \
        ${ICHING} \
        cat output "${OUTPUT}"

    echo -e "\033[32mCreated final document: ${OUTPUT}\033[0m"
}

# Display the final document
function display_document() {
    echo -e "\033[33mOpening document for preview...\033[0m"
    okular "${LATEST_DIR}/${OUTPUT_NAME}_${FORMAT}.pdf"
}

# Main execution flow
function main() {
    # Start processing
    echo -e "\033[1;34mStarting document post-processing\033[0m"
    echo -e "\033[34mPage size: ${PAGE_SIZE}, Format: ${FORMAT}\033[0m"

    # Clean up previous files
    cleanup_previous_files

    # Process documents
    process_documents_for_format

    # Set format-specific files
    set_format_files

    # Merge documents
    merge_documents

    # Display the final document
    display_document

    echo -e "\033[1;32mPost-processing complete\033[0m"
}

# Run the main function
main

