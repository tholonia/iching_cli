#!/bin/env python

"""

Creates the temporary output file, which is a markdown version of all 64 hexagrams with teh images and explanations, plus the forward text.

See JNOTES.md for more details.


This script converts I-Ching (易經/Book of Changes) data from JSON format into formatted Markdown documents.

Key functionality:
1. File Processing:
   - Takes JSON files containing I-Ching hexagram data
   - Can process either a single hexagram or all 64 hexagrams
   - Supports different image sets through -s/--set parameter

2. Content Generation:
   - Creates structured Markdown with sections for:
     - Core hexagram information (number, name, description)
     - Hexagram image
     - Line interpretations
     - Tholonic analysis
     - Stories related to the hexagram
     - Historical context
     - Notes section

3. Special Features:
   - Uses OpenAI's GPT-4 to rewrite descriptions in literary style
   - Caches AI-generated descriptions
   - Includes YAML frontmatter from external config
   - Supports page breaks for document formatting
   - Can generate complete books (--content all) or specific pages (--content pages)

4. File Organization:
   - Works with directory structure under /home/jw/store/src/iching_cli/defs/
   - Handles multiple image sets (s0, s1, etc)
   - Creates and manages cached descriptions

5. Command Line Interface:
   - Arguments:
     -o/--output: Specify output file
     -x/--hex: Select specific hexagram
     -s/--set: Choose image set
     -c/--content: Select content type (all/pages)
"""

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

def rewrite_literary_style(text, hexagram_id, setnum):
    # Try reading from cache first
    tdir = f"/home/jw/store/src/iching_cli/defs/final/{setnum}/descp/"
    ensure_directory_exists(tdir)

    try:
        with open(f"{tdir}/{hexagram_id}_descp.txt", 'r', encoding='utf-8') as f:
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

            cfile = f"/home/jw/store/src/iching_cli/defs/final/{setnum}/descp/{hexagram_id}_descp.txt"
            # print(cfile)
            # Cache the result
            with open(cfile, 'w', encoding='utf-8') as f:
                f.write(result)

            return result
        except Exception as e:
            print(f"OpenAI API error: {e}")
            input("Paused on ERROR OpenAI API error")
            return text

def get_image_blurb(sfnum,setnum):
    try:
        with open(f'/home/jw/store/src/iching_cli/defs/final/{setnum}/{sfnum}.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file final/{id}.txt: {e}")
        input("Paused on ERROR reading file final/{id}.txt")
        return None

def format_core_section(core,sfnum,setnum):

# make paaragraph

    descp = f""" This hexagram contributes {core['order8child']} qualities to the tholon of {core['order8parent']}.  Its perspective is one of {core['perspective']} . Its nature is one  of  {core['nature']}, and its {core['action']} is that of Manifesting.  It achieves success through {core['success_through']}.  It' energy is {core['energy_cycle']} {core['yinyang_balance']}.  The challange to overcome is {core['challenge']}.
"""
    descp = descp.replace(";",", ")
    descp = descp.lower()
    descp = rewrite_literary_style(descp,sfnum,setnum)

    image_blurb = get_image_blurb(sfnum,setnum)



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

<img src="/home/jw/store/src/iching_cli/defs/final/{setnum}/{core['image_file']}">

### *{image_blurb}*
<div style="page-break-after: always;"></div>

#### {descp}

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
        with open("/home/jw/store/src/iching_cli/defs/BOOK_INTRO.md", 'r', encoding='utf-8') as file:
            intro = file.read()

        intro += "\n<div style=\"page-break-after: always;\"></div>\n"
    elif args.content == "pages":
        intro = ""
    return intro

def get_yaml():
    yaml_path = "/home/jw/store/src/iching_cli/defs/export.yaml"
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

def generate_markdown_from_json(json_data, sfnum,setnum):
    """Generate complete markdown using all JSON sections"""
    markdown = get_yaml()

    # Add core section
    markdown += format_core_section(json_data['hx']['core'],sfnum,setnum)

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
    directory = "/home/jw/src/iching_cli/defs/final"
    json_files = glob.glob(os.path.join(directory, "*.json"))

    sfiles = sorted(os.path.basename(f) for f in json_files)

    for i in range(len(sfiles)):
        sfiles[i] = directory + "/" + sfiles[i]


    # print(sfiles)
    # exit()
    return sfiles

def main():
    parser = argparse.ArgumentParser(description='Convert I-Ching JSON data to complete Markdown format')
    # parser.add_argument('template_file', help='Template markdown file path')
    # parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('-o', '--output', help='Output markdown file path (optional)')
    parser.add_argument('-x', '--hex', help='Seclet a specific hexagram only to make (optional)')
    parser.add_argument('-s', '--set', help='Set number to use for imnages and img blurbs (default:0)')
    parser.add_argument('-c', '--content', default="all", help='"pages" or "all" (default:"all")')

    args = parser.parse_args()

    # Read the template file (for reference structure)
    # template = read_template(args.template_file)


    hfrom = 1
    hto = 65
    if args.hex:
        hfrom = int(args.hex)
        hto = int(args.hex)

    if hfrom == hto: #! this is only to test if we are printing specific pages, for testing.
        markdown_output = ""
    else: #! don't need to add intro if printing a single page
        # markdown_output = format_intro_section(args)
        markdown_output = "" # skip intro



    # for filename in get_json_filenames():


    directory = "/home/jw/src/iching_cli/defs/final"


    array = [int(args.hex)] if hfrom == hto else list(range(hfrom,hto))


    for i in range(len(array)):
        fnum = array[i]
        sfnum = f"{fnum:02d}"
        # filename = directory + "/" + sfnum + "/" + sfnum + ".json"
        filename = directory + "/"  + sfnum + ".json"
        print(Fore.GREEN + filename + Style.RESET_ALL)

        # Read the JSON file
        print(Fore.YELLOW + "Reading " + filename + Style.RESET_ALL)
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)


        if args.set:
            setnum = f"s{args.set}"
        else:
            setnum = "s0"

        # Generate markdown
        markdown_output += "\n"+generate_markdown_from_json(json_data, sfnum,setnum)

    # Handle output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(markdown_output)
        print(f"Markdown has been saved to {args.output}")
    else:
        print(markdown_output)


if __name__ == "__main__":
    main()