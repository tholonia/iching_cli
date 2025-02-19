# get_new_hex_desc_LOCAL.py

## I Ching Hexagram Description Generator

### Description
This script generates descriptive paragraphs for I Ching hexagrams using AI. For each hexagram, it generates two narrative paragraphs:
1. A general description of the hexagram's archetypal meaning
2. A description relating to tholonic concepts specific to the hexagram

### Usage
```bash
python get_new_hex_desc_LOCAL.py [-s] <hexagram_number>
```

### Arguments
- `hexagram_number`: Number of the hexagram (1-64)
- `-s, --save`: Save the output to a text file

### Examples
```bash
python get_new_hex_desc_LOCAL.py 20         # Display output only
python get_new_hex_desc_LOCAL.py -s 20      # Display and save output
```

### Process
1. Reads context from local files (`tholonic_primer.md` and hexagram JSON)
2. Sends context to local AI server for processing
3. Generates two formatted paragraphs
4. Optionally saves output to text file

### Dependencies
- OpenAI API key (can be any string when using local server)
- Local AI server running on `http://127.0.0.1:1234/v1`
- Required Python packages: `openai`, `colorama`

### File Structure
- Input: `/book/tholonic_primer.md`
- Input: `/book/v2/<hexagram_number>.json`
- Output: `/book/v2/<hexagram_number>_hex.txt` (when using `--save`)

*Author: JW*

*Last Updated:* 12-15-2024 14:30

---

