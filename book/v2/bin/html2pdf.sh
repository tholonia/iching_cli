#!/bin/bash

# =============================================================================
# html2pdf.sh - I Ching Book PDF Generation Script
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
#   ./html2pdf.sh <input.html>
#
# Dependencies:
#   - Prince: HTML to PDF conversion with TOC support
#     Required flags: --prince-toc for TOC generation
#   - pdftk: PDF manipulation tool
#   - Okular: PDF viewer
#
# Input Files:
#   - <input.html>: Main content with TOC nav element
#   - iching.css: Styling with Prince-specific TOC properties
#
# Output:
#   - FINAL_<input>.pdf: Complete book with:
#     - Cover page
#     - Copyright page
#     - Table of contents
#     - Main content
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Error: No input HTML file specified"
    echo "Usage: $0 <input.html>"
    exit 1
fi

INPUT_HTML="$1"
OUTPUT_NAME=$(basename "$INPUT_HTML" .html)
CURRENT_SIZE="8.25x11"

D="/home/jw/src/iching_cli/book/v2/bin"


function process_document() {
    local DOCUMENT="$1"
    local CSS="${2:-iching.css}"

    echo -e "\033[35mProcessing ${DOCUMENT}\033[0m"

    # delete calc() line
    cp ${D}/../includes/${DOCUMENT}.html /tmp/html.tmp
    cat /tmp/html.tmp | grep -v "calc(" > ${D}/../includes/${DOCUMENT}.html

    # make PDF
    rm -f ${D}/../includes/${DOCUMENT}.pdf
    set -x
    prince-books \
        --style=${D}/../includes/${CSS} \
        --media=print \
        -o ${D}/../includes/${DOCUMENT}.pdf \
        ${D}/../includes/${DOCUMENT}.html
    set +x
}


#! need to copy latest css for typora
lessc ${D}/../includes/iching.less ${D}/../includes/iching.css
cp ${D}/../includes/iching.css /home/jw/.config/Typora/themes/iching.css


#! IMPORTANT, in /home/jw/.config/Typora/themes/, you must
#! ln -fs iching_7_44-9_68 iching_7_44-9_68_nopage

lessc ${D}/../includes/iching_nopage.less ${D}/../includes/iching_nopage.css
cp ${D}/../includes/iching_nopage.css /home/jw/.config/Typora/themes/iching_nopage.css



#^ PROCESS: TOC.html > TOC.pdf
#! make sure the HTML output was generated with the 'nopages' CSS to avoid page numbers
process_document "$OUTPUT_NAME" "iching_nopage.css"
cp ${D}/../includes/${OUTPUT_NAME}.pdf /tmp/${OUTPUT_NAME}.pdf
pdftk /tmp/${OUTPUT_NAME}.pdf cat 3-end output /tmp/${OUTPUT_NAME}-cut.pdf
# insert 2 blank pages
pdftk ${BLANK} /tmp/${OUTPUT_NAME}-cut.pdf cat output ${D}/../includes/FINAL_${OUTPUT_NAME}.pdf

okular ${D}/../includes/FINAL_${OUTPUT_NAME}.pdf

