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
#   ./post.sh [BOOK|PDF] [--minimal] [--pagesize WIDTHxHEIGHT]
#
# Arguments:
#   BOOK|PDF: Format to generate (default: PDF)
#   --minimal: Only include the main content (iching) in the final document
#   --pagesize: Page dimensions in format WIDTHxHEIGHT (default: 8.25x11)
#              Examples: --pagesize 7.0x10.0, --pagesize 6.69x9.61
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

# Determine the numeric width/height and Prince page flag for a WIDTHxHEIGHT string
function determine_page_size_settings() {
    local size="$1"
    local width height prince_flag

    if [[ "$size" == *"x"* ]]; then
        IFS='x' read -r width height <<< "$size"
    else
        width="$size"
        height="$size"
    fi

    case "$size" in
        8.27x11.69)
            prince_flag="A4"
            ;;
        8.5x11|8.25x11)
            prince_flag="Letter"
            ;;
        *)
            prince_flag="${width}in ${height}in"
            ;;
    esac

    echo "${width}|${height}|${prince_flag}"
}

# Generate a blank single-page PDF at the requested dimensions
function create_blank_page_pdf() {
    local output_pdf="$1"
    local width="$2"
    local height="$3"
    local prince_flag="$4"
    local blank_html="${TEMP_DIR}/blank_${width}x${height}.html"

    cat > "${blank_html}" <<EOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>blank</title>
  <style>
    @page { size: ${width}in ${height}in !important; margin: 0; }
    body { margin: 0; }
  </style>
</head>
<body></body>
</html>
EOF

    if prince-books \
        --media=print \
        --page-size="${prince_flag}" \
        -o "${output_pdf}" \
        "${blank_html}"; then
        return 0
    else
        return 1
    fi
}

# Resize a PDF to match target dimensions (in inches)
function resize_pdf_to_size() {
    local input_pdf="$1"
    local output_pdf="$2"
    local width="$3"   # in inches
    local height="$4"  # in inches
    # Convert inches to points (1 inch = 72 points) using awk for floating point math
    local width_pt=$(awk "BEGIN {printf \"%.0f\", ${width} * 72}")
    local height_pt=$(awk "BEGIN {printf \"%.0f\", ${height} * 72}")
    
    if command -v gs >/dev/null 2>&1; then
        # Use ghostscript to resize
        if gs -sDEVICE=pdfwrite -dFIXEDMEDIA -dPDFFitPage \
           -dDEVICEWIDTHPOINTS="${width_pt}" \
           -dDEVICEHEIGHTPOINTS="${height_pt}" \
           -o "${output_pdf}" \
           "${input_pdf}" >/dev/null 2>&1; then
            return 0
        else
            return 1
        fi
    else
        # Fallback: just copy if ghostscript not available
        cp "${input_pdf}" "${output_pdf}"
        return 1
    fi
}

# Parse command line arguments
FORMAT="PDF"  # Default to PDF if no format specified
MINIMAL=false # Default to full document
PAGE_SIZE="8.25x11"  # Default page size

# Parse command line arguments
while (( "$#" )); do
  case "$1" in
    BOOK|PDF)
      FORMAT="$1"
      shift
      ;;
    --minimal)
      MINIMAL=true
      shift
      ;;
    --pagesize)
      if [ -n "$2" ] && [[ "$2" =~ ^[0-9]+\.?[0-9]*x[0-9]+\.?[0-9]*$ ]]; then
        PAGE_SIZE="$2"
        shift 2
      else
        echo -e "\033[31mError: Invalid page size format. Use format like '7.0x10.0'\033[0m"
        echo -e "Usage: $0 [BOOK|PDF] [--minimal] [--pagesize WIDTHxHEIGHT]"
        exit 1
      fi
      ;;
    *)
      echo -e "\033[31mError: Invalid argument '$1'\033[0m"
      echo -e "Usage: $0 [BOOK|PDF] [--minimal] [--pagesize WIDTHxHEIGHT]"
      exit 1
      ;;
  esac
done

# Constants and configuration
D="/home/jw/src/iching_cli/book/v2/bin"
CURRENT_SIZE="${PAGE_SIZE}"
BLANK="${D}/../includes/blank_${CURRENT_SIZE}.pdf"
TEMP_DIR="/tmp/iching_book_$$"  # Use PID for isolation

# Create required directories
mkdir -p "${TEMP_DIR}"

# Verify blank page exists
if [ ! -f "${BLANK}" ]; then
    echo -e "\033[31mError: Blank page not found: ${BLANK}\033[0m"
    echo -e "\033[33mAvailable blank pages:\033[0m"
    ls -1 "${D}/../includes/blank_"*.pdf 2>/dev/null || echo "  None found"
    exit 1
fi

# Trap for cleaning up on exit
trap 'rm -rf "${TEMP_DIR}"' EXIT INT TERM

# Function to ensure required files exist
function ensure_required_files() {
    local PAGE_SIZE="$1"
    
    # Create page-specific PDF files if they don't exist
    local FILES_TO_CREATE=(
        "_q8_iching_${PAGE_SIZE}_png.pdf"
        "_binhex4col_${PAGE_SIZE}_png.pdf"
        "_32paths_${PAGE_SIZE}_png.pdf"
        "_COVER_v2_${PAGE_SIZE}.pdf"
    )
    
    for file in "${FILES_TO_CREATE[@]}"; do
        local TARGET_FILE="${D}/../includes/${file}"
        if [ ! -f "${TARGET_FILE}" ]; then
            echo -e "\033[33mCreating missing file: ${file}\033[0m"
            # Find the closest existing file with similar name
            local BASE_NAME=$(echo "${file}" | sed "s/_${PAGE_SIZE}_/_8.25x11_/")
            local TEMPLATE_FILE="${D}/../includes/${BASE_NAME}"
            
            if [ -f "${TEMPLATE_FILE}" ]; then
                cp "${TEMPLATE_FILE}" "${TARGET_FILE}"
            else
                # Try A4 size as fallback
                local A4_NAME=$(echo "${file}" | sed "s/_${PAGE_SIZE}_/_8.27x11.69_/")
                local A4_FILE="${D}/../includes/${A4_NAME}"
                if [ -f "${A4_FILE}" ]; then
                    cp "${A4_FILE}" "${TARGET_FILE}"
                else
                    echo -e "\033[33mWarning: No template found for ${file}, skipping...\033[0m"
                fi
            fi
        fi
    done
}

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
    set -x

    # Convert page size format for Prince and override CSS
    IFS='|' read -r WIDTH HEIGHT PRINCE_PAGE_SIZE <<< "$(determine_page_size_settings "${PAGE_SIZE}")"
    local PAGE_OVERRIDE_CSS="${TEMP_DIR}/${DOCUMENT}_page_override.css"
    cat > "${PAGE_OVERRIDE_CSS}" <<EOF
@page {
  size: ${WIDTH}in ${HEIGHT}in !important;
}
EOF
    
    if prince-books \
        --style="${D}/../includes/${CSS_FILE}" \
        --style="${D}/../includes/force-cjk.css" \
        --style="${PAGE_OVERRIDE_CSS}" \
        --media=print \
        --page-size="${PRINCE_PAGE_SIZE}" \
        -o "${D}/../includes/${DOCUMENT}.pdf" \
        "${D}/../includes/${DOCUMENT}.html"; then

        echo -e "\033[32m✓ Created ${DOCUMENT}.pdf\033[0m"
        return 0
    else
        echo -e "\033[31m✗ Failed to create ${DOCUMENT}.pdf\033[0m"
        return 1
    fi
    set +x
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
        # Add two blanks at beginning and blank at end for proper alignment
        pdftk "${BLANK}" "${BLANK}" "${TEMP_DIR}/TOC_${FORMAT}-cut.pdf" "${BLANK}" cat output "${D}/../includes/FINAL_TOC_${FORMAT}.pdf"
    fi

    # Process COPYRIGHT
    echo -e "\033[34mProcessing Copyright Page...\033[0m"
    # Watermark removal strategy:
    # COPYRIGHT.pdf has structure: [blank page WITH watermark] [content pages WITHOUT watermarks]
    # 1. Remove page 1 (blank with watermark): leaves [content]
    # 2. Resize content to match target page size
    # 3. Add blank page at end for alignment
    cp "${D}/../includes/COPYRIGHT.pdf" "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf"
    
    # Step 1: Remove page 1 (blank with watermark), leaving only content
    pdftk "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf" cat 2-end output "${TEMP_DIR}/COPYRIGHT_${FORMAT}-no-watermark.pdf"
    
    # Step 2: Resize content to match target page size
    IFS='|' read -r WIDTH HEIGHT PRINCE_PAGE_SIZE <<< "$(determine_page_size_settings "${PAGE_SIZE}")"
    if ! resize_pdf_to_size "${TEMP_DIR}/COPYRIGHT_${FORMAT}-no-watermark.pdf" \
                       "${TEMP_DIR}/COPYRIGHT_${FORMAT}-resized.pdf" \
                       "${WIDTH}" "${HEIGHT}"; then
        echo -e "\033[31mError: Failed to resize COPYRIGHT_${FORMAT}.pdf\033[0m"
        status=1
    fi
    
    # Step 3: Add blank page at end
    if ! pdftk "${TEMP_DIR}/COPYRIGHT_${FORMAT}-resized.pdf" "${BLANK}" cat output "${D}/../includes/COPYRIGHT_${FORMAT}.pdf"; then
        echo -e "\033[31mError: Failed to add blank page to COPYRIGHT_${FORMAT}.pdf\033[0m"
        status=1
    fi

    # Process BOOK_INTRO
    echo -e "\033[34mProcessing Book Introduction...\033[0m"
    if ! process_document "BOOK_INTRO" "iching_nopage.css"; then
        echo -e "\033[31mFailed to process BOOK_INTRO\033[0m"
        status=1
    else
        cp "${D}/../includes/BOOK_INTRO.pdf" "${TEMP_DIR}/BOOK_INTRO_${FORMAT}.pdf"
        pdftk "${TEMP_DIR}/BOOK_INTRO_${FORMAT}.pdf" cat 3-end output "${D}/../includes/BOOK_INTRO_${FORMAT}.pdf"
    fi

    # Process main content
    echo -e "\033[34mProcessing Main Content...\033[0m"
    if ! process_document "iching"; then
        echo -e "\033[31mFailed to process iching\033[0m"
        status=1
    else
        cp "${D}/../includes/iching.pdf" "${TEMP_DIR}/iching_${FORMAT}.pdf"
        pdftk "${TEMP_DIR}/iching_${FORMAT}.pdf" cat 3-end output "${D}/../includes/iching_${FORMAT}.pdf"
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

    if [ "${MINIMAL}" = true ]; then
        echo -e "\033[33mUsing minimal format - only including main content\033[0m"
        # Only verify and use ICHING component
        if [ ! -f "${ICHING}" ]; then
            echo -e "\033[31mError: Required file |${ICHING}| not found\033[0m"
            return 1
        else
            echo -e "\033[32m✓ Found file |${ICHING}|\033[0m"
        fi

        if pdftk "${ICHING}" cat output "${OUTPUT}"; then
            echo -e "\033[32mSuccessfully created minimal ${OUTPUT}\033[0m"
            return 0
        else
            echo -e "\033[31mFailed to create minimal document\033[0m"
            return 1
        fi
    else
        # Verify all files exist
        for file in "${COPYRIGHT}" "${BOOK}" "${Q8}" "${BIN}" "${PATHS}" "${TOC}" "${ICHING}"; do
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
    fi
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
    echo -e "\033[34mPage size: ${PAGE_SIZE}, Format: ${FORMAT}, Minimal: ${MINIMAL}\033[0m"

    # Ensure required files exist
    if ! ensure_required_files "${PAGE_SIZE}"; then
        echo -e "\033[31mError: Failed to create required files\033[0m"
        return 1
    fi

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

