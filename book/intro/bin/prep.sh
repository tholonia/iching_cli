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
#     ./prep.sh [--small] [--no-gui] [--build]
#       --small    Use lower resolution images for faster processing
#       --no-gui   Skip launching Typora (for systems without X11/display)
#       --build    Rebuild all image files (otherwise uses cached versions)
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



# cat \
# ../content/i00_INTRO.md \
# ../content/i01_FOUNDATION.md \
# ../content/i02_ICHING_BASICS.md \
# ../content/i03_MAPPING.md \
# ../content/i04_SYNTHESIS.md \
# ../content/i05_MATH.md \
# ../content/i06_APPENDIX.md \
# > ../content/iching_intro.md

cat \
../content/i00_INTRO.md \
../content/i01_FOUNDATION.md \
../content/i02_ICHING_BASICS.md \
../content/i03_MAPPING.md \
../content/i04_SYNTHESIS.md \
../content/i05_MATH.md \
../content/i06_APPENDIX.md \
> ../content/iching_intro.md





D="/home/jw/src/iching_cli/book/intro/bin"
PAGE_SIZE=_6.69x9.61

# Parse command line arguments
SMALL=false
NO_GUI=false
BUILD=false
rm -f ../Images
ln -fs /home/jw/store/src/iching_cli/book/intro/HiRes  /home/jw/store/src/iching_cli/book/intro/Images
for arg in "$@"; do
  case $arg in
    --small)
      SMALL=true
      rm -f ../Images
      ln -fs /home/jw/store/src/iching_cli/book/intro/72  /home/jw/store/src/iching_cli/book/intro/Images

      shift
      ;;
    --no-gui)
      NO_GUI=true
      shift
      ;;
    --build)
      BUILD=true
      shift
      ;;
    *)
      # Unknown option
      ;;
  esac
done


# Get version suffix if provided
VERSION_SUFFIX=""

# Only set display if not in no-gui mode
if [ "$NO_GUI" = false ]; then
  export DISPLAY=:0
fi

# rm -f ${D}/../intro/iching_intro.html

#! need to copy latest css for typora
lessc ${D}/../Styles/iching_intro.less ${D}/../Styles/iching_intro.css
cp ${D}/../Styles/iching_intro.css /home/jw/.config/Typora/themes/iching_intro.css
cp ${D}/../Styles/iching_intro.less /home/jw/.config/Typora/themes/iching_intro.less

lessc ${D}/../Styles/iching_intro_nopage.less ${D}/../Styles/iching_intro_nopage.css
cp ${D}/../Styles/iching_intro_nopage.css /home/jw/.config/Typora/themes/iching_intro_nopage.css
cp ${D}/../Styles/iching_intro_nopage.less /home/jw/.config/Typora/themes/iching_intro_nopage.less

if [ "$SMALL" = true ]; then

    if [ "$BUILD" = true ]; then
        rm -f ../72/bc/*.jpg
        # Process all PNG files from the HiRes directory
        for file in ../HiRes/bc/*.png; do
            # Extract just the filename without the path and extension
            filename=$(basename "${file%.*}")

            # Convert the file to 72 DPI and immediately to JPEG with 50% quality
            magick "$file" -density 72 -units PixelsPerInch -quality 50 "../72/bc/${filename}.jpg"

            echo "Converted: $filename.png to $filename.jpg with 72 DPI and 50% quality"
            done
        cd ../72/bc
        rename .jpg _sm.jpg *.jpg
        cd -

        # Process all PNG files from the HiRes directory
        echo "Processing images in small mode..."
        rm -f ../72/*.jpg

        for file in ../HiRes/*.png; do
            # Extract just the filename without the path and extension
            filename=$(basename "${file%.*}")

            # Convert the file to 72 DPI and immediately to JPEG with 50% quality
            magick "$file" -density 72 -units PixelsPerInch -quality 50 "../72/${filename}.jpg"

            echo "Converted: $filename.png to $filename.jpg with 72 DPI and 50% quality"
            done

        cd ../72
            rename .jpg _sm.jpg *.jpg
        cd -
    fi


    cp ../content/iching_intro.md ../content/iching_intro_sm.md
    perl -pi -e 's/\.png/_sm.jpg/g' ../content/iching_intro_sm.md

    if [ "$NO_GUI" = false ]; then
      typora ${D}/../content/iching_intro_sm.md || echo "Error: Failed to open Typora. Try running with --no-gui option."
    else
      echo "Skipping Typora in no-gui mode. Files are prepared at: ${D}/../content/iching_intro_sm.md"
    fi
else
    if [ "$NO_GUI" = false ]; then
    # Display reminder in cyan
      echo -e "\033[36mREMINDER: You must save the output to the '../latest' directory!\033[0m"
      echo "Press Enter to continue..."
      read

      typora ${D}/../content/iching_intro.md || echo "Error: Failed to open Typora. Try running with --no-gui option."
    else
      echo "Skipping Typora in no-gui mode. Files are prepared at: ${D}/../content/iching_intro.md"
    fi
fi

