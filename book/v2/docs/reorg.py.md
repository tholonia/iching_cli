# reorg.py

## I Ching PDF Page Reorganizer

### Description
This script processes a PDF file containing I Ching hexagram entries and adds blank pages before each hexagram to ensure proper double-sided printing layout. It's specifically designed for book printing where hexagrams should start on right-hand (odd-numbered) pages.

### Usage
```bash
reorg.py [-h] input_pdf output_pdf
```

### Arguments
- `input_pdf`: Path to input PDF file
- `output_pdf`: Path to output PDF file

### Process
1. Detects hexagram entries by:
   - Unicode hexagram symbols (U+4DC0 to U+4DFF)
   - Large font titles in format "1 ䷀ 63 - Creation"
2. Inserts blank pages before hexagrams for proper layout
3. Preserves first 3 pages (table of contents)
4. Only checks odd-numbered pages for hexagrams
5. Processes PDF iteratively to handle large files
6. Maintains PDF dimensions and properties

### Input Format
- PDF file with I Ching hexagram entries
- Each hexagram entry starts with titled hexagram symbol
- First 3 pages contain table of contents

### Output Format
- Modified PDF with blank pages inserted
- Hexagrams start on right-hand pages
- Original content unchanged except for page positioning

### Dependencies
- PyMuPDF (fitz) for PDF content analysis
- pdfrw for PDF manipulation

### Example
```bash
reorg.py docs/clean_iching.pdf docs/reorg.pdf
```

*Last Updated:* 01-01-2024 00:00

---

