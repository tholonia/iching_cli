#!/bin/env python

"""
I Ching Image Corner Rounding Script

This script processes a set of I Ching hexagram images by applying rounded corners
using ImageMagick. It's a Python implementation of the ROUND_ALL_CORNERS bash script
with improved error handling and progress reporting.

Process:
1. Takes a parameter set directory name as input
2. Creates a temporary output directory
3. Processes all PNG files in the input directory
4. Applies 50-pixel radius rounded corners to each image
5. Saves processed images in the tmp/ subdirectory

Usage:
    python round_all_corners.py <pset>

Arguments:
    pset    Parameter set directory name (e.g., 's99')
            Images should be in /home/jw/src/iching_cli/defs/final/<pset>/

Required:
    - ImageMagick must be installed
    - Input images must be PNG format
    - Write permissions for creating tmp/ subdirectory

Example:
    python round_all_corners.py s99

Output:
    Processed images saved to /home/jw/src/iching_cli/defs/final/<pset>/tmp/
"""

import subprocess
import os
from pathlib import Path
from glob import glob
import argparse

def process_image(input_path: str, output_dir: str) -> None:
    """
    Process a single image using ImageMagick commands.

    Args:
        input_path (str): Full path to input image
        output_dir (str): Directory for output images
    """
    # Get just the filename from the input path
    filename = os.path.basename(input_path)
    output_path = os.path.join(output_dir, filename)

    # Construct ImageMagick command
    command = [
        'magick',
        input_path,
        '(',
            '+clone',
            '-alpha', 'extract',
            '-draw', 'fill black polygon 0,0 0,50 50,0 fill white circle 50,50 50,0',
            '(',
                '+clone',
                '-flip',
            ')',
            '-compose', 'Multiply',
            '-composite',
            '(',
                '+clone',
                '-flop',
            ')',
            '-compose', 'Multiply',
            '-composite',
        ')',
        '-alpha', 'off',
        '-compose', 'CopyOpacity',
        '-composite',
        output_path
    ]

    try:
        # Execute the command
        subprocess.run(command, check=True)
        print(f"Processed image: {filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing image {filename}: {e}")
    except Exception as e:
        print(f"Unexpected error processing image {filename}: {e}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process PNG files in a specified directory.')
    parser.add_argument('pset', help='The parameter set directory name')
    args = parser.parse_args()

    # Define directories using the command line argument
    input_dir = f"/home/jw/src/iching_cli/defs/final/{args.pset}"
    output_dir = os.path.join(input_dir, "tmp")

    # Verify input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Directory not found: {input_dir}")
        return

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Get list of all PNG files in input directory
    png_files = glob(os.path.join(input_dir, "*.png"))

    if not png_files:
        print(f"No PNG files found in {input_dir}")
        return

    print(f"Found {len(png_files)} PNG files to process")

    # Process each PNG file
    for png_file in sorted(png_files):
        process_image(png_file, output_dir)

    print("Processing complete!")

if __name__ == "__main__":
    main()