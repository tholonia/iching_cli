#!/bin/bash
# =============================================================================
# prep.sh - I Ching Introduction Document Preparation Script
# =============================================================================
#
# Description:
#     Prepares the I Ching introduction document by cleaning previous builds,
#     compiling LESS stylesheets to CSS, updating Typora themes, and opening
#     the document for editing. This script ensures consistent styling and
#     proper environment setup before document generation.
#
# Usage:
#     ./prep.sh
#
# Process:
#     1. Environment Setup - Sets directory paths and display
#     2. Clean Previous Builds - Removes existing HTML output
#     3. Style Compilation - Processes LESS files to CSS
#     4. Theme Installation - Copies styles to Typora theme directory
#     5. Document Opening - Launches Typora with the introduction document
#
# Files Processed:
#     - iching_intro.less → iching_intro.css
#     - iching_intro_nopage.less → iching_intro_nopage.css
#     - iching_intro.md (opened in Typora)
#
# Dependencies:
#     - lessc: LESS CSS compiler
#     - Typora: Markdown editor/viewer
#     - X11 display server
#
# Directory Structure:
#     - ../Styles/: Contains LESS and CSS style files
#     - ../content/: Contains markdown content
#     - /home/jw/.config/Typora/themes/: Typora themes directory
#
# Notes:
#     - Uses PAGE_SIZE=_6.69x9.61 for consistent document dimensions
#     - Requires X11 display server for Typora GUI (export DISPLAY=:0)
#
# Author: JW
# Last Updated: 2024
# =============================================================================

D="/home/jw/src/iching_cli/book/intro/bin"
PAGE_SIZE=_6.69x9.61

# Get version suffix if provided
VERSION_SUFFIX=""

export DISPLAY=:0

rm -f ${D}/../intro/iching_intro.html

#! need to copy latest css for typora
lessc ${D}/../Styles/iching_intro.less ${D}/../Styles/iching_intro.css
cp ${D}/../Styles/iching_intro.css /home/jw/.config/Typora/themes/iching_intro.css
cp ${D}/../Styles/iching_intro.less /home/jw/.config/Typora/themes/iching_intro.less

lessc ${D}/../Styles/iching_intro_nopage.less ${D}/../Styles/iching_intro_nopage.css
cp ${D}/../Styles/iching_intro_nopage.css /home/jw/.config/Typora/themes/iching_intro_nopage.css
cp ${D}/../Styles/iching_intro_nopage.less /home/jw/.config/Typora/themes/iching_intro_nopage.less


typora ${D}/../content/iching_intro.md

