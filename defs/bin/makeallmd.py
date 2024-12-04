#!/bin/env python

import json
import sys
import argparse
import glob
import os
from colorama import Fore, Style
import openai


from openai import OpenAI

def rewrite_literary_style(text, hexagram_id):
    # Try reading from cache first
    try:
        with open(f"/home/jw/store/src/iching_cli/defs/final/descp/{hexagram_id}_descp.txt", 'r', encoding='utf-8') as f:
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

            # Cache the result
            with open(f"{hexagram_id}_descq.txt", 'w', encoding='utf-8') as f:
                f.write(result)

            return result
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return text

def get_image_blurb(sfnum):
    try:
        with open(f'/home/jw/store/src/iching_cli/defs/final/{sfnum}.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file final/{id}.txt: {e}")
        return None

def format_core_section(core,sfnum):

# make paaragraph

    descp = f""" This hexagram contributes {core['order8child']} qualities to the tholon of {core['order8parent']}.  Its perspective is one of {core['perspective']} . Its nature is one  of  {core['nature']}, and its {core['action']} is that of Manifesting.  It achieves success through {core['success_through']}.  It' energy is {core['energy_cycle']} {core['yinyang_balance']}.  The challange to overcome is {core['challenge']}.
"""
    descp = descp.replace(";",", ")
    descp = descp.lower()
    descp = rewrite_literary_style(descp,sfnum)

    image_blurb = get_image_blurb(sfnum)



    """Format the core hexagram section"""

    ostr = f"""
<div style="page-break-after: always;"></div>
# {core['hexagram']} {core['name']}
## {core['description']}

<img src="/home/jw/store/src/iching_cli/defs/final/{core['image_file']}" />
### *{core['image']}; {image_blurb}*

#### {descp}


### **King Wen Sequence**: {core['king_wen_sequence']}, {core['king_wen_title']} **Binary Sequence**: {core['binary_sequence']} **Above**: {core['above']} **Below**: {core['below']}


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
        result += f"""
##### {story['title']}
### In the style of {story['style']}

{story['description']}

#### *Lines in Context:*

6: {story['key_elements']['6']}
5: {story['key_elements']['5']}
4: {story['key_elements']['4']}
3: {story['key_elements']['3']}
2: {story['key_elements']['2']}
1: {story['key_elements']['1']}\n\n"""

    return result

def format_history_section(history):
    """Format the historical event section"""
    return f"""
# {history['subtitle']}

## *{history['title']}*

{history['description']}

*Source: {history['source']}*

#### *Lines in Context:*
6: {history['key_elements']['6']}
5: {history['key_elements']['5']}
4: {history['key_elements']['4']}
3: {history['key_elements']['3']}
2: {history['key_elements']['2']}
1: {history['key_elements']['1']}"""

def generate_markdown_from_json(json_data,sfnum):
    """Generate complete markdown using all JSON sections"""
    markdown = ""

    # Add core section
    markdown += format_core_section(json_data['hx']['core'],sfnum)

    # Add stories section
    markdown += format_stories_section(json_data['hx']['stories'])

    # Add history section
    markdown += "\n\n" + format_history_section(json_data['hx']['history'])

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

    args = parser.parse_args()

    # Read the template file (for reference structure)
    # template = read_template(args.template_file)

    with open("/home/jw/store/src/iching_cli/defs/BOOK_INTRO.md", 'r', encoding='utf-8') as file:
        markdown_output = file.read()

    # for filename in get_json_filenames():

    directory = "/home/jw/src/iching_cli/defs/final"

    for fnum in range(1,65):
        sfnum = f"{fnum:02d}"
        # filename = directory + "/" + sfnum + "/" + sfnum + ".json"
        filename = directory + "/"  + sfnum + ".json"
        print(Fore.GREEN + filename + Style.RESET_ALL)

        # Read the JSON file
        print(Fore.YELLOW + "Reading " + filename + Style.RESET_ALL)
        with open(filename, 'r', encoding='utf-8') as file:
            json_data = json.load(file)



        # Generate markdown
        markdown_output += "\n"+generate_markdown_from_json(json_data, sfnum)

    # Handle output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(markdown_output)
        print(f"Markdown has been saved to {args.output}")
    else:
        print(markdown_output)


if __name__ == "__main__":
    main()