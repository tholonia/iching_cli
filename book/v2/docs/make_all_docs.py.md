# makeallmd.py

## I Ching Book Markdown Generator

### Description
This script generates a formatted markdown document for the I Ching book by combining JSON data, generated descriptions, and images into a cohesive document structure.

### Usage
```bash
python makeallmd.py [--content {all,pages}] [--test]
```

### Arguments
- **--content**: Choose content to include
  - **all**: Include introduction and hexagram pages (default)
  - **pages**: Include only hexagram pages
- **--test**: Use test set of hexagrams instead of full set
  - When active, uses `test_HEXAGRAMS = ['01']`
  - When inactive, uses all 64 hexagrams

### Process
1. Processes hexagrams defined in `HEXAGRAMS` list (or `test_HEXAGRAMS` if `--test` is active)
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

### Dependencies
- Required Python packages:
  - `colorama`: Terminal output formatting
  - `pyyaml`: YAML frontmatter handling
  - `json`: JSON data parsing
  - `re`: Regular expression text processing
  - `argparse`: Command line argument parsing

### File Structure
- **Input**:
  - `/BOOK_INTRO.md`: Introduction text
  - `/*.json`: Hexagram data files (XX.json where XX is hexagram number)
  - `/*_img.txt`: Cached image descriptions
  - `/*_hex.txt`: Cached hexagram descriptions
  - `/export.yaml`: Document metadata and configuration
- **Output**:
  - `includes/iching.md`: Complete markdown document with TOC

### TOC Structure
- Adds navigation element at start of document:
  ```html
  <nav role="doc-toc">
    <h1>Table of Contents</h1>
  </nav>
  ```
- Required for Prince PDF generation
- Must be properly formatted for CSS styling

### Environment
- **ROOT**: Base directory containing required input files

### Example
```bash
# Generate full book with all hexagrams
python makeallmd.py --content all

# Generate only hexagram pages with test set
python makeallmd.py --content pages --test
```

*Last Updated:* 10-29-2023 15:04

---

