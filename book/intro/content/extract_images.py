#!/usr/bin/env python3
import re
import sys

def extract_image_urls(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match both Markdown and HTML image formats
    md_pattern = r'!\[.*?\]\((.*?)\)'
    html_pattern = r'<img[^>]*src=["\']([^"\']+)["\']'

    # Combine all found URLs in discovery order
    md_matches = list(re.finditer(md_pattern, content))
    html_matches = list(re.finditer(html_pattern, content))

    # Combine and sort by original position in file
    all_matches = md_matches + html_matches
    all_matches.sort(key=lambda m: m.start())

    for match in all_matches:
        print(match.group(1))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_images.py your_markdown_file.md")
        sys.exit(1)
    extract_image_urls(sys.argv[1])
