# get_new_image_desc_OPENAI.py

## I Ching Hexagram Image Description Generator

### Description
This script generates AI-powered descriptions of I Ching hexagram images using OpenAI's GPT-4 Vision API. For each hexagram image, it generates a narrative paragraph explaining why specific visual elements and styles were chosen to represent that hexagram.

### Usage
```bash
python get_new_image_desc_OPENAI.py [-s] <hexagram_number>
```

### Arguments
- `hexagram_number`: Number of the hexagram (1-64)
- `-s, --save`: Save the output to a text file

### Examples
- `python get_new_image_desc_OPENAI.py 20`  
  Display output only
- `python get_new_image_desc_OPENAI.py -s 20`  
  Display and save output

### Process
1. Reads hexagram image and context files
2. Converts image to base64 for API submission
3. Sends image and context to OpenAI's Vision API
4. Generates a formatted description paragraph
5. Optionally saves output to text file

### Dependencies
- OpenAI Python package (v1.0.0 or later)
- Valid OpenAI API key set in OPENAI_API_KEY environment variable
- Access to GPT-4 Vision model in your OpenAI account
- Required Python packages: `openai`, `colorama`

### File Structure
- Input: `/book/tholonic_primer.md`
- Input: `/book/v2/<hexagram_number>.json`
- Input: `/book/v2/<hexagram_number>.png`
- Output: `/book/v2/<hexagram_number>_img.txt` (when using --save)

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)

### Note
Vision API calls may have higher costs than standard GPT-4 calls. Ensure proper rate limiting and cost monitoring when using this script.

*Last Updated:* 10-16-2023 14:30

---

