#!/bin/env python

import os
import hashlib
from pathlib import Path
from typing import List, Tuple

def get_png_hashes(directory: str) -> List[Tuple[str, str]]:
    """
    Find all PNG files in the specified directory and calculate their MD5 hashes.

    Args:
        directory (str): Path to the directory to search

    Returns:
        List[Tuple[str, str]]: List of tuples containing (file_path, md5_hash)
    """
    results = []

    # Convert to Path object for easier handling
    dir_path = Path(directory)

    # Verify directory exists
    if not dir_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Find all PNG files and filter out those starting with 'X'
    for png_file in dir_path.glob("**/[0123456789]*.png"):
        if not png_file.name.startswith('X'):  # Add this condition
            # Calculate MD5 hash
            md5_hash = hashlib.md5()

            # Read file in chunks to handle large files efficiently
            with open(png_file, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    md5_hash.update(chunk)

            # Store results as (file_path, hash)
            results.append((
                str(png_file),
                md5_hash.hexdigest()
            ))

    return results
def main():
    import json
    directory = "/home/jw/src/iching_cli/defs/final"

    try:
        # Get hashes for all PNG files
        png_hashes = get_png_hashes(directory)
        json.dump(png_hashes, open("png_hashes.json", "w"), indent=4)

        # Create a dictionary to store hash -> filenames mapping
        hash_to_files = {}
        for file_path, md5_hash in png_hashes:
            if md5_hash not in hash_to_files:
                hash_to_files[md5_hash] = []
            hash_to_files[md5_hash].append(file_path)

        # Find and print duplicates
        print("Duplicate files found:")
        for md5_hash, files in hash_to_files.items():
            if len(files) > 1:
                if 'X' in files[0]:
                    target = os.path.abspath(files[0]).replace('png', 'txt')
                    source = os.path.abspath(files[1]).replace('png', 'txt')
                    cmd = f"cp {source} {target}"
                    print(cmd)
                    # os.system(cmd)
                if 'X' in files[1]:
                    target = os.path.abspath(files[1]).replace('png', 'txt')
                    source = os.path.abspath(files[0]).replace('png', 'txt')
                    cmd = f"cp {source} {target}"
                    print(cmd)
                    # os.system(cmd)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()