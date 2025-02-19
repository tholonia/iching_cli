# get_new_hex_desc_OPENAI.py

## I Ching Hexagram Description Generator

### Description
This script generates descriptive paragraphs for I Ching hexagrams using OpenAI's GPT-4 API. For each hexagram, it generates two narrative paragraphs:
1. A general description of the hexagram's archetypal meaning
2. A description relating to tholonic concepts specific to the hexagram

### Usage
```bash
python get_new_hex_desc_OPENAI.py [-s] <hexagram_number>
```

### Arguments
- `hexagram_number`: Number of the hexagram (1-64)
- `-s`, `--save`: Save the output to a text file

### Examples
```bash
python get_new_hex_desc_OPENAI.py 20         # Display output only
python get_new_hex_desc_OPENAI.py -s 20      # Display and save output
```

### Process
1. Reads context from local files (tholonic_primer.md and hexagram JSON)
2. Sends context to OpenAI's GPT-4 API for processing
3. Generates two formatted paragraphs
4. Optionally saves output to text file

### Dependencies
- OpenAI Python package (v1.0.0 or later)
- Valid OpenAI API key set in OPENAI_API_KEY environment variable
- Access to GPT-4 model in your OpenAI account
- Required Python packages: openai, colorama

### File Structure
- Input: `/book/tholonic_primer.md`
- Input: `/book/v2/<hexagram_number>.json`
- Output: `/book/v2/<hexagram_number>_hex.txt` (when using --save)

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

*Last Updated:* 01-01-2024 00:00

---

