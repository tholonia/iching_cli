#!/bin/env python

"""
I Ching Markdown Generator

This script generates a complete markdown document from I Ching hexagram data.
It processes a predefined set of hexagrams (01-64) and combines their JSON data
into a formatted markdown document suitable for book production.

Features:
1. Processes all 64 hexagrams in sequential order
2. Includes for each hexagram:
   - Core information and description
   - Hexagram image with analysis
   - Line interpretations
   - Related stories
   - Historical context
   - Notes section
3. Adds YAML frontmatter for document metadata
4. Includes proper page breaks for book formatting
5. Uses image set 's0' by default

Input:
    - JSON files from /home/jw/src/iching_cli/book/final/
    - Each file named as XX.json (01.json through 64.json)
    - YAML configuration from /home/jw/store/src/iching_cli/book/export.yaml

Output:
    - Creates output.md in the current directory
    - Includes all hexagrams in a single markdown document
    - Formatted with proper page breaks and sections

Dependencies:
    - colorama for terminal output
    - openai for GPT processing
    - pyyaml for frontmatter handling
"""

# Predefined list of all hexagrams
HEXAGRAMS = ['X01']
# HEXAGRAMS = [
#     'X01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
#     '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
#     '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
#     '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
#     '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
#     '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
#     '61', '62', '63', '64'
# ]

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
                    "content": "You are a literary writer. Rewrite the given text in an elegant, flowing style while preserving all key information."
                },
                {
                    "role": "user",
                    "content": text
                }]
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
    Read the hexagram description from a text file.

    Args:
        sfnum (str): Hexagram number (e.g., 'X01')

    Returns:
        str: Contents of the hexagram description file, or None if file not found
    """
    try:
        with open(f'{ROOT}/{sfnum}_hex.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {ROOT}/{sfnum}_hex.txt: {e}")
        input(f"Paused on ERROR reading file {ROOT}/{sfnum}_hex.txt")
        return None

def format_core_section(core,sfnum):
    # Read the hexagram description
    img_desc = get_hex_blurb(sfnum)
    if img_desc is None:
        # Fallback to generating description if file not found
        img_desc = f""" This hexagram contributes {core['order8child']} qualities to the tholon of {core['order8parent']}.  Its perspective is one of {core['perspective']} . Its nature is one  of  {core['nature']}, and its {core['action']} is that of Manifesting.  It achieves success through {core['success_through']}.  It' energy is {core['energy_cycle']} {core['yinyang_balance']}.  The challange to overcome is {core['challenge']}.
"""
        img_desc = img_desc.replace(";",", ")
        img_desc = img_desc.lower()
        img_desc = rewrite_literary_style(img_desc,sfnum)

    image_blurb = get_image_blurb(sfnum)

    """Format the core hexagram section"""

    # setnu,m is used to select whocui image and descriptions top use
    # s0 = 1280x1280, s1 = 1280x9-something
    # setnum = "_s1"

#^██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
    # changed below from
    ### *{core['image']}; {image_blurb}*
    #

    ostr = f"""
<div style="page-break-after: always;"></div>
<div style="page-break-before: right;"></div>
# {core['king_wen_sequence']} {core['hexagram']} *{core['binary_sequence']}* - {core['name']}
## {core['description']}

<img src="{ROOT}/{core['image_file']}">

### *{image_blurb}*
<div style="page-break-after: always;"></div>

#### {img_desc}

### **King Wen Order**: {core['king_wen_title']} **Binary**: {core['binary_sequence']} **Above**: {core['above']} **Below**: {core['below']}


# Lines in Transition

6: {core['lines_in_transition']['6']}
5: {core['lines_in_transition']['5']}
4: {core['lines_in_transition']['4']}
3: {core['lines_in_transition']['3']}
2: {core['lines_in_transition']['2']}
1: {core['lines_in_transition']['1']}

# Tholonic Analysis
**Negotiation**: {core['tholonic_analysis']['negotiation']}

**Limitation**: {core['tholonic_analysis']['limitation']}

**Contribution**: {core['tholonic_analysis']['contribution']}

**Significance in the Thologram**: {core['tholonic_analysis']['significance_in_thologram']}

**No Moving Lines**: {core['no_moving_lines']}

**All Moving Lines**: {core['all_moving_lines']}"""
    return ostr

def format_stories_section(stories):
    """Format the three stories section"""
    result = f"\n\n# {stories['title']}\n\n"

    for story in stories['stories']:
        udesc = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', story['description'])
        result += f"""
##### {story['title']}
### In the style of {story['style']}

{udesc}

#### *Lines in Context:*

6: {story['key_elements']['6']}
5: {story['key_elements']['5']}
4: {story['key_elements']['4']}
3: {story['key_elements']['3']}
2: {story['key_elements']['2']}
1: {story['key_elements']['1']}


"""

    return result

def format_history_section(history,core):
    """Format the historical event section"""
    return f"""
# '{core['name']}' in History

## *{history['title']}*

{history['description']}

*Source: {history['source']}*

#### *Lines in Context:*
6: {history['key_elements']['6']}
5: {history['key_elements']['5']}
4: {history['key_elements']['4']}
3: {history['key_elements']['3']}
2: {history['key_elements']['2']}
1: {history['key_elements']['1']}
"""
#*██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

def format_intro_section(args):
    """Format the intro section"""
    if args.content == "all":
        with open(f"{ROOT}/BOOK_INTRO.md", 'r', encoding='utf-8') as file:
            intro = file.read()

        intro += "\n<div style=\"page-break-after: always;\"></div>\n"
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
    markdown += format_core_section(json_data['hx']['core'],sfnum)

    # Add stories section
    markdown += format_stories_section(json_data['hx']['stories'])

    # Add history section
    markdown += "\n\n" + format_history_section(json_data['hx']['history'],json_data['hx']['core'])

    markdown += """

<div style="page-break-after: always;"></div>
# *Notes*
<div style="page-break-after: always;"></div>
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

def main():
    # Simplified main without command line arguments
    markdown_output = ""

    # setnum = "s0"  # Default image set

    for sfnum in HEXAGRAMS:
        filename = f"{ROOT}/{sfnum}.json"
        print(Fore.GREEN + filename + Style.RESET_ALL)

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
    output_file = "output.md"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_output)
    print(f"Markdown has been saved to {output_file}")

if __name__ == "__main__":
    main()