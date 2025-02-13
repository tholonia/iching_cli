#!/bin/bash -x

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

# Function to process a document
process_document() {
    local DOCUMENT="$1"
	local STYLE="$2"
	local FROM=$3

    # delete calc() line
    cp ${D}/../includes/${DOCUMENT}.html /tmp/${DOCUMENT}-html.tmp
    cat /tmp/${DOCUMENT}-html.tmp | grep -v "calc(" > ${D}/../includes/${DOCUMENT}.html

	# create watermark page
	# cp ${D}/../includes/iching_all.html /tmp/html.tmp
	# echo ${BREAK} > ${D}/../includes/iching_all.html
	# cat /tmp/html.tmp >> ${D}/../includes/iching_all.html

    # make PDF
    rm -f ${D}/../includes/${DOCUMENT}.pdf
    prince-books \
        --style=${D}/../includes/${STYLE:-iching.css} \
        --media=print \
        -o ${D}/../includes/${DOCUMENT}.pdf \
        ${D}/../includes/${DOCUMENT}.html

	pdftk ${D}/../includes/${DOCUMENT}.pdf cat ${FROM}-end output /tmp/${DOCUMENT}-pdf.tmp
	mv /tmp/${DOCUMENT}-pdf.tmp ${D}/../includes/${DOCUMENT}.pdf
}

rm -f ${D}/../includes/FINAL_iching.pdf
rm -f /tmp/out.pdf
rm -f /tmp/html.pdf

process_document "COPYRIGHT_PAGE_v1" "iching_nopage.css" 5
# add a blank page to the beginning of the document
cp ${D}/../includes/COPYRIGHT_PAGE_v1.pdf /tmp/out.pdf
pdftk B=../includes/blank.pdf A=/tmp/out.pdf cat B A output ${D}/../includes/COPYRIGHT_PAGE_v1.pdf

process_document "BOOK_INTRO" "iching.css" 3
# add a blank page to the beginning of the document
cp ${D}/../includes/BOOK_INTRO.pdf /tmp/out.pdf
pdftk B=../includes/blank.pdf A=/tmp/out.pdf cat B A output ${D}/../includes/BOOK_INTRO.pdf

process_document "iching" "iching.css" 3
# add 2 blank pages to the beginning of the document
cp ${D}/../includes/iching.pdf /tmp/out.pdf

pdftk B=../includes/blank.pdf C=../includes/blank.pdf A=/tmp/out.pdf cat B C A output ${D}/../includes/iching.pdf


#~-----------------------------------------------------------------------------------

# add copyright and cover to PDF
pdftk \
    ${D}/../includes/COVER_PAGE.pdf \
    ${D}/../includes/COPYRIGHT_PAGE_v1.pdf \
    ${D}/../includes/BOOK_INTRO.pdf \
    ${D}/../includes/iching.pdf \
    cat output /tmp/out.pdf


# okular    ${D}/../includes/COVER_PAGE.pdf
# okular    ${D}/../includes/COPYRIGHT_PAGE_v1.pdf
# okular    ${D}/../includes/BOOK_INTRO.pdf
# okular    ${D}/../includes/iching.pdf
okular    /tmp/out.pdf

