#!/bin/bash

# =============================================================================
# get_new_image_desc_OPENAI_BATCH.sh - I Ching Image Description Generator
# =============================================================================
#
# Description:
#   This script automates the generation of image descriptions by iterating
#   through all 64 hexagrams using OpenAI's API. For each hexagram, it calls
#   get_new_image_desc_OPENAI.py to generate and save image descriptions.
#
# Usage:
#   ./get_new_image_desc_OPENAI_BATCH.sh
#
# Process:
#   1. Loops through numbers 1-64
#   2. For each number, formats it with leading zeros (01, 02, etc.)
#   3. Calls get_new_image_desc_OPENAI.py with the formatted number
#   4. Automatically saves results (--save flag)
#
# Dependencies:
#   - get_new_image_desc_OPENAI.py script in same directory
#   - Python environment with required packages
#   - Valid OpenAI API key in environment
#   - Access to GPT-4 Vision model in your OpenAI account
#
# Note:
#   This is a batch processing script that will process all hexagram images
#   sequentially. Be aware of OpenAI API rate limits and costs when
#   running this script, especially for vision API calls.
#
# Author: JW
# Last Updated: 2024
# =============================================================================

# Loop from 01 to 64
for i in $(seq -f "%02g" 01 64); do
    # Execute the command with the current number
    ./get_new_image_desc_OPENAI.py "$i" --save
done
