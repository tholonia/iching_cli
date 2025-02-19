# regen_TOC.py

## Table of Contents Generator for I Ching Book

### Description
Generates a formatted HTML table of contents for the I Ching book by:
1. Extracting page numbers from PDF where hexagram images appear
2. Reading hexagram titles and codes from JSON files
3. Creating a three-column HTML layout with dotted leaders

### Usage
```bash
./regen_TOC.py
```

### Input Files
- `../includes/iching.pdf`: Source PDF file
- `../regen/*.json`: Hexagram JSON files containing titles and codes

### Output
- `../includes/TOC.html`: Generated table of contents in HTML format

### Format
Three-column layout with:
- Hexagram number (01-64)
- Unicode hexagram symbol
- Hexagram name
- Dotted leader
- Page number

### Functions
- `extract_page_numbers(pdf_path)`: Extracts page numbers from PDF pages containing hexagram images
- `get_hexagram_titles(directory)`: Reads hexagram data from JSON files
- `create_toc_html(titles, pages)`: Generates formatted HTML with three-column layout
- `generate_toc(titles, pages, output_file)`: Main function to create and save TOC file

### Dependencies
- PyMuPDF (fitz)
- json
- glob
- os
- re

*Last Updated:* 10-01-2024 12:34

---

