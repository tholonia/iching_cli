#!/bin/bash

# =============================================================================
# prep.sh - I Ching Book Preparation Script
# =============================================================================
#
# Description:
#   This script prepares the I Ching book for PDF generation by setting up
#   necessary files, compiling styles, and initiating the document generation
#   process. It ensures a clean build environment and consistent styling.
#
# Usage:
#   ./prep.sh [version_suffix] [--test]
#   Example: ./prep.sh v2         # Will use files with "_v2" suffix
#   Example: ./prep.sh v2 --test  # Will use test set of hexagrams
#
# Arguments:
#   version_suffix: Optional suffix for versioned files
#   --test: Optional flag to use test set of hexagrams
#
# Process:
#   1. Clean Build Environment:
#      - Remove existing HTML and MD files
#      - Ensure fresh start for new build
#   2. Style Compilation:
#      - Compile iching.less to iching.css
#      - Compile iching_nopage.less to iching_nopage.css
#   3. Typora Configuration:
#      - Copy compiled CSS to Typora themes
#      - Set up both paged and non-paged variants
#   4. Document Generation:
#      - Run makeallmd.py to create markdown
#      - Open in Typora for manual export
#
# Dependencies:
#   - lessc: LESS CSS compiler
#   - Typora: Markdown editor
#   - makeallmd.py: Markdown generation script
#
# File Structure:
#   Input:
#     - ../includes/iching.less
#     - ../includes/iching_nopage.less
#   Output:
#     - ../includes/iching.css
#     - ../includes/iching_nopage.css
#     - ~/.config/Typora/themes/iching.css
#     - ~/.config/Typora/themes/iching_nopage.css
#
# Notes:
#   - Ensure Typora is properly configured with theme directory
#   - Manual export to HTML required after script completion
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# makebook.sh
# Usage: ./makebook_pre.sh [version_suffix]
# Example: ./makebook_pre.sh v2    # Will use files with "_v2" suffix

# This script prepares the I Ching book for PDF generation by performing the following tasks:
# 1. Cleans up previous HTML and Markdown files to ensure a fresh build.
# 2. Compiles LESS stylesheets into CSS for use in Typora and Prince.
# 3. Copies the latest CSS to Typora's theme directory for consistent styling.
# 4. Generates the Markdown document for the I Ching book using makeallmd.py.
# 5. Opens the generated Markdown in Typora for manual export to HTML.
# 6. After exporting, makebook_postonly.sh is called from Typora to finalize the PDF.

# Steps:
# 1. Remove existing iching.html and iching.md files to avoid conflicts.
# 2. Compile iching.less into iching.css using lessc.
# 3. Copy the compiled CSS to Typora's theme directory.
# 4. Generate the Markdown document using makeallmd.py with the --content pages option.
# 5. Open the generated iching.md in Typora for review and export.

# Usage:
# Run this script to prepare the I Ching book for PDF generation. After running, use Typora to export the Markdown to HTML.

# Dependencies:
# - lessc: A tool for compiling LESS to CSS.
# - Typora: A Markdown editor for reviewing and exporting the document.
# - makeallmd.py: A Python script for generating the Markdown document.

# Note:
# Ensure all input files and dependencies are present and correctly configured before running the script.

D="/home/jw/src/iching_cli/book/v2/bin"

# Get version suffix if provided
VERSION_SUFFIX=""
TEST_FLAG=""


# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            TEST_FLAG="--test"
            shift
            ;;
        *)
            VERSION_SUFFIX="$1"
            shift
            ;;
    esac
done

export DISPLAY=:0

rm -f ${D}/../includes/iching.html
rm -f ${D}/../includes/iching.md

#! need to copy latest css for typora
lessc ${D}/../includes/iching.less ${D}/../includes/iching.css
cp ${D}/../includes/iching.css /home/jw/.config/Typora/themes/iching.css


#! IMPORTANT, in /home/jw/.config/Typora/themes/, you must
#! ln -fs iching_7_44-9_68 iching_7_44-9_68_nopage

lessc ${D}/../includes/iching_nopage.less ${D}/../includes/iching_nopage.css
cp ${D}/../includes/iching_nopage.css /home/jw/.config/Typora/themes/iching_nopage.css

# Pass the test flag to makeallmd.py if present
#./makeallmd.py --content pages ${TEST_FLAG}
./make_all_docs.py --content pages ${TEST_FLAG}

typora ${D}/../includes/iching.md

# after export./ makebook_postonly.sh in called from Typora