#!/bin/env python

"""
I Ching Book Generator

This script generates a formatted markdown document for the I Ching book by combining:
- Introduction text
- Hexagram data from JSON files
- Generated literary descriptions
- Images and their descriptions

Features:
1. Processes hexagrams defined in HEXAGRAMS list (configurable subset of 01-64)
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
4. Caches generated descriptions to avoid redundant API calls

Input Files:
- /BOOK_INTRO.md: Introduction text
- /*.json: Hexagram data files (XX.json where XX is hexagram number)
- /*_img.txt: Cached image descriptions
- /*_hex.txt: Cached hexagram descriptions
- /export.yaml: Document metadata and configuration

Output:
- docs/iching.md: Complete markdown document ready for PDF conversion

Dependencies:
- colorama: Terminal output formatting
- openai: GPT-4 API for literary descriptions
- pyyaml: YAML frontmatter handling
- json: JSON data parsing
- re: Regular expression text processing

Environment:
- Requires OPENAI_API_KEY environment variable
- Expects ROOT directory with required input files
"""

# Predefined list of all hexagrams
HEXAGRAMS = ['01', '02','03']


HEXAGRAMS = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
    '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
    '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
    '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
    '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
    '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
    '61', '62', '63', '64'
]

ROOT="/home/jw/store/src/iching_cli/book/v2"

import json
import sys
import argparse
import glob
import os
from colorama import Fore, Style
import openai
import re
import yaml
from openai import OpenAI

def ensure_directory_exists(tdir):
    """Create the description directory if it doesn't exist"""
    if not os.path.exists(tdir):
        try:
            os.makedirs(tdir, exist_ok=True)
            print(f"Created directory: {tdir}")
        except Exception as e:
            print(f"Error creating directory {tdir}: {e}")
            return False
    return True

def rewrite_literary_style(text, hexagram_id):
    # Try reading from cache first
    try:
        with open(f"{ROOT}/{hexagram_id}_img.txt", 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError):
        # If file doesn't exist or can't be read, call OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "You are a literary writer and a master of the I Ching and the Tholonic Model. Rewrite the given text in an elegant, flowing style while preserving all key information."
                },
                {
                    "role": "user",
                    "content": text
                }],
                max_tokens=2000,  # Adjust this value as needed
                temperature=0.7   # You can also adjust temperature if desired
            )
            result = response.choices[0].message.content

            cfile = f"{ROOT}/{hexagram_id}_img.txt"
            # print(cfile)
            # Cache the result
            with open(cfile, 'w', encoding='utf-8') as f:
                f.write(result)

            return result
        except Exception as e:
            print(f"OpenAI API error: {e}")
            input("Paused on ERROR OpenAI API error")
            return text

def get_image_blurb(sfnum):
    try:
        with open(f'{ROOT}/{sfnum}_img.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {ROOT}/{sfnum}.txt: {e}")
        input(f"Paused on ERROR reading file {ROOT}/{sfnum}_img.txt")
        return None

def get_hex_blurb(sfnum):
    """
    Read the hexagram description from a text file and return as array of paragraphs.

    Args:
        sfnum (str): Hexagram number (e.g., '01')

    Returns:
        list: Array of paragraphs from the file, or None if file not found
    """
    try:
        with open(f'{ROOT}/{sfnum}_hex.txt', 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Split on double newlines to separate paragraphs
            # and filter out empty strings
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            if not paragraphs:
                print(Fore.RED + f"Warning: No paragraphs found in {ROOT}/{sfnum}_hex.txt" + Style.RESET_ALL)
                input(f"Paused on WARNING: Empty file {ROOT}/{sfnum}_hex.txt")
                return None
            return paragraphs
    except Exception as e:
        print(Fore.RED + f"Error reading file {ROOT}/{sfnum}_hex.txt: {e}" + Style.RESET_ALL)
        input(f"Paused on ERROR reading file {ROOT}/{sfnum}_hex.txt")
        return None

def format_core_section(core,sfnum):
    image_file = f"{ROOT}/{sfnum}.png"
    # Read the hexagram description
    hex_desc_ary = get_hex_blurb(sfnum)
#     if hex_desc_ary is None:
#         # Fallback to generating description if file not found
#         hex_desc_ary = f""" This hexagram contributes {core['order8child']} qualities to the tholon of {core['order8parent']}.  Its perspective is one of {core['perspective']} . Its nature is one  of  {core['nature']}, and its {core['action']} is that of Manifesting.  It achieves success through {core['success_through']}.  It' energy is {core['energy_cycle']} {core['yinyang_balance']}.  The challange to overcome is {core['challenge']}.
# """
#         hex_desc_ary = hex_desc_ary.replace(";",", ")
#         hex_desc_ary = hex_desc_ary.lower()
#         hex_desc_ary = rewrite_literary_style(hex_desc_ary,sfnum)

    image_blurb = get_image_blurb(sfnum)

    """Format the core hexagram section"""


#^██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
    # changed below from
    ### *{core['image']}; {image_blurb}*
    #

#! markdown version of title.  Below is the HTML version -->
# {core['king_wen_sequence']} {core['hexagram']} *{core['binary_sequence']}* - {core['name']}


    ostr = f"""
# &nbsp;
<div style="margin: 0 auto; text-align: center;border-bottom:1px solid #c5c5c5;padding-bottom:1em;">
<span style="font-size:2em;color:#666;text-align:center;font-weight:normal;padding-bottom:0.2em;font-family:'LinLibertine',serif;">{core['king_wen_sequence']} {core['hexagram']}</span><span style="font-size:1em;color:#666;text-align:center;font-weight:normal;padding-bottom:0.2em;font-family:'LinLibertine',serif;vertical-align:text-bottom;"> {core['binary_sequence']} </span><span style="font-size:2em;color:#666;text-align:center;font-weight:normal;padding-bottom:0.2em;font-family:'LinLibertine',serif;">&nbsp; {core['name']}</span>
</div>


## {core['description']}

<img src="{ROOT}/{core['image_file']}">
<span style="margin-bottom: 8px;"> &nbsp; </span>

### *{image_blurb}*

<p/>

#### {hex_desc_ary[0]}

#### {core['tholonic_analysis']['significance_in_thologram']} {hex_desc_ary[1]}

#### ***Lines in Transition***
<ul>
<li><B>Line 6</B>: {core['lines_in_transition']['6']}</li>
<li><B>Line 5</B>: {core['lines_in_transition']['5']}</li>
<li><B>Line 4</B>: {core['lines_in_transition']['4']}</li>
<li><B>Line 3</B>: {core['lines_in_transition']['3']}</li>
<li><B>Line 2</B>: {core['lines_in_transition']['2']}</li>
<li><B>Line 1</B>: {core['lines_in_transition']['1']}</li>
</ul>
#### **No Moving Lines**: {core['no_moving_lines']}
#### **All Moving Lines**: {core['all_moving_lines']}


###### Tholonic Analysis
#### **Negotiation**: {core['tholonic_analysis']['negotiation']}

#### **Limitation**: {core['tholonic_analysis']['limitation']}

#### **Contribution**: {core['tholonic_analysis']['contribution']}
"""
    return ostr

def format_stories_section(stories):
    """Format the three stories section"""
    result = f"\n\n###### {stories['title']}\n\n"

    for story in stories['stories']:
        udesc = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', story['description'])
        result += f"""
##### {story['title']}
### In the style of {story['style']}

#### {udesc}

#### ***Lines in Context:***
<ul>
<li><B>6</B>: {story['key_elements']['6']}</li>
<li><B>5</B>: {story['key_elements']['5']}</li>
<li><B>4</B>: {story['key_elements']['4']}</li>
<li><B>3</B>: {story['key_elements']['3']}</li>
<li><B>2</B>: {story['key_elements']['2']}</li>
<li><B>1</B>: {story['key_elements']['1']}</li>
</ul>
"""

    return result

def format_history_section(history,core):
    """Format the historical event section"""
    return f"""
###### '{core['name']}' in History

##### *{history['title']}*

#### {history['description']}

<div style="font-size: 8pt;font-style:italic">Source: {history['source']}</div>

#### ***Lines in Context:***

<ul>
<li><B>6</B>: {history['key_elements']['6']}</li>
<li><B>5</B>: {history['key_elements']['5']}</li>
<li><B>4</B>: {history['key_elements']['4']}</li>
<li><B>3</B>: {history['key_elements']['3']}</li>
<li><B>2</B>: {history['key_elements']['2']}</li>
<li><B>1</B>: {history['key_elements']['1']}</li>
</ul>
"""
#*██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

def format_intro_section(args):
    """Format the intro section"""
    if args.content == "all":
        with open(f"{ROOT}/docs/BOOK_INTRO.md", 'r', encoding='utf-8') as file:
            intro = file.read()

        # intro += "\n<div style=\"page-break-after: always;\"></div>\n"
        # intro += "\n<div style=\"page-break-before: right;\"></div>\n"
        intro += ""

    elif args.content == "pages":
        intro = ""
    return intro

def get_yaml():
    yaml_path = f"{ROOT}/../export.yaml"
    if not os.path.exists(yaml_path):
        return ""

    with open(yaml_path, 'r', encoding='utf-8') as file:
        yaml_data = yaml.safe_load(file)

    # Generate YAML frontmatter string
    frontmatter = ["---"]
    for key, value in yaml_data.items():
        if isinstance(value, (list, dict)):
            frontmatter.append(f"{key}: {yaml.dump(value, default_flow_style=False)}")
        else:
            frontmatter.append(f"{key}: {value}")
    frontmatter.append("---\n")
    # Convert frontmatter list to string
    frontmatter_str = "\n".join(frontmatter)

    # Note: title_page and copyright_page variables are unused, so removed

    return frontmatter_str

def generate_markdown_from_json(json_data, sfnum):
    """Generate complete markdown using all JSON sections"""
    markdown = get_yaml()

    # Add core section
    core = json_data['hx']['core']
    markdown += format_core_section(core,sfnum)

    # Add stories section
    markdown += format_stories_section(json_data['hx']['stories'])

    # Add history section
    markdown += "\n\n" + format_history_section(json_data['hx']['history'],json_data['hx']['core'])

    markdown += f"""

###### *Notes*

### **King Wen Order**: {core['king_wen_title']} **Binary**: {core['binary_sequence']} **Above**: {core['above']} **Below**: {core['below']}


"""
    return markdown

def get_json_filenames():
    """
    Get names of all JSON files from the specified directory.

    Returns:
        list: List of JSON filenames (without full path)
    """
    json_files = glob.glob(os.path.join(ROOT, "*.json"))

    sfiles = sorted(os.path.basename(f) for f in json_files)

    for i in range(len(sfiles)):
        sfiles[i] = ROOT + "/" + sfiles[i]


    # print(sfiles)
    # exit()
    return sfiles

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Generate I Ching book markdown with optional intro section'
    )
    parser.add_argument(
        '--content',
        choices=['all', 'pages'],
        default='all',
        help='Include all content (with intro) or just hexagram pages'
    )
    args = parser.parse_args()


    return args

def get_json_version():
    """
    Read version string from VER_JSON.txt file.
    Returns empty string if file is empty or doesn't exist.
    """
    try:
        with open(f"{ROOT}/VER_JSON.txt", 'r', encoding='utf-8') as f:
            version = f.readline().strip()
            return version if version else ""
    except (FileNotFoundError, IOError):
        return ""

def main():
    # Parse command line arguments
    args = parse_args()

    # Get intro section if requested
    markdown_output = format_intro_section(args)

    for sfnum in HEXAGRAMS:
        filename = f"{ROOT}/{sfnum}{get_json_version()}.json"

        # Read the JSON file
        print(Fore.YELLOW + "Reading " + filename + Style.RESET_ALL)
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            print(Fore.RED + f"Error: File {filename} not found" + Style.RESET_ALL)
            continue
        except json.JSONDecodeError:
            print(Fore.RED + f"Error: Invalid JSON in {filename}" + Style.RESET_ALL)
            continue

        # Generate markdown
        markdown_output += "\n" + generate_markdown_from_json(json_data, sfnum)

    # Write output to file
    output_file = f"{ROOT}/includes/iching.md"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_output)
    print(f"Markdown has been saved to {output_file}")

if __name__ == "__main__":
    main()