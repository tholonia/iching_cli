# execute_pair_workflow.py

=============================================================================
execute_pair_workflow.py - ComfyUI Workflow Executor
=============================================================================

Description:
    This script executes a generated ComfyUI workflow for image pair blending.
    It connects to a local ComfyUI server, queues the workflow, and monitors
    its execution progress.

Usage:
    ./execute_pair_workflow.py <workflow.json>

Arguments:
    workflow.json       JSON workflow file to execute

Dependencies:
    - Python 3.x
    - requests
    - websocket-client
    - json

Output:
    - Status updates during execution
    - Generated image in ComfyUI output directory

Example:
    ./execute_pair_workflow.py workflow.json

Author: JW
Last Updated: 2024
=============================================================================


# funcs_lib.py

=============================================================================
funcs_lib.py - Common Functions Library
=============================================================================

Description:
    A collection of utility functions for making API calls to various AI providers
    and handling common tasks across the I Ching CLI tools.

Functions:
    call_ai_api(prompt, system_message, model, provider) -> str
        Makes API calls to various AI providers (OpenAI, Google, Anthropic, Grok)
        and returns the response text.

Usage:
    from funcs_lib import call_ai_api

    response = call_ai_api(
        prompt="Your prompt here",
        system_message="System context here",
        model="gpt-4",
        provider="openai"
    )

Supported Providers:
    - OpenAI (provider="openai")
        Models: gpt-4, gpt-3.5-turbo, etc.
        Requires: OPENAI_API_KEY environment variable

    - Google (provider="google")
        Models: gemini-pro, etc.
        Requires: GOOGLE_API_KEY environment variable

    - Anthropic (provider="anthropic")
        Models: claude-3, etc.
        Requires: ANTHROPIC_API_KEY environment variable

    - Grok (provider="grok") [Not yet implemented]
        Requires: GROK_API_KEY environment variable

Dependencies:
    - openai
    - google-cloud-aiplatform
    - anthropic
    - colorama
    - python-dotenv (recommended for API key management)

Author: JW
Last Updated: 2024
=============================================================================


# gen_pair_images.py

=============================================================================
gen_pair_images.py - ComfyUI Image Pair Blending Workflow Generator
=============================================================================

Description:
    This script generates and optionally executes a ComfyUI workflow that
    blends two input images using a VAE-based latent space blending technique.

Usage:
    ./gen_pair_images.py <image1> <image2> [options]

    batch with:
    cat ../includes/pairs.csv \
    | awk -F "," '{printf "./gen_pair_images.py %02d.png %02d.png --prefix %02d --execute --queue\n", $2, $3, $1}' |tail -32 > x.sh


Arguments:
    image1              First input image filename
    image2              Second input image filename
    --prefix PREFIX     Prefix for output filename (default: p06)
    --output OUTPUT     Output JSON filename (default: workflow.json)
    --server SERVER     ComfyUI server URL (default: http://localhost:8188)
    --execute          Execute the workflow after generation
    --queue            Queue the workflow to ComfyUI server (deprecated, use --execute)

Dependencies:
    - Python 3.x
    - requests
    - websocket-client
    - uuid
    - json
    - argparse
    - random

Output:
    - JSON workflow file
    - Generated image with specified prefix (when executed)

Example:
    ./gen_pair_images.py image1.png image2.png --prefix blend01 --execute

Author: JW
Last Updated: 2024
=============================================================================


# gen_schema.py

=============================================================================
gen_schema.py - JSON Schema Generator for I Ching Data
=============================================================================

Description:
  This script generates a JSON schema from an input JSON file, specifically
  designed for I Ching data structures. It analyzes the structure and data
  types of the input JSON and creates a corresponding schema that describes
  the format and validation rules for hexagram data files.

Usage:
  ./gen_schema.py <input_json_file>

  Example:
    ./gen_schema.py ../regen/01.json

Process:
  1. Reads input JSON file (typically a hexagram data file)
  2. Analyzes structure recursively:
     - Determines data types for all fields
     - Identifies required fields (non-null values)
     - Handles arrays and nested objects
     - Processes special I Ching specific structures
  3. Generates schema with:
     - Property definitions for hexagram data
     - Type information for all fields
     - Required field lists
     - Validation rules for I Ching specific data
  4. Saves schema to schema.json

Arguments:
  input_json_file    Path to the input JSON file to analyze
                     (typically a hexagram JSON file from ../regen/)

Output:
  - schema.json: Generated JSON schema file that describes the hexagram
                data format and validation rules

Schema Features:
  - Validates hexagram structure
  - Enforces required fields
  - Type checking for all properties
  - Handles nested objects (trigrams, lines, etc.)
  - Array validation for line data
  - Special handling for I Ching specific fields

Dependencies:
  - Python 3.x
  - json (standard library)
  - typing

Author: Assistant
Last Updated: 2024-03-21
=============================================================================


# get_new_hex_desc_LOCAL.py

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


# get_new_hex_desc_OPENAI.py

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


# get_new_image_desc_OPENAI.py

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


# get_openai_models_list.py

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


# hexbinvals.py

=============================================================================
hexbinvals.py - Hexagram Binary Value Extractor
=============================================================================

Description:
  This script extracts and displays hexagram binary sequences and their
  corresponding hex values from JSON files. It processes one or more hexagram
  numbers provided as command-line arguments.

Usage:
  python hexbinvals.py num1,num2,num3,...
  Example: python hexbinvals.py 1,2,3

Arguments:
  numbers: Comma-separated list of hexagram numbers to process
          Numbers will be zero-padded to two digits (1 -> "01")

Process:
  1. Accepts comma-separated hexagram numbers from command line
  2. Converts numbers to zero-padded two-digit strings
  3. Loads corresponding JSON files from regen directory
  4. Extracts hex ID and binary sequence for each hexagram
  5. Displays results in format: "Hex X = binary_sequence"

Dependencies:
  - json: JSON file parsing
  - pathlib: Cross-platform path handling
  - sys: Command line argument processing

File Structure:
  Input:
    - ../regen/XX.json: Hexagram data files where XX is hexagram number
    Each JSON file contains:
      - id: Hexagram identifier
      - binary_sequence: Binary representation of hexagram

Output Format:
  Hex <id> = <binary_sequence>
  Example: "Hex 01 = 111111"

Error Handling:
  - Validates command line arguments
  - Checks for file existence
  - Verifies JSON structure
  - Reports specific error messages for each failure case

Author: JW
Last Updated: 2024
=============================================================================


# line_types.py

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


# make_doc_python.py

=============================================================================
make_doc_py.py - Python Documentation Collector with Usage Index
=============================================================================

Description:
  This script provides two main functions:
  1. Processes Python files and converts their documentation to markdown format
  2. Checks Python files for 'Last Updated' field in their docstrings

Usage:
  Process files:
    ./make_doc_py.py

  Check Last Updated:
    ./make_doc_py.py --check-dates

Process:
  1. Scans current directory for *.py files
  2. For each Python file:
     - Extracts the docstring between first set of triple quotes
     - Extracts usage information
     - Converts to markdown format OR checks for Last Updated
  3. Either:
     - Creates script list and usage index in doc_py.md
     - OR prints list of files missing Last Updated field

Output:
  - doc_py.md: Combined markdown documentation with script list and usage index
  - OR console output listing files missing Last Updated field

Arguments:
  --check-dates    Check all Python files for Last Updated field

Author: Assistant
Last Updated: 2024
=============================================================================


# make_doc_shell-copy.py

=============================================================================
make_doc_sh.py - Shell Script Documentation Collector
=============================================================================

Description:
  This script scans the current directory for shell script files (*.sh), extracts
  their documentation comments, and compiles them into a single markdown file
  with an index of script usages at the top.

Usage:
  ./make_doc_sh.py

Process:
  1. Scans current directory for *.sh files
  2. For each shell script file:
     - Extracts the comment block at the top of the file
     - Extracts usage information
     - Converts to markdown format
  3. Creates script list and usage index
  4. Combines all sections into doc_sh.md

Output:
  - doc_sh.md: Combined markdown documentation with script list and usage index

Author: Assistant
Last Updated: 2024
=============================================================================


# make_doc_shell.py

=============================================================================
make_doc_shell.py - Shell Script Documentation Collector
=============================================================================

Description:
  This script provides two main functions:
  1. Processes shell script files and converts their documentation to markdown
  2. Checks shell scripts for 'Last Updated' field in their comments

Usage:
  Process files:
    ./make_doc_shell.py
    ./make_doc_shell.py --modified-only

  Check Last Updated:
    ./make_doc_shell.py --check-dates

Process:
  1. Scans current directory for *.sh files
  2. For each shell script:
     - Extracts the comment block between first set of block comments
     - Extracts usage information
     - Converts to markdown format OR checks for Last Updated
  3. Either:
     - Creates script list and usage index in doc_shell.md
     - OR prints list of files missing Last Updated field

Output:
  - doc_shell.md: Combined markdown documentation with script list and usage index
  - OR console output listing files missing Last Updated field

Arguments:
  --check-dates    Check all shell scripts for Last Updated field
  --modified-only  Only process files with MODIFIED tag in documentation

Dependencies:
  - Python 3.x
  - funcs_lib
  - colorama

Author: Assistant
Last Updated: 2024-03-21
MODIFIED
=============================================================================


# makeallmd.py

=============================================================================
makeallmd.py - I Ching Book Markdown Generator
=============================================================================

Description:
  This script generates a formatted markdown document for the I Ching book by
  combining JSON data, generated descriptions, and images into a cohesive
  document structure.

Usage:
  python makeallmd.py [--content {all,pages}] [--test]

Arguments:
  --content: Choose content to include
    all: Include introduction and hexagram pages (default)
    pages: Include only hexagram pages
  --test: Use test set of hexagrams instead of full set
    When active, uses test_HEXAGRAMS = ['01']
    When inactive, uses all 64 hexagrams

Process:
  1. Processes hexagrams defined in HEXAGRAMS list
     (or test_HEXAGRAMS if --test is active)
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
  4. Adds table of contents navigation element

Dependencies:
  - Required Python packages:
    - colorama: Terminal output formatting
    - pyyaml: YAML frontmatter handling
    - json: JSON data parsing
    - re: Regular expression text processing
    - argparse: Command line argument parsing

File Structure:
  Input:
    - /BOOK_INTRO.md: Introduction text
    - /*.json: Hexagram data files (XX.json where XX is hexagram number)
    - /*_img.txt: Cached image descriptions
    - /*_hex.txt: Cached hexagram descriptions
    - /export.yaml: Document metadata and configuration
  Output:
    - includes/iching.md: Complete markdown document with TOC

TOC Structure:
  - Adds navigation element at start of document:
    <nav role="doc-toc">
      <h1>Table of Contents</h1>
    </nav>
  - Required for Prince PDF generation
  - Must be properly formatted for CSS styling

Environment:
  - ROOT: Base directory containing required input files

Example:
  # Generate full book with all hexagrams
  python makeallmd.py --content all

  # Generate only hexagram pages with test set
  python makeallmd.py --content pages --test

Author: JW
Last Updated: 2024
=============================================================================


# print_fields.py

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


# print_json_paths.py

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


# regen_TOC.py

=============================================================================
regen_TOC.py - Table of Contents Generator for I Ching Book
=============================================================================

Description:
    Generates a formatted HTML table of contents for the I Ching book by:
    1. Extracting page numbers from PDF where hexagram images appear
    2. Reading hexagram titles and codes from JSON files
    3. Creating a three-column HTML layout with dotted leaders

Usage:
    ./regen_TOC.py

Input Files:
    - ../includes/iching.pdf : Source PDF file
    - ../regen/*.json : Hexagram JSON files containing titles and codes

Output:
    - ../includes/TOC.html : Generated table of contents in HTML format

Format:
    Three-column layout with:
    - Hexagram number (01-64)
    - Unicode hexagram symbol
    - Hexagram name
    - Dotted leader
    - Page number

Functions:
    extract_page_numbers(pdf_path)
        - Extracts page numbers from PDF pages containing hexagram images

    get_hexagram_titles(directory)
        - Reads hexagram data from JSON files

    create_toc_html(titles, pages)
        - Generates formatted HTML with three-column layout

    generate_toc(titles, pages, output_file)
        - Main function to create and save TOC file

Dependencies:
    - PyMuPDF (fitz)
    - json
    - glob
    - os
    - re

Author: JW
Last Updated: 2024
=============================================================================


# regen_lines_in_context.py

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


# regen_lines_in_history.py

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


# regen_lines_in_trans.py

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


# regen_pairings.py

=============================================================================
regen_pairings.py - I Ching Pair-Path Analysis Generator
=============================================================================

Description:
    This script analyzes pairs of I Ching hexagrams that are inversions of
    each other, representing ascending and descending aspects of a pair-path.
    It processes hexagram data and uses AI to generate pair-path analysis.

Usage:
    ./regen_pairings.py <hex1> <hex2> <pair_number>
    Example: ./regen_pairings.py 1 2 1

Process:
    1. Loads data for both hexagrams from JSON files
    2. Analyzes their relationship as a pair-path
    3. Generates analysis using AI:
       - Title for the pair-path
       - Description of relationship
       - Image prompt for visualization
    4. Updates both hexagram JSON files with pair-path data
    5. Determines path stability (dynamic/stable)
    6. Assigns pair-path number (1-32)

Arguments:
    hex1: First hexagram number (1-64)
    hex2: Second hexagram number (1-64)
    pair_number: Pair-path number (1-32)
    --save: Save changes back to JSON files

Output:
    - Updates to hexagram JSON files with pair-path analysis
    - Console output of generated analysis
    - Status messages for process steps

Pair-Path Features:
    - Identifies ascending/descending relationships
    - Generates meaningful titles
    - Creates descriptive analysis
    - Provides image generation prompts
    - Determines path stability
    - Assigns canonical path numbers

Dependencies:
    - Python 3.x
    - openai
    - json
    - colorama

Author: Assistant
Last Updated: 2024-03-21
=============================================================================


# regen_story.py

=============================================================================
regen_story.py - I Ching Story Generator
=============================================================================

Description:
  This script generates new stories for I Ching hexagrams using OpenAI's GPT API.
  It takes a JSON file containing story data and an entry index as input, then
  updates the specified story with new AI-generated content.

Usage:
  ./regen_story.py --filename <input_json_file> --index <entry_index>
  ./regen_story.py -f <input_json_file> -i <entry_index>

Arguments:
  -f, --filename : Path to JSON file containing stories data
  -i, --index    : Integer specifying which story entry to update (0-based index)
  -s, --save     : Save the modified data back to the input file

Example:
  ./regen_story.py --filename ../regen/01.json --index 0
  ./regen_story.py -f ../regen/01.json -i 0

Environment Variables:
  OPENAI_API_KEY: Required OpenAI API key for making requests

Process:
  1. Reads and validates input JSON file against schema
  2. Makes API request to OpenAI for new story content
  3. Updates specified story entry with new content:
     - title
     - theme
     - short_story
     - lines_in_context (name, meaning, changing for each line)
  4. Prints updated story and returns modified data structure

Dependencies:
  - OpenAI Python package
  - jsonschema
  - colorama
  - regen_story_lib.py (local library)

Output:
  - Prints formatted story to stdout
  - Returns updated stories data structure
  - Prints complete JSON output in red

Author: Assistant
Last Updated: 2024
=============================================================================


# regen_story_lib.py

=============================================================================
regen_story_lib.py - Story Generation Library for I Ching
=============================================================================

Description:
  This library provides functions and schemas for generating stories based on
  I Ching hexagrams. It defines the structure for story generation prompts
  and responses, ensuring consistent story formats that align with hexagram
  interpretations.

Usage:
  Import and use in other scripts:
    from regen_story_lib import make_prompt, stories_schema

  Example:
    prompt = make_prompt(hexagram_number=1, story_idx=0)

Core Components:
  1. Story Types:
     - Man vs. Man
     - Man vs. Nature
     - Man vs. Self

  2. Schema Structure:
     - Title
     - Theme
     - Short Story (~200 words)
     - Lines in Context (6 lines with interpretations)

  3. Line Interpretations:
     - Name: Central concept
     - Meaning: Significance in story
     - Changing: Effect when line changes

Functions:
  make_prompt(hexagram_number, story_idx)
    Generates a complete prompt for story generation using:
    - I Ching primer
    - Tholonic primer
    - Hexagram-specific content
    - Story structure guidelines

Schema Validation:
  - Enforces story length limits
  - Validates line interpretations
  - Ensures complete hexagram coverage
  - Maintains consistent structure

Dependencies:
  - json
  - os
  - sys

Author: Assistant
Last Updated: 2024-03-21
=============================================================================


# regen_titles.py

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


# regen_tri_gen_phrase.py

=============================================================================
regen_trigrams_phrase_general.py - I Ching Trigram Phrase Generator
=============================================================================

Description:
  This script generates a general trigram phrase for an I Ching hexagram by
  combining multiple philosophical perspectives (Jungian, Platonic, Taoist,
  Tholonic, and Thermodynamic) into a single comprehensive description.
  It processes a single JSON file containing hexagram data and can either
  display or save the generated phrase.

Usage:
  ./regen_trigrams_phrase_general.py <filename> [--save]
  Example: ./regen_trigrams_phrase_general.py 01.json --save

Arguments:
  filename: JSON file to process (e.g., 01.json)
  --save: Optional flag to save updates to the JSON file

Process:
  1. Loads specified hexagram JSON file
  2. Extracts existing trigram phrases from different perspectives
  3. Uses OpenAI API to generate a combined general phrase
  4. Either displays the result or saves it back to the file
  5. Updates JSON with new 'general' field under 'trigram_phrase'

Dependencies:
  - Python 3.x
  - Required packages: openai, colorama
  - OpenAI API key in environment

File Structure:
  Input JSON format:
    {
      "trigram_phrase": {
        "Jungian": "...",
        "Platonic": "...",
        "Taoist": "...",
        "Tholonic": "...",
        "Thermodynamics": "..."
      }
    }

Environment:
  OPENAI_API_KEY: OpenAI API authentication key

Error Handling:
  - Validates file existence
  - Ensures valid JSON formatting
  - Handles API errors gracefully
  - Reports errors in color-coded output

Author: JW
Last Updated: 2024
=============================================================================


# regen_trigram_phrase.py

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


# reorg.py

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


# version_utils.py

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
