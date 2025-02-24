#!/bin/env python

"""
=============================================================================
makeallmd.py - I Ching Book Markdown Generator
=============================================================================

Description:
  This script generates a formatted markdown document for the I Ching book by
  combining JSON data, generated descriptions, and images into a cohesive
  document structure.

Usage:
  python makeallmd.py [--content {all,pages}] [--test]

Arguments:
  --content: Choose content to include
    all: Include introduction and hexagram pages (default)
    pages: Include only hexagram pages
  --test: Use test set of hexagrams instead of full set
    When active, uses test_HEXAGRAMS = ['01']
    When inactive, uses all 64 hexagrams

Process:
  1. Processes hexagrams defined in HEXAGRAMS list
     (or test_HEXAGRAMS if --test is active)
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

Dependencies:
  - Required Python packages:
    - colorama: Terminal output formatting
    - pyyaml: YAML frontmatter handling
    - json: JSON data parsing
    - re: Regular expression text processing
    - argparse: Command line argument parsing

File Structure:
  Input:
    - /BOOK_INTRO.md: Introduction text
    - /*.json: Hexagram data files (XX.json where XX is hexagram number)
    - /*_img.txt: Cached image descriptions
    - /*_hex.txt: Cached hexagram descriptions
    - /export.yaml: Document metadata and configuration
  Output:
    - includes/iching.md: Complete markdown document with TOC

TOC Structure:
  - Adds navigation element at start of document:
    <nav role="doc-toc">
      <h1>Table of Contents</h1>
    </nav>
  - Required for Prince PDF generation
  - Must be properly formatted for CSS styling

Environment:
  - ROOT: Base directory containing required input files

Example:
  # Generate full book with all hexagrams
  python makeallmd.py --content all

  # Generate only hexagram pages with test set
  python makeallmd.py --content pages --test

Author: JW
Last Updated: 2024
=============================================================================
"""
# Predefined list of all hexagrams
# xHEXAGRAMS = [ '20','23','28','30','31','39','55','56','59']
test_HEXAGRAMS = [ '01','02','03']

from funcs_lib import wen_values

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
from pprint import pprint

def ensure_directory_exists(tdir):
    """Create the description directory if it doesn't exist"""
    if not os.path.exists(tdir):
        try:
            os.makedirs(tdir, exist_ok=True)
            print(f"Created directory: {tdir}")
        except Exception as e:
            print(f"Error (r03) creating directory {tdir}: {e}")
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
        with open(f'{ROOT}/prod/{sfnum}_img.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error (r04) reading file {ROOT}/{sfnum}.txt: {e}")
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
        with open(f'{ROOT}/prod/{sfnum}_hex.txt', 'r', encoding='utf-8') as f:
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
        print(Fore.RED + f"Error (r05) reading file {ROOT}/{sfnum}_hex.txt: {e}" + Style.RESET_ALL)
        input(f"Paused on ERROR reading file {ROOT}/{sfnum}_hex.txt")
        return None

def format_core_section(core, sfnum):
    image_file = f"{ROOT}/{sfnum}.png"
    # Read the hexagram description
    hex_desc_ary = get_hex_blurb(sfnum)

    image_blurb = get_image_blurb(sfnum)

    """Format the core hexagram section"""


    """
### {core['trigram_phrase']['Thermodynamics']} *--Thermodynamics*
### {core['trigram_phrase']['Taoist']} *--Taoist*
### {core['trigram_phrase']['Platonic']} *--Platonic*
### {core['trigram_phrase']['Jungian']} *--Jungian*
### {core['trigram_phrase']['Tholonic']} *--Tholonic*
    """

    hexline_style= "font-size: 1.8em;  vertical-align: middle;"
    ostr = f"""

# &nbsp;

<div style="margin: 0 auto; text-align: center;border-bottom:1px solid #c5c5c5;padding-bottom:1em;">
<span style="font-size:2em;color:#666;text-align:center;font-weight:normal;padding-bottom:0.2em;font-family:'LinLibertine',serif;">{core['king_wen']['sequence']} {core['hexagram_code']}</span><span style="font-size:1em;color:#666;text-align:center;font-weight:normal;padding-bottom:0.2em;font-family:'LinLibertine',serif;vertical-align:text-bottom;"> {core['binary_sequence']} </span><span style="font-size:2em;color:#666;text-align:center;font-weight:normal;padding-bottom:0.2em;font-family:'LinLibertine',serif;">&nbsp; {core['name']}</span>
</div>
## {core['description']}
<img src="{ROOT}/prod/{core['image']['file']}">
<span style="margin-bottom: 8px;"> &nbsp; </span>
### *{image_blurb}*
<p/>

#### {hex_desc_ary[0]}
#### {core['tholonic_analysis']['significance_in_thologram']} {hex_desc_ary[1]}

#### ***Trigrams***
"*{core['trigram_phrase']['general']}*": {core['trigram_phrase']['explanation']}
"""


    ostr += f"""

#### ***Lines in Transition***

<ul><li><B>{core['lines'][5]['position']}</B> ({core['line_type'][5]}) <I>{core['lines'][5]['name']}</I> - {core['lines'][5]['meaning']}\n<i>Moving line</i>: {core['lines'][5]['changing']}</li></ul>
<ul><li><B>{core['lines'][4]['position']}</B> ({core['line_type'][4]}) <I>{core['lines'][4]['name']}</I> - {core['lines'][4]['meaning']}\n<i>Moving line</i>: {core['lines'][4]['changing']}</li></ul>
<ul><li><B>{core['lines'][3]['position']}</B> ({core['line_type'][3]}) <I>{core['lines'][3]['name']}</I> - {core['lines'][3]['meaning']}\n<i>Moving line</i>: {core['lines'][3]['changing']}</li></ul>
<ul><li><B>{core['lines'][2]['position']}</B> ({core['line_type'][2]}) <I>{core['lines'][2]['name']}</I> - {core['lines'][2]['meaning']}\n<i>Moving line</i>: {core['lines'][2]['changing']}</li></ul>
<ul><li><B>{core['lines'][1]['position']}</B> ({core['line_type'][1]}) <I>{core['lines'][1]['name']}</I> - {core['lines'][1]['meaning']}\n<i>Moving line</i>: {core['lines'][1]['changing']}</li></ul>
<ul><li><B>{core['lines'][0]['position']}</B> ({core['line_type'][0]}) <I>{core['lines'][0]['name']}</I> - {core['lines'][0]['meaning']}\n<i>Moving line</i>: {core['lines'][0]['changing']}</li></ul>

#### **No Moving Lines**: {core['transformations']['no_moving_lines']}
#### **All Moving Lines**: {core['transformations']['all_moving_lines']}

#### ***Tholonic Analysis***
**Negotiation**: {core['tholonic_analysis']['negotiation']} **Limitation**: {core['tholonic_analysis']['limitation']} **Contribution**: {core['tholonic_analysis']['contribution']}"""


    asc_hbval = wen_values[core['pairpath']['ascending_hex_num']][1]
    des_hbval = wen_values[core['pairpath']['descending_hex_num']][1]


    ostr += f"""

#### ***The 32 Paths***
#### The *{core['pairpath']['kstate']}* path of *{core['pairpath']['title']}* hold "{core['pairpath']['ascending_hex_name']}" ({core['pairpath']['ascending_hex_num']} <sub>*{asc_hbval}*</sub>) and *{core['pairpath']['descending_hex_name']}* ({core['pairpath']['descending_hex_num']} <sub>*{des_hbval}*</sub>).  {core['pairpath']['description']}

"""
    return ostr

def format_stories_section(core,stories):
    """Format the three stories section"""
    result = f"\n\n###### {stories['title']}\n\n"

    for story in stories['entries']:
        udesc = re.sub(r'(?<!\n)\n(?!\n)', '\n\n', story['short_story'])

        result += f"""
##### {story['title']}
### *In the style of {story['theme']}*

#### {udesc}

#### ***Lines in Context:***
<ul><li><B>1</B> ({core['line_type'][5]}) <i>{story['lines_in_context']['1']['name']}</i> - {story['lines_in_context']['1']['meaning']} <i>Moving line</i> - {story['lines_in_context']['1']['changing']}</li></ul>
<ul><li><B>2</B> ({core['line_type'][4]}) <i>{story['lines_in_context']['2']['name']}</i> - {story['lines_in_context']['2']['meaning']} <i>Moving line</i> - {story['lines_in_context']['2']['changing']}</li></ul>
<ul><li><B>3</B> ({core['line_type'][3]}) <i>{story['lines_in_context']['3']['name']}</i> - {story['lines_in_context']['3']['meaning']} <i>Moving line</i> - {story['lines_in_context']['3']['changing']}</li></ul>
<ul><li><B>4</B> ({core['line_type'][2]}) <i>{story['lines_in_context']['4']['name']}</i> - {story['lines_in_context']['4']['meaning']} <i>Moving line</i> - {story['lines_in_context']['4']['changing']}</li></ul>
<ul><li><B>5</B> ({core['line_type'][1]}) <i>{story['lines_in_context']['5']['name']}</i> - {story['lines_in_context']['5']['meaning']} <i>Moving line</i> - {story['lines_in_context']['5']['changing']}</li></ul>
<ul><li><B>6</B> ({core['line_type'][0]}) <i>{story['lines_in_context']['6']['name']}</i> - {story['lines_in_context']['6']['meaning']} <i>Moving line</i> - {story['lines_in_context']['6']['changing']}</li></ul>
"""

    return result

def format_history_section(history, core):
    """Format the historical event section"""
    return f"""
###### '{core['name']}' in History

##### *{history['title']}*

#### {history['short_story']}

<div style="font-size: 8pt;font-style:italic">Source: {', '.join(history['source'])}</div>

#### ***Lines in History:***

<ul><li><B>1</B> ({core['line_type'][5]}) <i>{history['lines_in_history']['1']['name']}</i> - {history['lines_in_history']['1']['meaning']} <i>Moving line</i> - {history['lines_in_history']['1']['changing']}</li></ul>
<ul><li><B>2</B> ({core['line_type'][4]}) <i>{history['lines_in_history']['2']['name']}</i> - {history['lines_in_history']['2']['meaning']} <i>Moving line</i> - {history['lines_in_history']['2']['changing']}</li></ul>
<ul><li><B>3</B> ({core['line_type'][3]}) <i>{history['lines_in_history']['3']['name']}</i> - {history['lines_in_history']['3']['meaning']} <i>Moving line</i> - {history['lines_in_history']['3']['changing']}</li></ul>
<ul><li><B>4</B> ({core['line_type'][2]}) <i>{history['lines_in_history']['4']['name']}</i> - {history['lines_in_history']['4']['meaning']} <i>Moving line</i> - {history['lines_in_history']['4']['changing']}</li></ul>
<ul><li><B>5</B> ({core['line_type'][1]}) <i>{history['lines_in_history']['5']['name']}</i> - {history['lines_in_history']['5']['meaning']} <i>Moving line</i> - {history['lines_in_history']['5']['changing']}</li></ul>
<ul><li><B>6</B> ({core['line_type'][0]}) <i>{history['lines_in_history']['6']['name']}</i> - {history['lines_in_history']['6']['meaning']} <i>Moving line</i> - {history['lines_in_history']['6']['changing']}</li></ul>
"""

def format_intro_section(args):
    """Format the intro section"""
    if args.content == "all":
        with open(f"{ROOT}/includes/BOOK_INTRO.md", 'r', encoding='utf-8') as file:
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
    core = json_data
    markdown += format_core_section(core, sfnum)

    # Add stories section
    markdown += format_stories_section(json_data,json_data['stories'])

    # Add history section
    markdown += "\n\n" + format_history_section(json_data['history'], json_data)

    # Safely access the 'above' and 'below' keys
    above = core['trigrams']['above']
    below = core['trigrams']['below']

    if isinstance(above, dict):
        above_symbol = above.get('Symbol', 'N/A')
        above_quality = above.get('Quality', 'N/A')
        above_num = above.get('Trigram Number', 'N/A')
        above_bin = above.get('Binary Decimal', 'N/A')
        above_meaning = above.get('Meaning', 'N/A')
        above_engtr = above.get('English Translation', 'N/A')
    else:
        above_symbol = 'N/A'
        above_quality = 'N/A'
        above_num = 'N/A'
        above_bin = 'N/A'
        above_meaning = 'N/A'
        above_engtr = 'N/A'

    if isinstance(below, dict):
        below_symbol = below.get('Symbol', 'N/A')
        below_quality = below.get('Quality', 'N/A')
        below_num = below.get('Trigram Number', 'N/A')
        below_bin = below.get('Binary Decimal', 'N/A')
        below_meaning = below.get('Meaning', 'N/A')
        below_engtr = below.get('English Translation', 'N/A')
    else:
        below_symbol = 'N/A'
        below_quality = 'N/A'
        below_num = 'N/A'
        below_bin = 'N/A'
        below_meaning = 'N/A'
        below_engtr = 'N/A'


# removed from notes section: <div style="page-break-before: always;"></div>

    markdown += f"""

###### *Notes*
### **King Wen**: {core['king_wen']['sequence']} {core['hexagram_code']} <sub>*{core['binary_sequence']}*</sub> {core['king_wen']['common_title']}; {above_num} {above_symbol} <sub>*{above_bin}*</sub> {above_meaning},  {above_engtr} *over* {below_num} {below_symbol} <sub>*{below_bin}*</sub> {below_meaning}, {below_engtr};
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

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
        default='pages',
        help='Include all content (with intro) or just hexagram pages'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Use test hexagrams instead of full set'
    )
    args = parser.parse_args()


    return args

def get_json_version():
    """
    Read version string from VER_JSON.txt file.
    Returns empty string if file is empty or doesn't exist.
    """
    try:
        with open(f"{ROOT}/includes/VER_JSON.txt", 'r', encoding='utf-8') as f:
            version = f.readline().strip()
            return version if version else ""
    except (FileNotFoundError, IOError):
        return ""

def flatten_json(json_data):
    """
    Flattens a nested JSON structure into a 1D dictionary with intuitive key names.

    Args:
        json_data (dict): The JSON data to flatten

    Returns:
        dict: Flattened dictionary with dot-notation keys
    """
    flat_dict = {}

    def flatten(data, prefix=''):
        if isinstance(data, dict):
            for key, value in data.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    flatten(value, new_prefix)
                else:
                    flat_dict[new_prefix] = value
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_prefix = f"{prefix}[{i}]"
                if isinstance(item, (dict, list)):
                    flatten(item, new_prefix)
                else:
                    flat_dict[new_prefix] = item
        else:
            flat_dict[prefix] = data

    flatten(json_data)
    return flat_dict

def main():
    # Parse command line arguments
    args = parse_args()

    # Set HEXAGRAMS based on --test flag
    global HEXAGRAMS
    if args.test:
        HEXAGRAMS = test_HEXAGRAMS
        print(Fore.YELLOW + "Using test hexagrams: " + str(HEXAGRAMS) + Style.RESET_ALL)

    # Get intro section if requested
    markdown_output = format_intro_section(args)

    # Load the version string
    json_version = get_json_version()


    for sfnum in HEXAGRAMS:
        # Construct the filename using the version string
        filename = f"{ROOT}/{json_version}/{sfnum}.json"

        # Read the JSON file
        print(Fore.YELLOW + "Reading " + filename + Style.RESET_ALL)
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            print(Fore.RED + f"Error (r01): File {filename} not found" + Style.RESET_ALL)
            continue
        except json.JSONDecodeError:
            print(Fore.RED + f"Error (r02): Invalid JSON in {filename}" + Style.RESET_ALL)
            continue

        # flat_json = flatten_json(json_data)
        # pprint(flat_json)
        # exit()

        # Generate markdown
        markdown_output += "\n" + generate_markdown_from_json(json_data, sfnum)

    # Write output to file
    output_file = f"{ROOT}/includes/iching.md"
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(markdown_output)

# currently not used
    toc_marker = f"""\n\n
<nav role="doc-toc">
<h1>Table of Contents</h1>
</nav>

!!!div style=\"page-break-before: always;\">!!!/div>\n\n
    """

    # Write TOC marker to beginning of file
    with open(output_file, 'r', encoding='utf-8') as file:
        content = file.read()

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)


    print(f"Markdown has been saved to {output_file}")

if __name__ == "__main__":
    main()