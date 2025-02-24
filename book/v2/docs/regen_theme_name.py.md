# regen_theme_name.py

## Story Theme Author Extractor

### Description
Extracts author names from story themes in I Ching JSON files using NLP Named Entity Recognition and pattern matching. Handles various formats like:
- "Style of {Author}"
- "In the style of {Author}"
- "Inspired by {Author}"
- "{Author}'s Style"
- "{Author} Style"
etc.

### Usage
```bash
./regen_theme_name.py [--save]
```

### Arguments
- `--save`: Update the files with extracted author names instead of printing.

### Dependencies
- `spacy` (with `en_core_web_sm` model)
- `colorama`

### Setup
```bash
pip install spacy colorama
python -m spacy download en_core_web_sm
```

### Output
- Without `--save`: Prints filename and transformations in color
  - Filename in green
  - Original theme in yellow
  - Extracted name in cyan
- With `--save`: Updates files with extracted names

*Last Updated:* 03-20-2024 09:00

---

