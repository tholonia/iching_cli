#!/bin/bash

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

rm ${D}/../docs/FINAL_iching.pdf

prince-books \
	--style=${D}/../includes/iching.css \
	--media=print \
	-o ${D}/../includes/iching.pdf \
	${D}/../includes/iching.html

# add copyrigth and cover tp pdfg
pdftk \
    ../includes/COVER_PAGE.pdf \
	../includes/COPYRIGHT_PAGE.pdf \
    ../includes/iching.pdf \
    cat output ${D}/../docs/FINAL_iching.pdf

okular ${D}/../docs/FINAL_iching.pdf

