get_new_hex_desc_LOCAL.py
get_new_hex_desc_OPENAI.py
get_new_image_desc_OPENAI.py
get_openai_models_list.py
line_types.py
make_doc_py.py
makeallmd.py
print_fields.py
print_json_paths.py
regen_lines_in_context.py
regen_lines_in_history.py
regen_lines_in_trans.py
regen_titles.py
regen_trigram_phrase.py
regen_trigrams.py
reorg.py
version_utils.py


# Python Scripts Documentation

This document contains the documentation for all Python scripts in the current directory.

---

# Script Usage Index

Detailed usage instructions for each script:

- [get_new_hex_desc_LOCAL.py](#get_new_hex_desc_local.py)
  ```
  python get_new_hex_desc_LOCAL.py [-s] <hexagram_number>
  ```

- [get_new_hex_desc_OPENAI.py](#get_new_hex_desc_openai.py)
  ```
  python get_new_hex_desc_OPENAI.py [-s] <hexagram_number>
  ```

- [get_new_image_desc_OPENAI.py](#get_new_image_desc_openai.py)
  ```
  python get_new_image_desc_OPENAI.py [-s] <hexagram_number>
  ```

- [get_openai_models_list.py](#get_openai_models_list.py)
  ```
  python get_openai_models_list.py
  ```

- [line_types.py](#line_types.py)
  ```
  ./line_types.py <json_file> [--save]
  ```

- [make_doc_py.py](#make_doc_py.py)
  ```
  ./make_doc_py.py
  ```

- [makeallmd.py](#makeallmd.py)
  ```
  python makeallmd.py [--content {all,pages}]
  ```

- [print_fields.py](#print_fields.py)
  ```
  ./print_fields.py
  ```

- [print_json_paths.py](#print_json_paths.py)
  ```
  ./print_json_paths.py <file_path>
  ```

- [regen_lines_in_context.py](#regen_lines_in_context.py)
  ```
  ./regen_lines_in_context.py <source_dir> <hexagram_number> <story_index>
  ```

- [regen_lines_in_history.py](#regen_lines_in_history.py)
  ```
  ./regen_lines_in_history.py <source_dir> <hexagram_number>
  ```

- [regen_lines_in_trans.py](#regen_lines_in_trans.py)
  ```
  ./regen_lines_in_trans.py <source_dir> <dest_dir>
  ```

- [regen_titles.py](#regen_titles.py)
  ```
  ./regen_titles.py <source_dir> <hexagram_number>
  ```

- [regen_trigram_phrase.py](#regen_trigram_phrase.py)
  ```
  ./regen_trigram_phrase.py <source_dir> <hexagram_number> [--save]
  ```

- [regen_trigrams.py](#regen_trigrams.py)
  ```
  ./regen_trigrams.py <source_dir> <hexagram_number>
  ```

- [reorg.py](#reorg.py)
  ```
  reorg.py [-h] input_pdf output_pdf
  ```

---

# Script Documentation

## get_new_hex_desc_LOCAL.py

=============================================================================
get_new_hex_desc_LOCAL.py - I Ching Hexagram Description Generator
=============================================================================

Description:
  This script generates descriptive paragraphs for I Ching hexagrams using AI.
  For each hexagram, it generates two narrative paragraphs:
  1. A general description of the hexagram's archetypal meaning
  2. A description relating to tholonic concepts specific to the hexagram

Usage:
  python get_new_hex_desc_LOCAL.py [-s] <hexagram_number>

Arguments:
  hexagram_number: Number of the hexagram (1-64)
  -s, --save: Save the output to a text file

Examples:
  python get_new_hex_desc_LOCAL.py 20         # Display output only
  python get_new_hex_desc_LOCAL.py -s 20      # Display and save output

Process:
  1. Reads context from local files (tholonic_primer.md and hexagram JSON)
  2. Sends context to local AI server for processing
  3. Generates two formatted paragraphs
  4. Optionally saves output to text file

Dependencies:
  - OpenAI API key (can be any string when using local server)
  - Local AI server running on http://127.0.0.1:1234/v1
  - Required Python packages: openai, colorama

File Structure:
  - Input: /book/tholonic_primer.md
  - Input: /book/v2/<hexagram_number>.json
  - Output: /book/v2/<hexagram_number>_hex.txt (when using --save)

Author: JW
Last Updated: 2024
=============================================================================

---

## get_new_hex_desc_OPENAI.py

=============================================================================
get_new_hex_desc_OPENAI.py - I Ching Hexagram Description Generator
=============================================================================

Description:
  This script generates descriptive paragraphs for I Ching hexagrams using
  OpenAI's GPT-4 API. For each hexagram, it generates two narrative paragraphs:
  1. A general description of the hexagram's archetypal meaning
  2. A description relating to tholonic concepts specific to the hexagram

Usage:
  python get_new_hex_desc_OPENAI.py [-s] <hexagram_number>

Arguments:
  hexagram_number: Number of the hexagram (1-64)
  -s, --save: Save the output to a text file

Examples:
  python get_new_hex_desc_OPENAI.py 20         # Display output only
  python get_new_hex_desc_OPENAI.py -s 20      # Display and save output

Process:
  1. Reads context from local files (tholonic_primer.md and hexagram JSON)
  2. Sends context to OpenAI's GPT-4 API for processing
  3. Generates two formatted paragraphs
  4. Optionally saves output to text file

Dependencies:
  - OpenAI Python package (v1.0.0 or later)
  - Valid OpenAI API key set in OPENAI_API_KEY environment variable
  - Access to GPT-4 model in your OpenAI account
  - Required Python packages: openai, colorama

File Structure:
  - Input: /book/tholonic_primer.md
  - Input: /book/v2/<hexagram_number>.json
  - Output: /book/v2/<hexagram_number>_hex.txt (when using --save)

Environment Variables:
  OPENAI_API_KEY: Your OpenAI API key (required)

Author: JW
Last Updated: 2024
=============================================================================

---

## get_new_image_desc_OPENAI.py

=============================================================================
get_new_image_desc_OPENAI.py - I Ching Hexagram Image Description Generator
=============================================================================

Description:
  This script generates AI-powered descriptions of I Ching hexagram images using
  OpenAI's GPT-4 Vision API. For each hexagram image, it generates a narrative
  paragraph explaining why specific visual elements and styles were chosen to
  represent that hexagram.

Usage:
  python get_new_image_desc_OPENAI.py [-s] <hexagram_number>

Arguments:
  hexagram_number: Number of the hexagram (1-64)
  -s, --save: Save the output to a text file

Examples:
  python get_new_image_desc_OPENAI.py 20         # Display output only
  python get_new_image_desc_OPENAI.py -s 20      # Display and save output

Process:
  1. Reads hexagram image and context files
  2. Converts image to base64 for API submission
  3. Sends image and context to OpenAI's Vision API
  4. Generates a formatted description paragraph
  5. Optionally saves output to text file

Dependencies:
  - OpenAI Python package (v1.0.0 or later)
  - Valid OpenAI API key set in OPENAI_API_KEY environment variable
  - Access to GPT-4 Vision model in your OpenAI account
  - Required Python packages: openai, colorama

File Structure:
  - Input: /book/tholonic_primer.md
  - Input: /book/v2/<hexagram_number>.json
  - Input: /book/v2/<hexagram_number>.png
  - Output: /book/v2/<hexagram_number>_img.txt (when using --save)

Environment Variables:
  OPENAI_API_KEY: Your OpenAI API key (required)

Note:
  Vision API calls may have higher costs than standard GPT-4 calls.
  Ensure proper rate limiting and cost monitoring when using this script.

Author: JW
Last Updated: 2024
=============================================================================

---

## get_openai_models_list.py

=============================================================================
get_openai_models_list.py - OpenAI Models List Generator
=============================================================================

Description:
  This script retrieves and displays a list of all available OpenAI models
  with their creation dates. The output is sorted chronologically, making it
  easy to see the evolution of available models.

Usage:
  python get_openai_models_list.py

Output Format:
  (creation_date, model_id)
  Example: ('2023-12-01 12:00:00', 'gpt-4-1106-preview')

Process:
  1. Connects to OpenAI API using provided credentials
  2. Retrieves complete list of available models
  3. Converts Unix timestamps to readable dates
  4. Sorts models by creation date
  5. Displays formatted results

Dependencies:
  - OpenAI Python package (v1.0.0 or later)
  - Valid OpenAI API key set in OPENAI_API_KEY environment variable

Environment Variables:
  OPENAI_API_KEY: Your OpenAI API key (required)

Author: JW
Last Updated: 2024
=============================================================================

---

## line_types.py

=============================================================================
line_types.py - I Ching Line Type Generator
=============================================================================

Description:
  This script processes hexagram JSON files to create or update line_type
  values based on binary sequences. It converts 6-digit binary numbers into
  an array of yin/yang symbols (⚊/⚋) for each hexagram.

Usage:
  ./line_types.py <json_file> [--save]

Arguments:
  json_file: Path to the hexagram JSON file to process
  --save: Optional flag to save changes back to the JSON file

Examples:
  ./line_types.py hexagram.json         # Display output only
  ./line_types.py hexagram.json --save  # Update JSON file

Process:
  1. Reads binary_sequence from input JSON file
  2. Converts to 6-digit binary string with zero padding
  3. Maps binary digits to yin/yang symbols (1->⚊, 0->⚋)
  4. Updates line_type array in JSON
  5. Optionally saves back to file

Dependencies:
  - Python 3.x
  - Required modules: json, argparse, sys

File Structure:
  - Input/Output: JSON file containing:
    - binary_sequence: Integer (0-63)
    - line_type: Array of 6 symbols

Author: JW
Last Updated: 2024
=============================================================================

---

## make_doc_py.py

=============================================================================
make_doc_py.py - Python Documentation Collector with Usage Index
=============================================================================

Description:
  This script scans the current directory for Python files (*.py), extracts
  their documentation comments, and compiles them into a single markdown file
  with an index of script usages at the top.

Usage:
  ./make_doc_py.py

Process:
  1. Scans current directory for *.py files
  2. For each Python file:
     - Extracts the docstring between first set of triple quotes
     - Extracts usage information
     - Converts to markdown format
  3. Creates script list and usage index
  4. Combines all sections into doc_py.md

Output:
  - doc_py.md: Combined markdown documentation with script list and usage index

Author: Assistant
Last Updated: 2024
=============================================================================

---

## makeallmd.py

=============================================================================
makeallmd.py - I Ching Book Generator
=============================================================================

Description:
  This script generates a formatted markdown document for the I Ching book by
  combining introduction text, hexagram data, generated descriptions, and
  images into a cohesive document.

Usage:
  python makeallmd.py [--content {all,pages}]

Arguments:
  --content: Choose content to include
    all: Include introduction and hexagram pages (default)
    pages: Include only hexagram pages

Process:
  1. Processes hexagrams defined in HEXAGRAMS list
  2. For each hexagram, generates sections for:
     - Title and basic information
     - Core hexagram description and image
     - Line-by-line interpretations
     - Three thematic stories
     - Historical context
     - Notes section
  3. Formats content with:
     - Proper page breaks for book layout
     - Consistent heading hierarchy
     - Structured lists for line interpretations
     - Image placement and captions

Dependencies:
  - Required Python packages:
    - colorama: Terminal output formatting
    - openai: GPT-4 API for literary descriptions
    - pyyaml: YAML frontmatter handling
    - json: JSON data parsing
    - re: Regular expression text processing

File Structure:
  Input:
    - /BOOK_INTRO.md: Introduction text
    - /*.json: Hexagram data files (XX.json where XX is hexagram number)
    - /*_img.txt: Cached image descriptions
    - /*_hex.txt: Cached hexagram descriptions
    - /export.yaml: Document metadata and configuration
  Output:
    - docs/iching.md: Complete markdown document ready for PDF conversion

Environment:
  - OPENAI_API_KEY: OpenAI API key for generating descriptions
  - ROOT: Base directory containing required input files

Author: JW
Last Updated: 2024
=============================================================================

---

## print_fields.py

=============================================================================
print_fields.py - I Ching Hexagram Field Extractor
=============================================================================

Description:
  This script extracts and displays specific fields from hexagram JSON files.
  It focuses on the "lines_in_transition" data, showing the first four words
  of each line's description for quick reference and verification.

Usage:
  ./print_fields.py

Process:
  1. Scans ../_v2 directory for JSON files
  2. For each hexagram file:
     - Extracts "lines_in_transition" data
     - Shows first four words for lines 1-6
     - Displays in order by hexagram number

Dependencies:
  - Python 3.x
  - Required modules: json, os

File Structure:
  Input:
    - ../_v2/*.json: Hexagram JSON files
  Output Format:
    --- filename.json ---
    [first four words of line 6]
    [first four words of line 5]
    ...etc

Author: JW
Last Updated: 2024
=============================================================================

---

## print_json_paths.py

=============================================================================
print_json_paths.py - JSON Path Structure Analyzer
=============================================================================

Description:
  This script processes a JSON file and prints all paths to each value in
  the JSON structure. It helps visualize and analyze the hierarchical
  structure of JSON data by showing complete paths to all values.

Usage:
  ./print_json_paths.py <file_path>

Arguments:
  file_path: Full path to the JSON file to analyze

Process:
  1. Reads the specified JSON file
  2. Recursively traverses the JSON structure
  3. For each element encountered:
     - Builds the complete path using dot notation
     - Handles both objects and arrays
     - Prints each unique path

Dependencies:
  - Python 3.x
  - Required modules: json, argparse, pathlib

Output Format:
  Paths for example.json:
  key1
  key1.subkey1
  key1.array[0]
  key1.array[1]
  ...etc

Author: JW
Last Updated: 2024
=============================================================================

---

## regen_lines_in_context.py

Generate six stages of change for a specific story in I Ching Hexagrams using OpenAI API.

This script loads a JSON file from a specified source directory based on the hexagram number, extracts a specific story by index, and uses the OpenAI API to generate the six stages of change. It updates the JSON file with the new data, including a name, meaning, and changing description for each line.

Usage:
    ./regen_lines_in_context.py <source_dir> <hexagram_number> <story_index>

Required Arguments:
    source_dir: The directory containing the source JSON files
    hexagram_number: The number of the hexagram to process (1-64)
    story_index: The index of the story to process (0-based index)

Example:
    ./regen_lines_in_context.py ../regen 01 0

Process:
    1. Validates input arguments and file paths
    2. Loads hexagram data from JSON file
    3. Extracts specified story by index
    4. Generates six stages of change using OpenAI API
    5. Updates JSON with new line data:
       - name: Concept title for the stage
       - meaning: Description of the stage
       - changing: Interpretation when line changes

Dependencies:
    - OpenAI Python package (v1.0.0 or later)
    - colorama: Terminal output formatting
    - Required files:
      - ../includes/iching_primer.md
      - ../includes/tholonic_primer.md

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required)

File Structure:
    Input:
        - <source_dir>/<hexagram_number>.json
        - ../includes/iching_primer.md
        - ../includes/tholonic_primer.md
    Output:
        - Updated JSON file with new lines_in_context data

Author: JW
Last Updated: 2024

---

## regen_lines_in_history.py

=============================================================================
regen_lines_in_history.py - I Ching Line History Generator
=============================================================================

Description:
  This script generates the six stages of change for a specific hexagram's
  history section using the OpenAI API. It processes a JSON file containing
  hexagram data and updates it with generated line-by-line interpretations.

Usage:
  ./regen_lines_in_history.py <source_dir> <hexagram_number>

Arguments:
  source_dir: Directory containing hexagram JSON files
  hexagram_number: Number of hexagram to process (1-64)

Process:
  1. Validates input arguments and file existence
  2. Loads hexagram JSON data
  3. Extracts history section
  4. Uses OpenAI API to generate line interpretations
  5. Updates JSON with new line data:
     - name: Concept name for the line
     - meaning: Line interpretation
     - changing: Meaning when line changes

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  - Input/Output: <source_dir>/<hexagram_number>.json

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Author: JW
Last Updated: 2024
=============================================================================

---

## regen_lines_in_trans.py

=============================================================================
regen_lines_in_trans.py - I Ching Line Transition Generator
=============================================================================

Description:
  This script generates line transition interpretations for I Ching hexagrams
  using the OpenAI API. It processes JSON files containing hexagram data and
  updates them with new line-by-line transition meanings. For each line,
  it generates a name, meaning, and changing line interpretation based on
  the hexagram's context.

Usage:
  ./regen_lines_in_trans.py <source_dir> <dest_dir>

Arguments:
  source_dir: Directory containing source hexagram JSON files
  dest_dir: Directory to write updated JSON files

Process:
  1. Validates input/output directories
  2. Loads hexagram JSON data
  3. For each hexagram (1-64):
     - Extracts hexagram context and data
     - Uses OpenAI API to generate line transitions
     - For each line (1-6):
       * Generates name capturing transition concept
       * Generates meaning interpretation
       * Generates changing line interpretation
  4. Updates JSON with new line data
  5. Saves to destination directory

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  - Input: <source_dir>/<hexagram>.json
  - Output: <dest_dir>/<hexagram>.json

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Error Handling:
  - Validates directory paths
  - Ensures valid JSON formatting
  - Handles API errors gracefully

Author: JW
Last Updated: 2024
=============================================================================

---

## regen_titles.py

=============================================================================
regen_titles.py - I Ching Hexagram Title Generator
=============================================================================

Description:
  This script uses the OpenAI API to generate a concise one- or two-word title
  that best expresses the core concept of a specific I Ching hexagram. It
  processes a JSON file containing hexagram data and updates the title based
  on the hexagram's meaning and context.

Usage:
  ./regen_titles.py <source_dir> <hexagram_number>

Arguments:
  source_dir: Directory containing hexagram JSON files
  hexagram_number: Number of hexagram to process (1-64)

Process:
  1. Validates input arguments and file existence
  2. Loads hexagram JSON data
  3. Extracts current hexagram name
  4. Uses OpenAI API to generate new concise title
  5. Updates JSON with new title

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  - Input/Output: <source_dir>/<hexagram_number>.json

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Author: JW
Last Updated: 2024
=============================================================================

---

## regen_trigram_phrase.py

=============================================================================
regen_trigram_phrase.py - I Ching Trigram Phrase Generator
=============================================================================

Description:
  This script generates interpretive phrases for I Ching hexagrams based on
  their upper and lower trigram combinations using the OpenAI API. It processes
  a JSON file containing hexagram data and can update it with the new trigram
  interpretation.

Usage:
  ./regen_trigram_phrase.py <source_dir> <hexagram_number> [--save]

Arguments:
  source_dir: Directory containing hexagram JSON files
  hexagram_number: Number of hexagram to process (1-64)
  --save: Optional flag to save changes to JSON file

Process:
  1. Validates input arguments and file existence
  2. Loads hexagram JSON data
  3. Extracts trigram information
  4. Uses OpenAI API to generate interpretive phrase
  5. Optionally updates JSON with new phrase

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  - Input/Output: <source_dir>/<hexagram_number>.json

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Author: JW
Last Updated: 2024
=============================================================================

---

## regen_trigrams.py

=============================================================================
regen_trigrams.py - I Ching Trigram Generator
=============================================================================

Description:
  This script generates interpretations of trigram combinations for I Ching
  hexagrams using the OpenAI API. It processes a JSON file containing hexagram
  data and updates it with new trigram-based interpretations that reflect the
  interaction between the upper and lower trigrams.

Usage:
  ./regen_trigrams.py <source_dir> <hexagram_number>

Arguments:
  source_dir: Directory containing hexagram JSON files
  hexagram_number: Number of hexagram to process (1-64)

Process:
  1. Validates input arguments and file existence
  2. Loads hexagram JSON data
  3. Extracts trigram information
  4. Uses OpenAI API to generate interpretations
  5. Updates JSON with new trigram data

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  - Input/Output: <source_dir>/<hexagram_number>.json

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Author: JW
Last Updated: 2024
=============================================================================

---

## reorg.py

=============================================================================
reorg.py - I Ching PDF Page Reorganizer
=============================================================================

Description:
  This script processes a PDF file containing I Ching hexagram entries and adds
  blank pages before each hexagram to ensure proper double-sided printing layout.
  It's specifically designed for book printing where hexagrams should start on
  right-hand (odd-numbered) pages.

Usage:
  reorg.py [-h] input_pdf output_pdf

Arguments:
  input_pdf: Path to input PDF file
  output_pdf: Path to output PDF file

Process:
  1. Detects hexagram entries by:
     - Unicode hexagram symbols (U+4DC0 to U+4DFF)
     - Large font titles in format "1 ䷀ 63 - Creation"
  2. Inserts blank pages before hexagrams for proper layout
  3. Preserves first 3 pages (table of contents)
  4. Only checks odd-numbered pages for hexagrams
  5. Processes PDF iteratively to handle large files
  6. Maintains PDF dimensions and properties

Input Format:
  - PDF file with I Ching hexagram entries
  - Each hexagram entry starts with titled hexagram symbol
  - First 3 pages contain table of contents

Output Format:
  - Modified PDF with blank pages inserted
  - Hexagrams start on right-hand pages
  - Original content unchanged except for page positioning

Dependencies:
  - PyMuPDF (fitz) for PDF content analysis
  - pdfrw for PDF manipulation

Example:
  reorg.py docs/clean_iching.pdf docs/reorg.pdf

Author: JW
Last Updated: 2024
=============================================================================

---

## version_utils.py

=============================================================================
version_utils.py - Version Management Utilities
=============================================================================

Description:
  This script provides utility functions for managing semantic versioning
  in the project. It handles reading, incrementing, and updating version
  numbers stored in a VERSION file.

Functions:
  - read_version(): Reads current version from VERSION file
  - increment_version(version_str): Increments patch version number
  - update_version(): Updates VERSION file with incremented version

Version Format:
  major.minor.patch (e.g., 1.2.3)
  - Patch increments normally (0-99)
  - Minor increments when patch > 99
  - Major increments when minor > 99

Dependencies:
  - Python 3.x standard library (os, pathlib)

File Structure:
  - VERSION file in parent directory

Author: JW
Last Updated: 2024
=============================================================================

---

