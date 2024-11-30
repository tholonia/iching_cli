#!/bin/env python

import json
import sys
import argparse

def read_template(template_file):
    """Read and parse the template file into sections"""
    with open(template_file, 'r', encoding='utf-8') as file:
        template = file.read()
    return template

def format_core_section(core):
    """Format the core hexagram section"""
    return f"""# {core['hexagram']} {core['name']}

{core['description']}

**King Wen Sequence**: {core['king_wen_sequence']}
**King Wen Title**: {core['king_wen_title']}
**Binary Sequence**: {core['binary_sequence']}
**Above**: {core['above']}
**Below**: {core['below']}
**Perspective**: {core['perspective']}
**Nature**: {core['nature']}
**Action**: {core['action']}
**Success through**: {core['success_through']}
**Image**: {core['image']}
**Challenge**: {core['challenge']}
**8-Fold**: This hexagram contributes **"{core['order8child']}"** qualities to the **"{core['order8parent']}"** class.

## Lines in Transition
**Line 6**: *{core['lines_in_transition']['6']}*
**Line 5**: *{core['lines_in_transition']['5']}*
**Line 4**: *{core['lines_in_transition']['4']}*
**Line 3**: *{core['lines_in_transition']['3']}*
**Line 2**: *{core['lines_in_transition']['2']}*
**Line 1**: *{core['lines_in_transition']['1']}*

## Tholonic Analysis
**Negotiation**: {core['tholonic_analysis']['negotiation']}

**Limitation**: {core['tholonic_analysis']['limitation']}

**Contribution**: {core['tholonic_analysis']['contribution']}

**Significance in the Thologram**: {core['tholonic_analysis']['significance_in_thologram']}

**No Moving Lines**: {core['no_moving_lines']}
**All Moving Lines**: {core['all_moving_lines']}"""

def format_stories_section(stories):
    """Format the three stories section"""
    result = f"\n\n# Three Tales of \"{stories['title']}\"\n\n"

    for story in stories['stories']:
        result += f"""## {story['title']}
*In the style of {story['style']}*

{story['description']}

### Key Elements:

Line 6: {story['key_elements']['6']}
Line 5: {story['key_elements']['5']}
Line 4: {story['key_elements']['4']}
Line 3: {story['key_elements']['3']}
Line 2: {story['key_elements']['2']}
Line 1: {story['key_elements']['1']}\n\n"""

    return result

def format_history_section(history):
    """Format the historical event section"""
    return f"""# {history['title']}

## {history['subtitle']}

{history['description']}

*Source: {history['source']}*

### Key Elements:
Line 6: {history['key_elements']['6']}
Line 5: {history['key_elements']['5']}
Line 4: {history['key_elements']['4']}
Line 3: {history['key_elements']['3']}
Line 2: {history['key_elements']['2']}
Line 1: {history['key_elements']['1']}"""

def generate_markdown_from_json(json_data):
    """Generate complete markdown using all JSON sections"""
    markdown = ""

    # Add core section
    markdown += format_core_section(json_data['hx']['core'])

    # Add stories section
    markdown += format_stories_section(json_data['hx']['stories'])

    # Add history section
    markdown += "\n\n" + format_history_section(json_data['hx']['history'])

    return markdown

def main():
    parser = argparse.ArgumentParser(description='Convert I-Ching JSON data to complete Markdown format')
    parser.add_argument('template_file', help='Template markdown file path')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('-o', '--output', help='Output markdown file path (optional)')

    args = parser.parse_args()

    try:
        # Read the template file (for reference structure)
        template = read_template(args.template_file)

        # Read the JSON file
        with open(args.input_file, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        # Generate markdown
        markdown_output = generate_markdown_from_json(json_data)

        # Handle output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(markdown_output)
            print(f"Markdown has been saved to {args.output}")
        else:
            print(markdown_output)

    except FileNotFoundError as e:
        print(f"Error: File not found - {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{args.input_file}'")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()