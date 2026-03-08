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
#     ./post.sh [BOOK|PDF] [--small] [--no-gui] [--paperback|--hardcover] # default: BOOK
#
# Options:
#     BOOK|PDF   - Output format (defaults to PDF if not specified)
#     --small    - Use small image version (iching_intro_sm.md) as input
#     --no-gui   - Skip document preview
#     --paperback - Use paperback page size (6.69x9.61) - default
#     --hardcover - Use hardcover page size (7.0x10.0)
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
SMALL=false    # Default to standard version
SHOW_GUI=true  # Default to showing GUI
PAGE_TYPE="paperback"  # Default to paperback

# Parse all arguments
for arg in "$@"; do
  case $arg in
    BOOK|PDF)
      FORMAT="$arg"
      ;;
    --small)
      SMALL=true
      ;;
    --no-gui)
      SHOW_GUI=false
      ;;
    --paperback)
      PAGE_TYPE="paperback"
      ;;
    --hardcover)
      PAGE_TYPE="hardcover"
      ;;
    *)
      echo -e "\033[31mError: Invalid argument '$arg'. Valid formats are BOOK or PDF with optional --small, --no-gui, --paperback, or --hardcover.\033[0m"
      echo -e "Usage: $0 [BOOK|PDF] [--small] [--no-gui] [--paperback|--hardcover]"
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

# Set page size based on page type
if [ "$PAGE_TYPE" = "hardcover" ]; then
    PROD_PAGE_SIZE="7.0x10.0"
    PRINCE_PAGE_SIZE="7in 10in"
#    PROD_PAGE_SIZE="6.69x9.61"
#    PRINCE_PAGE_SIZE="6.69in 9.61in"
    echo -e "\033[34mUsing hardcover page size: ${PROD_PAGE_SIZE}\033[0m"
else
    PROD_PAGE_SIZE="6.69x9.61"
    PRINCE_PAGE_SIZE="6.69in 9.61in"
    echo -e "\033[34mUsing paperback page size: ${PROD_PAGE_SIZE}\033[0m"
fi

PAGE_SIZE="${PROD_PAGE_SIZE}"
BASE_DIR="/home/jw/src/iching_cli/book/intro"
SCRIPT_DIR="${BASE_DIR}/bin"
CONTENT_DIR="${BASE_DIR}/content"
LATEST_DIR="${BASE_DIR}/Latest"
STYLES_DIR="${BASE_DIR}/Styles"
BLANK_PAGE="${CONTENT_DIR}/blank_${PAGE_SIZE}.pdf"
OUTPUT_NAME="FINAL_iching_intro_${PAGE_TYPE}_${FORMAT}"
if [ "$SMALL" = true ]; then
  OUTPUT_NAME="FINAL_iching_intro_sm_${PAGE_TYPE}_${FORMAT}"
fi
TEMP_DIR="/tmp"

# Create required directories
mkdir -p "${LATEST_DIR}"


echo -e "\033[36mPreparing...\033[0m"
./prep.sh --no-gui



function rmx() {
    # echo "Deleting: ${1}"
    rm -f "${1}"
}


# Cleanup previous run
function cleanup_previous_files() {
    echo -e "\033[33mCleaning up previous files...\033[0m"
    # rmx "${LATEST_DIR}/${OUTPUT_NAME}_${FORMAT}.pdf"
    # rmx "${TEMP_DIR}/out.pdf"
    # rmx "${TEMP_DIR}/html.pdf"
    # rmx "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf"
    # rmx "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf"
    # rmx "${TEMP_DIR}/TOC_${FORMAT}.pdf"
    # rmx "${TEMP_DIR}/${INPUT_BASE}_${FORMAT}.pdf-cut.pdf"
    # rmx "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf-cut.pdf"
    # rmx "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf"
    # rmx "${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    # rmx "${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"

}

# Process an HTML document into PDF
function process_document() {
    # set -x
    local DOCUMENT="$1"
    local CSS_FILE="${2:-iching_intro.css}"
    
    # Use different CSS file based on format
    if [ "$FORMAT" = "BOOK" ]; then
        CSS_FILE="iching_intro_book.css"
    else
        CSS_FILE="iching_intro_pdf.css"
    fi
    
    local INPUT_HTML="${LATEST_DIR}/${DOCUMENT}.html"
    local OUTPUT_PDF="${LATEST_DIR}/${DOCUMENT}.pdf"
    local TEMP_HTML="${TEMP_DIR}/html.tmp"

    echo -e "\033[35mProcessing ${INPUT_HTML}\033[0m"

    # Remove calc() line to prevent rendering issues
    cp "${INPUT_HTML}" "${TEMP_HTML}"
    grep -v "calc(" "${TEMP_HTML}" > "${INPUT_HTML}"

    # cp "${INPUT_HTML}" "${TEMP_HTML}"
    # mjpage --output SVG --font TeX --dollars < "${INPUT_HTML}" > "${TEMP_HTML}"


    # cp "${INPUT_HTML}" "${TEMP_HTML}"
    # sed -E ':a;N;$!ba;s/<svg[^>]*>.*?<\/svg>//g' "${TEMP_HTML}" > "${INPUT_HTML}"

    # # Remove SVG line to prevent rendering issues
    # cp "${INPUT_HTML}" "${TEMP_HTML}"
    # grep -v -i "svg" "${TEMP_HTML}" > "${INPUT_HTML}"

    # Convert HTML to PDF

    # Concatenate all markdown files into one
    cat \
    ${CONTENT_DIR}/i00_INTRO.md \
    ${CONTENT_DIR}/i01_FOUNDATION.md \
    ${CONTENT_DIR}/i02_ICHING_BASICS.md \
    ${CONTENT_DIR}/i03_MAPPING.md \
    ${CONTENT_DIR}/i04_SYNTHESIS.md \
    ${CONTENT_DIR}/i05_MATH.md \
    ${CONTENT_DIR}/i06_APPENDIX.md \
    > ${LATEST_DIR}/${DOCUMENT}.md

    echo -e "\033[36mCreated ${LATEST_DIR}/${DOCUMENT}.md\033[0m"
    echo -e "\033[36mConverting to HTML (pandoc)\033[0m"

    pandoc \
        --pdf-engine=xelatex \
        --from=markdown+tex_math_dollars+tex_math_single_backslash \
        --to=html5 \
        --mathjax \
        --verbose \
        --webtex \
        --top-level-division=chapter \
        --metadata title='Delete this Title Text' \
        --metadata=lang:en \
        -o ${LATEST_DIR}/${DOCUMENT}.html \
        ${LATEST_DIR}/${DOCUMENT}.md


#!clean up some pandoc/typors/css incompatibilities

    # perl -pi -e 's/<\/style>//gmi' ${LATEST_DIR}/${DOCUMENT}.html
    # perl -pi -e 's/<\/head>/<\/style>\n<\/head>/gmi' ${LATEST_DIR}/${DOCUMENT}.html


    echo -e "\033[36mCreated ${LATEST_DIR}/${DOCUMENT}.html\033[0m"

        # --include-in-header=file://${STYLES_DIR}/${CSS_FILE}"  \

        # --standalone \
        # -o /home/jw/src/iching_cli/book/intro/Latest/iching_intro.html \
        # /home/jw/src/iching_cli/book/intro/content/iching_intro.md

    # Optional flags you might want to use later:
    # --template=/usr/share/pandoc/data/templates/tholonia.html5
    # --metadata-file=${H}/inc/metadata.yaml
    # --toc \
    echo -e "\033[36mConverting to PDF (prince-books)\033[0m"
    rm debug.log
    prince-books \
        --verbose \
        --no-warn-css \
        --debug \
        --log=debug.log  \
        --fail-dropped-content \
        --fail-missing-resources \
        --fail-missing-glyphs  \
        --input=html \
        --style="${STYLES_DIR}/${CSS_FILE}" \
        --media=print \
        -o "${OUTPUT_PDF}" \
        "${INPUT_HTML}"

    tail debug.log
    # Check if PDF was created successfully
    if [ ! -f "${OUTPUT_PDF}" ]; then
        echo -e "\033[31mError: Failed to create ${OUTPUT_PDF}\033[0m"
        return 1
    fi

    echo -e "\033[32m >>>CREATED ${OUTPUT_PDF}\033[0m"
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

    echo -e "\033[33m >>>OUTPUT TO: ${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf\033[0m"

    # Process copyright
#    process_document "COPYRIGHT"
    cp "${LATEST_DIR}/COPYRIGHT.pdf" "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf"
    if [ "$FORMAT" = "BOOK" ]; then
        pdftk "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf" cat 2-end output "${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    else
        pdftk "${TEMP_DIR}/COPYRIGHT_${FORMAT}.pdf" cat 1-end output "${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    fi
    # Process TOC with no page numbers
    # #!--------------------------------------------------------------
    # process_document "TOC" "iching_intro_nopage.css"
    # #!--------------------------------------------------------------
    # cp "${LATEST_DIR}/TOC.pdf" "${TEMP_DIR}/TOC_${FORMAT}.pdf"
    # pdftk "${TEMP_DIR}/TOC_${FORMAT}.pdf" cat 3-end output "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf"
    # pdftk "${BLANK_PAGE}" "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf" cat output "${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"

    # echo -e "\033[32m >>>OUTPUT TO: ${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf\033[0m"
    
}

# Set file references based on format
function set_format_files() {
    echo -e "\033[33mFORMAT = ${FORMAT}\033[0m"

    if [ "$FORMAT" = "BOOK" ]; then
        COVER=""
        COPYRIGHT="${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    else
        # COVER="${CONTENT_DIR}/COVER_${PAGE_SIZE}.pdf"
        COVER="/home/jw/src/iching_cli/book/intro/publish/PAPERBACK/COVER_6.69x9.61.pdf"
        COPYRIGHT="${LATEST_DIR}/FINAL_COPYRIGHT_${FORMAT}.pdf"
    fi

    echo -e "\033[33mCOVER =${COVER}\033[0m"
    echo -e "\033[33mCOPYRIGHT =${CONTENT_DIR}/\033[0m"
    echo -e "\033[33mICHING =${LATEST_DIR}/${INPUT_BASE}_${FORMAT}.pdf\033[0m"
    
}

# Merge all documents into final PDF
function merge_documents() {
    echo -e "\033[33mMerging documents into final PDF...\033[0m"

    TOC="${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"
    # TOC=""

    ICHING="${LATEST_DIR}/${INPUT_BASE}_${FORMAT}.pdf"
    OUTPUT="${LATEST_DIR}/${OUTPUT_NAME}.pdf"

    echo -e "\033[33m +++OUTPUT TO: ${COVER}\033[0m"
    echo -e "\033[33m +++OUTPUT TO: ${COPYRIGHT}\033[0m"
    echo -e "\033[33m +++OUTPUT TO: ${TOC}\033[0m"
    echo -e "\033[33m +++OUTPUT TO: ${BLANK_PAGE} (inserted to fix gutter alignment)\033[0m"
    echo -e "\033[33m +++OUTPUT TO: ${ICHING}\033[0m"
    echo -e "\033[33m >>>OUTPUT TO: ${OUTPUT}\033[0m"   

    echo -e "\033[1;34mRegenerating TOC\033[0m"
    ./regen_TOC_v2.py "${PROD_PAGE_SIZE}" "${FORMAT}"
    
    # Convert TOC HTML to PDF
    echo -e "\033[36mConverting TOC to PDF (prince-books)\033[0m"
    rm -f debug_toc.log
    prince-books \
        --verbose \
        --no-warn-css \
        --debug \
        --log=debug_toc.log  \
        --fail-dropped-content \
        --fail-missing-resources \
        --fail-missing-glyphs  \
        --input=html \
        --style="${STYLES_DIR}/iching_intro_nopage.css" \
        --media=print \
        -o "${LATEST_DIR}/TOC.pdf" \
        "${LATEST_DIR}/TOC.html"
    
    # Process TOC for final output
    cp "${LATEST_DIR}/TOC.pdf" "${TEMP_DIR}/TOC_${FORMAT}.pdf"
    pdftk "${TEMP_DIR}/TOC_${FORMAT}.pdf" cat 3-end output "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf"
    pdftk "${BLANK_PAGE}" "${TEMP_DIR}/TOC_${FORMAT}.pdf-cut.pdf" cat output "${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"
    
    # Update TOC variable to point to the newly generated file
    TOC="${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"
    
    echo -e "\033[32mTOC PDF generated: ${TOC}\033[0m"

    # Insert blank page after copyright/TOC to fix odd/even page alignment
    # This ensures the main content starts on the correct page for gutter positioning
    pdftk \
        ${COVER} \
        ${COPYRIGHT} \
        ${TOC} \
        ${BLANK_PAGE} \
        ${ICHING} \
        cat output "${OUTPUT}"

    # pdftk \
    #     ${ICHING} \
    #     cat output "${OUTPUT}"



    echo -e "\033[32mCreated final document: ${OUTPUT}\033[0m"
}

function content_only() {
    echo -e "\033[33mMerging documents into final PDF...\033[0m"

#    TOC="${LATEST_DIR}/FINAL_TOC_${FORMAT}.pdf"
    TOC=""

    ICHING="${LATEST_DIR}/${INPUT_BASE}_${FORMAT}.pdf"
    OUTPUT="${LATEST_DIR}/${OUTPUT_NAME}.pdf"

    pdftk ${ICHING} cat output "${OUTPUT}"

    echo -e "\033[32mCreated final document: ${OUTPUT}\033[0m"
}

# Display the final document
function display_document() {
    local OUTPUT_FILE="${LATEST_DIR}/${OUTPUT_NAME}.pdf"
    
    if [ "$SHOW_GUI" = true ]; then
        echo -e "\033[33mOpening document for preview...\033[0m"
        echo -e "\033[33mOpening: ${OUTPUT_FILE}\033[0m"
        okular "${OUTPUT_FILE}"
    else
        echo -e "\033[33mSkipping document preview (--no-gui mode)...\033[0m"
        echo -e "\033[33mFinal document: ${OUTPUT_FILE}\033[0m"
    fi
}

# Main execution flow
function main() {
    # Start processing
    echo -e "\033[1;34mStarting document post-processing\033[0m"
    echo -e "\033[34mPage size: ${PAGE_SIZE}, Format: ${FORMAT}\033[0m"

    # Clean up previous files
    echo -e "\033[31mCALLING cleanup_previous_files\033[0m"
    cleanup_previous_files

    # Process documents
    echo -e "\033[31mCALLING process_documents_for_format\033[0m"
    process_documents_for_format


    # Set format-specific files
    echo -e "\033[31mCALLING set_format_files\033[0m"
    set_format_files

    # Merge documents
    # echo -e "\033[1;34mCreating CONTENT ONLY for TOC\033[0m"
    # content_only

    echo -e "\033[31mCALLING merge_documents\033[0m"
    merge_documents

    # Display the final document
    echo -e "\033[31mCALLING display_document\033[0m"
    display_document

    echo -e "\033[1;32mPost-processing complete\033[0m"
}

# Run the main function
main

