#!/bin/bash

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
if [ $# -eq 1 ]; then
    VERSION_SUFFIX="$1"
fi

export DISPLAY=:0

rm -f ${D}/../includes/iching.html
rm -f ${D}/../includes/iching.md

#! need to copy latrest css for typora
lessc ${D}/../includes/iching.less ${D}/../includes/iching.css
cp ${D}/../includes/iching.css /home/jw/.config/Typora/themes/iching_7_44-9_68.css


#! IMPORTANT, in /home/jw/.config/Typora/themes/, you must
#! ln -fs iching_7_44-9_68 iching_7_44-9_68_nopage

lessc ${D}/../includes/iching_nopage.less ${D}/../includes/iching_nopage.css
cp ${D}/../includes/iching_nopage.css /home/jw/.config/Typora/themes/iching_7_44-9_68_nopage.css


#^ make the copyright page.  Export includes/COPYRIGHT_PAGE.docx to ../includes/COPYRIGHT_PAGE.pdf

#^ make the coverpage.  Export includes/COVER_PAGE.docx to ../includes/COVER_PAGE.pdf

# ./makeallmd.py --content all
./makeallmd.py --content pages


typora ${D}/../includes/iching.md

# after export./ makebook_postonly.sh in called from Typora