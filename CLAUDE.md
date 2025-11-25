# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository contains two main projects:
1. **I Ching CLI** - A command-line I Ching divination tool using the traditional yarrow stick method
2. **I Ching Book** - An AI-enhanced reinterpretation and publication system for the I Ching

## I Ching CLI Application

### Core Files
- `throw.py` - Main CLI application for I Ching readings
- `update.py` - Database management utilities
- `hexagrams.db` / `hexagrams.sqlite` - SQLite database containing hexagram data
- `trigrams.db` / `trigrams.sqlite` - SQLite database containing trigram data

### Common Commands

#### Basic I Ching Readings
```bash
# Ask a question using pseudo-random numbers (fast)
./throw.py --question "Should I?"

# Ask a question using true random data from RANDOM.ORG (slow but more authentic)
./throw.py --question "Should I?" --true_random

# View a specific hexagram by binary value (0-63)
./throw.py --binary 0

# View a specific hexagram by classic I Ching order (1-64, not yet implemented)
./throw.py --classic 1
```

#### Database Management
```bash
# Create dump backups of databases
./update.py --dump

# Reload database from specific backup
./update.py --reload hexagrams_08_12_2024.sql

# Add comment to specific binary ID
./update.py --bin 0 --comment "your comment here"
```

### Dependencies
- Python 3.10+ (tested on 3.10.14)
- `colorama` - Terminal color output
- `sqlite3` - Database operations
- `requests` - For RANDOM.ORG API calls

### Installation
```bash
pip install colorama sqlite3
chmod 755 *.py  # On Linux
```

## I Ching Book Project

Located in `book/v2/` directory - this is a comprehensive book generation system that creates AI-enhanced interpretations of the I Ching.

### Key Directories
- `book/v2/bin/` - Python scripts and shell utilities for book generation
- `book/v2/includes/` - CSS, HTML templates, and PDF components
- `book/v2/regen/` - Active JSON files being processed
- `book/v2/ok<n>/` - Archived versions of completed JSON files
- `book/v2/prod/` - Production files (images, descriptions)

### Publishing Workflow

#### Environment Setup
```bash
conda activate cbot  # Environment with requirements.txt installed
cd /home/jw/src/iching_cli/book/v2/bin
export OPENAI_API_KEY=sk-proj-...
export D=/home/jw/store/src/iching_cli/book/v2/bin
```

#### Book Generation Process
```bash
# 1. Prepare markdown file and launch Typora
./prep.sh

# 2. Export to HTML within Typora (manual step)

# 3. Create final PDF
./post.sh PDF      # For PDF reading format
./post.sh BOOK     # For book publishing format
./post.sh PDF --minimal  # Minimal version with main content only
```

### Content Generation Scripts

#### Story and Content Regeneration
```bash
# Regenerate specific story by index (0, 1, or 2)
./regen_story.py --filename ../regen/03.json --index 0 --provider openai --save

# Regenerate history content
./regen_history.py --filename ../regen/03.json --provider openai --save

# Clean up theme names (remove AI verbosity)
./regen_theme_name.py --filename ../regen/03.json
```

#### Batch Processing
```bash
# Process all hexagrams for story regeneration
./regen_story_BATCH.sh

# Process all hexagrams for history regeneration  
./regen_history_BATCH.sh

# Generate pair images for all hexagrams
./gen_pair_images.py
```

### Dependencies (Book Project)
See `book/v2/requirements.txt`:
- `colorama` - Terminal colors
- `fitz` / `PyMuPDF` - PDF manipulation
- `jsonschema` - JSON validation
- `openai` - OpenAI API integration
- `pyyaml` - YAML processing
- `typer` - CLI framework

### External Tools Required
- **pdftk** - PDF manipulation
- **prince-books** - HTML to PDF conversion with TOC support
- **lessc** - LESS CSS compilation
- **typora** - Markdown editor for manual HTML export
- **okular** - PDF viewer

### File Management

#### JSON Structure
- JSON files contain hexagram data with stories, history, and line interpretations
- Active development files are in `../regen/` folder
- Completed versions archived in `../ok<n>/` folders (n is incremented)

#### Page Size Changes
When changing page dimensions, update these files:
- `blank.pdf` - Generated from HTML export in Typora
- `BOOK_INTRO.pdf` - Generated from HTML export
- `COPYRIGHT.pdf` - Generated from PSD files
- `COVER.pdf` - Generated from PSD files
- Chart PDFs - Convert from PSD to PNG, then PNG to PDF using ImageMagick

### Content Modification Examples

#### Bulk Text Replacements
```bash
# Remove traditional Chinese names from trigrams
perl -pi -e 's/\(Kan\/Water\)/\(Water\)/gmi' ../regen/*
perl -pi -e 's/\(Qian\/Heaven\)/\(Heaven\)/gmi' ../regen/*

# Add JSON fields
perl -pi -e 's/"hexagram_code/"notes":"",\n  "hexagram_code/gmi' ../regen/*.json
```

## Architecture Overview

### CLI Application Architecture
- Uses original yarrow stick algorithm (ported from JavaScript)
- Supports both pseudo-random and true random number generation
- SQLite databases store traditional Wilhelm-Baynes interpretations
- ANSI terminal output with markdown file generation
- Question text determines output filename

### Book Generation Architecture
- **Content Layer**: JSON files containing hexagram interpretations
- **Generation Layer**: Python scripts for AI-enhanced content creation
- **Styling Layer**: LESS/CSS for print and digital formats
- **Assembly Layer**: Shell scripts orchestrating the build process
- **Output Layer**: PDF generation with Prince and pdftk

### Data Flow
1. Raw hexagram data stored in JSON format
2. AI providers (OpenAI, Perplexity, etc.) enhance interpretations
3. Python scripts compile content into markdown
4. LESS stylesheets compiled to CSS
5. Typora exports markdown to HTML
6. Prince converts HTML to PDF with proper pagination
7. pdftk merges components into final publication

## Development Notes

- Python 3.10.14 recommended for CLI application
- The book project uses conda environment with specific dependencies
- True random numbers from RANDOM.ORG provide more authentic readings
- JSON files follow a specific schema for consistency
- The publishing process requires manual HTML export step in Typora
- Page size changes require regenerating multiple PDF components