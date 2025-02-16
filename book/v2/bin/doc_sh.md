get_new_hex_desc_LOCAL_BATCH.sh
get_new_hex_desc_OPENAI_BATCH.sh
get_new_image_desc_OPENAI_BATCH.sh
joe_BATCH.sh
line_types_BATCH.sh
post.sh
prep.sh
regen_lines_in_context_BATCH.sh
regen_lines_in_context_HEX.sh
regen_lines_in_history_BATCH.sh
regen_trigram_phrase_BATCH.sh


# Shell Scripts Documentation

This document contains the documentation for all shell scripts in the current directory.

---

# Script Usage Index

Detailed usage instructions for each script:

- [get_new_hex_desc_LOCAL_BATCH.sh](#get_new_hex_desc_local_batch.sh)
  ```
  ./get_new_hex_desc_LOCAL_BATCH.sh
  ```

- [get_new_hex_desc_OPENAI_BATCH.sh](#get_new_hex_desc_openai_batch.sh)
  ```
  ./get_new_hex_desc_OPENAI_BATCH.sh
  ```

- [get_new_image_desc_OPENAI_BATCH.sh](#get_new_image_desc_openai_batch.sh)
  ```
  ./get_new_image_desc_OPENAI_BATCH.sh
  ```

- [joe_BATCH.sh](#joe_batch.sh)
  ```
  ./joe_BATCH.sh
  ```

- [line_types_BATCH.sh](#line_types_batch.sh)
  ```
  ./line_types_BATCH.sh
  ```

- [post.sh](#post.sh)
  ```
  Run this script from the command line to generate and view the final I Ching book PDF.
Dependencies:
- Prince: A tool for converting HTML and CSS to PDF.
- pdftk: A tool for manipulating PDF documents.
- Okular: A PDF viewer for reviewing the final document.
Note:
Ensure all input files (COVER_PAGE.pdf, COPYRIGHT_PAGE.pdf, iching.html) are present in the expected directories.
  ```

- [prep.sh](#prep.sh)
  ```
  ./prep.sh [version_suffix]
Example: ./prep.sh v2    # Will use files with "_v2" suffix
  ```

- [regen_lines_in_context_BATCH.sh](#regen_lines_in_context_batch.sh)
  ```
  ./regen_lines_in_context_BATCH.sh
  ```

- [regen_lines_in_context_HEX.sh](#regen_lines_in_context_hex.sh)
  ```
  ./regen_lines_in_context_HEX.sh <hexagram_number>
  ```

- [regen_lines_in_history_BATCH.sh](#regen_lines_in_history_batch.sh)
  ```
  ./regen_lines_in_history_BATCH.sh
  ```

- [regen_trigram_phrase_BATCH.sh](#regen_trigram_phrase_batch.sh)
  ```
  ./regen_trigram_phrase_BATCH.sh
  ```

---

# Script Documentation

## get_new_hex_desc_LOCAL_BATCH.sh

=============================================================================
get_new_hex_desc_LOCAL_BATCH.sh - I Ching Hexagram Description Generator
=============================================================================

Description:
This script automates the generation of hexagram descriptions by iterating
through all 64 hexagrams. For each hexagram, it calls the
get_new_hex_desc_LOCAL.py script to generate and save descriptions.

Usage:
./get_new_hex_desc_LOCAL_BATCH.sh

Process:
1. Loops through numbers 1-64
2. For each number, formats it with leading zeros (01, 02, etc.)
3. Calls get_new_hex_desc_LOCAL.py with the formatted number
4. Automatically saves results (--save flag)

Dependencies:
- get_new_hex_desc_LOCAL.py script in same directory
- Python environment with required packages

Note:
This is a batch processing script that will process all hexagrams
sequentially. Ensure enough time and resources are available for
complete processing.

Author: JW
Last Updated: 2024
=============================================================================
Loop from 1 to 64

---

## get_new_hex_desc_OPENAI_BATCH.sh

=============================================================================
get_new_hex_desc_OPENAI_BATCH.sh - I Ching Hexagram Description Generator
=============================================================================

Description:
This script automates the generation of hexagram descriptions by iterating
through all 64 hexagrams using OpenAI's API. For each hexagram, it calls
get_new_hex_desc_OPENAI.py to generate and save descriptions.

Usage:
./get_new_hex_desc_OPENAI_BATCH.sh

Process:
1. Loops through numbers 1-64
2. For each number, formats it with leading zeros (01, 02, etc.)
3. Calls get_new_hex_desc_OPENAI.py with the formatted number
4. Automatically saves results (--save flag)

Dependencies:
- get_new_hex_desc_OPENAI.py script in same directory
- Python environment with required packages
- Valid OpenAI API key in environment

Note:
This is a batch processing script that will process all hexagrams
sequentially. Be aware of OpenAI API rate limits and costs when
running this script.

Author: JW
Last Updated: 2024
=============================================================================
Loop from 01 to 64

---

## get_new_image_desc_OPENAI_BATCH.sh

=============================================================================
get_new_image_desc_OPENAI_BATCH.sh - I Ching Image Description Generator
=============================================================================

Description:
This script automates the generation of image descriptions by iterating
through all 64 hexagrams using OpenAI's API. For each hexagram, it calls
get_new_image_desc_OPENAI.py to generate and save image descriptions.

Usage:
./get_new_image_desc_OPENAI_BATCH.sh

Process:
1. Loops through numbers 1-64
2. For each number, formats it with leading zeros (01, 02, etc.)
3. Calls get_new_image_desc_OPENAI.py with the formatted number
4. Automatically saves results (--save flag)

Dependencies:
- get_new_image_desc_OPENAI.py script in same directory
- Python environment with required packages
- Valid OpenAI API key in environment
- Access to GPT-4 Vision model in your OpenAI account

Note:
This is a batch processing script that will process all hexagram images
sequentially. Be aware of OpenAI API rate limits and costs when
running this script, especially for vision API calls.

Author: JW
Last Updated: 2024
=============================================================================
Loop from 01 to 64

---

## joe_BATCH.sh

=============================================================================
joe_BATCH.sh - I Ching Hexagram File Editor Batch Script
=============================================================================

Description:
This script automates the process of opening hexagram text files in sequence
using the Visual Studio Code editor. It iterates through hexagrams 23-64,
allowing for systematic review and editing of hexagram files.

Usage:
./joe_BATCH.sh

Process:
1. Loops through hexagram numbers 23 to 64
2. Formats each number with leading zeros (e.g., 23 becomes "23")
3. Opens corresponding hexagram text file in VS Code

Dependencies:
- Visual Studio Code (code command)
- Hexagram text files in /home/jw/src/iching_cli/defs/v2/

File Structure:
- Input: /home/jw/src/iching_cli/defs/v2/XX_hex.txt
where XX is the hexagram number (23-64)

Author: JW
Last Updated: 2024
=============================================================================
Loop from 24 to 64

---

## line_types_BATCH.sh

=============================================================================
line_types_BATCH.sh - I Ching Line Types Generator Batch Script
=============================================================================

Description:
This script automates the process of generating line types for all 64
hexagrams. It converts binary sequences into yin/yang line types and
updates or creates the line_type array in each hexagram's JSON file.

Usage:
./line_types_BATCH.sh

Process:
1. Loops through hexagram numbers 1 to 64
2. Formats each number with leading zeros (01, 02, etc.)
3. Calls line_types.py for each hexagram with --save flag
4. Updates line_type array in corresponding JSON file

Dependencies:
- line_types.py script in same directory
- Python environment with required packages
- Hexagram JSON files in ../regen/ directory

File Structure:
- Input/Output: ../regen/XX.json
where XX is the hexagram number (01-64)

Author: JW
Last Updated: 2024
=============================================================================
Loop from 1 to 64

---

## post.sh

./makeallmd.py
typora docs/iching.md
makebook_postonly.sh
This script automates the process of generating a final PDF document for the I Ching book.
It performs the following steps:
1. Removes any existing final PDF to ensure a clean build.
2. Uses Prince to convert HTML content into a PDF, applying specific styles for print.
3. Merges additional pages (cover and copyright) into the final PDF using pdftk.
4. Opens the final PDF in Okular for review.
Steps:
1. Remove the existing FINAL_iching.pdf to avoid conflicts with previous builds.
2. Use Prince to convert iching.html to iching.pdf, applying styles from iching.css.
3. Merge COVER_PAGE.pdf and COPYRIGHT_PAGE.pdf with iching.pdf to create FINAL_iching.pdf.
4. Open the resulting FINAL_iching.pdf in Okular for viewing.
Usage:
Run this script from the command line to generate and view the final I Ching book PDF.
Dependencies:
- Prince: A tool for converting HTML and CSS to PDF.
- pdftk: A tool for manipulating PDF documents.
- Okular: A PDF viewer for reviewing the final document.
Note:
Ensure all input files (COVER_PAGE.pdf, COPYRIGHT_PAGE.pdf, iching.html) are present in the expected directories.

---

## prep.sh

=============================================================================
prep.sh - I Ching Book Preparation Script
=============================================================================

Description:
This script prepares the I Ching book for PDF generation by setting up
necessary files, compiling styles, and initiating the document generation
process. It ensures a clean build environment and consistent styling.

Usage:
./prep.sh [version_suffix]
Example: ./prep.sh v2    # Will use files with "_v2" suffix

Process:
1. Clean Build Environment:
- Remove existing HTML and MD files
- Ensure fresh start for new build
2. Style Compilation:
- Compile iching.less to iching.css
- Compile iching_nopage.less to iching_nopage.css
3. Typora Configuration:
- Copy compiled CSS to Typora themes
- Set up both paged and non-paged variants
4. Document Generation:
- Run makeallmd.py to create markdown
- Open in Typora for manual export

Dependencies:
- lessc: LESS CSS compiler
- Typora: Markdown editor
- makeallmd.py: Markdown generation script

File Structure:
Input:
- ../includes/iching.less
- ../includes/iching_nopage.less
Output:
- ../includes/iching.css
- ../includes/iching_nopage.css
- ~/.config/Typora/themes/iching_7_44-9_68.css
- ~/.config/Typora/themes/iching_7_44-9_68_nopage.css

Notes:
- Ensure Typora is properly configured with theme directory
- Manual export to HTML required after script completion

Author: JW
Last Updated: 2024
=============================================================================
makebook.sh
Usage: ./makebook_pre.sh [version_suffix]
Example: ./makebook_pre.sh v2    # Will use files with "_v2" suffix
This script prepares the I Ching book for PDF generation by performing the following tasks:
1. Cleans up previous HTML and Markdown files to ensure a fresh build.
2. Compiles LESS stylesheets into CSS for use in Typora and Prince.
3. Copies the latest CSS to Typora's theme directory for consistent styling.
4. Generates the Markdown document for the I Ching book using makeallmd.py.
5. Opens the generated Markdown in Typora for manual export to HTML.
6. After exporting, makebook_postonly.sh is called from Typora to finalize the PDF.
Steps:
1. Remove existing iching.html and iching.md files to avoid conflicts.
2. Compile iching.less into iching.css using lessc.
3. Copy the compiled CSS to Typora's theme directory.
4. Generate the Markdown document using makeallmd.py with the --content pages option.
5. Open the generated iching.md in Typora for review and export.
Usage:
Run this script to prepare the I Ching book for PDF generation. After running, use Typora to export the Markdown to HTML.
Dependencies:
- lessc: A tool for compiling LESS to CSS.
- Typora: A Markdown editor for reviewing and exporting the document.
- makeallmd.py: A Python script for generating the Markdown document.
Note:
Ensure all input files and dependencies are present and correctly configured before running the script.

---

## regen_lines_in_context_BATCH.sh

=============================================================================
regen_lines_in_context_BATCH.sh - I Ching Line Context Regenerator
=============================================================================

Description:
This script automates the regeneration of line context data for all
hexagrams from 2 to 64. It iterates through each hexagram number,
calling regen_lines_in_context_HEX.sh for each one.

Usage:
./regen_lines_in_context_BATCH.sh

Process:
1. Loops through hexagram numbers 2 to 64
2. Formats each number with leading zeros (02, 03, etc.)
3. Calls regen_lines_in_context_HEX.sh for each hexagram

Dependencies:
- regen_lines_in_context_HEX.sh script in same directory

File Structure:
- Input/Output: Handled by regen_lines_in_context_HEX.sh

Author: JW
Last Updated: 2024
=============================================================================
Loop from 1 to 64

---

## regen_lines_in_context_HEX.sh

=============================================================================
regen_lines_in_context_HEX.sh - I Ching Hexagram Line Context Generator
=============================================================================

Description:
This script regenerates line context data for a specific I Ching hexagram.
It processes each line (0-2) of the specified hexagram, updating the
contextual information in the corresponding files.

Usage:
./regen_lines_in_context_HEX.sh <hexagram_number>

Arguments:
hexagram_number: Number of the hexagram (1-64)

Examples:
./regen_lines_in_context_HEX.sh 1    # Process hexagram 1

Process:
1. Validates input hexagram number (1-64)
2. For each line (0-2):
- Calls regen_lines_in_context.py
- Updates context data in ../regen directory

Dependencies:
- regen_lines_in_context.py script
- Python environment with required packages

File Structure:
- Input/Output: ../regen/<hexagram_number>_*.json

Error Handling:
- Validates number of arguments
- Ensures hexagram number is valid integer
- Checks range (1-64)

Author: JW
Last Updated: 2024
=============================================================================
Check if exactly one argument is provided

---

## regen_lines_in_history_BATCH.sh

=============================================================================
regen_lines_in_history_BATCH.sh - I Ching Line History Regenerator
=============================================================================

Description:
This script automates the regeneration of line history data for all
hexagrams from 2 to 64. It iterates through each hexagram number,
calling regen_lines_in_history.py for each one.

Usage:
./regen_lines_in_history_BATCH.sh

Process:
1. Loops through hexagram numbers 2 to 64
2. Formats each number with leading zeros (02, 03, etc.)
3. Calls regen_lines_in_history.py for each hexagram

Dependencies:
- regen_lines_in_history.py script in same directory
- Python environment with required packages

File Structure:
- Input/Output: ../regen/<hexagram_number>.json

Author: JW
Last Updated: 2024
=============================================================================
Loop from 1 to 64

---

## regen_trigram_phrase_BATCH.sh

=============================================================================
regen_trigram_phrase_BATCH.sh - I Ching Trigram Phrase Batch Generator
=============================================================================

Description:
This script automates the regeneration of trigram phrases for all hexagrams
from 1 to 64. It iterates through each hexagram number, calling
regen_trigram_phrase.py for each one to generate new interpretations of
the upper and lower trigram combinations.

Usage:
./regen_trigram_phrase_BATCH.sh

Process:
1. Loops through hexagram numbers 1 to 64
2. Formats each number with leading zeros (01, 02, etc.)
3. Calls regen_trigram_phrase.py with --save flag for each hexagram

Dependencies:
- regen_trigram_phrase.py script in same directory
- Python environment with required packages

File Structure:
- Input/Output: ../regen/<hexagram_number>.json

Author: JW
Last Updated: 2024
=============================================================================
Loop from 1 to 64

---

