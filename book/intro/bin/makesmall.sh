#!/bin/bash

# # Process all PNG files from the HiRes directory
# for file in ../HiRes/*.png; do
#   # Extract just the filename without the path and extension
#   filename=$(basename "${file%.*}")

#   # Convert the file to 72 DPI and immediately to JPEG with 50% quality
#   magick "$file" -density 72 -units PixelsPerInch -quality 50 "../72/${filename}.jpg"

#   echo "Converted: $filename.png to $filename.jpg with 72 DPI and 50% quality"
# done

# rename .jpg _sm.jpg *



# # Process all PNG files from the HiRes directoryrename .jpg _sm.jpg *

# for file in ../HiRes/bc/*.png; do
#   # Extract just the filename without the path and extension
#   filename=$(basename "${file%.*}")

#   # Convert the file to 72 DPI and immediately to JPEG with 50% quality
#   magick "$file" -density 72 -units PixelsPerInch -quality 50 "../72/bc/${filename}.jpg"

#   echo "Converted: $filename.png to $filename.jpg with 72 DPI and 50% quality"
# done

#rename .jpg _sm.jpg *


cp ../content/iching_intro.md ../content/iching_intro_sm.md

perl -pi -e 's/\.png/_sm.jpg/g' ../content/iching_intro_sm.md

rm ../Images
ln -fs /home/jw/src/iching_cli/book/72  ../Images

typora ../content/iching_intro_sm.md
