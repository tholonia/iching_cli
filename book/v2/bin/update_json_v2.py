#!/bin/env python

import os
import sys
import json
import openai
import re
from colorama import Fore, Style
import jsonschema
from jsonschema import validate



def save_json_to_file(json_data, target_filename, color=Fore.GREEN):
    """
    Save JSON data to a specified file.

    Args:
        json_data: The JSON data to save.
        target_filename: The path to the target file where JSON data will be saved.
    """
    try:
        with open(target_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4)
        print(color + f"JSON data successfully saved to {target_filename}" + Style.RESET_ALL)
    except Exception as e:
        print(color + f"Error saving JSON data to {target_filename}: {str(e)}" + Style.RESET_ALL)


def validate_json_schema(json_data, schema_path, hex_str):
    """
    Validate the JSON data against the schema

    Args:
        json_data: The JSON data to validate
        schema_path: Path to the schema file

    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """

    # Save a copy of the original JSON data to LAST.json
    # with open(f"{JSON_DIR}LAST.json", "w", encoding="utf-8") as f:
    #     json.dump(json_data, f, indent=4)
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        validate(instance=json_data, schema=schema)
        return True, "JSON is valid"
    except jsonschema.exceptions.ValidationError as ve:
        save_json_to_file(json_data, f"{JSON_DIR}{hex_str}_v2_BAD-valid-error.json",Fore.RED)
        return False #, f"JSON validation error: {str(ve)}"
    except jsonschema.exceptions.SchemaError as se:
        save_json_to_file(json_data, f"{JSON_DIR}{hex_str}_v2_BAD-schema-error.json",Fore.RED)
        return False #, f"Schema error: {str(se)}"
    except Exception as e:
        save_json_to_file(json_data, f"{JSON_DIR}{hex_str}_v2_BAD-expect=error.json",Fore.RED)
        return False #, f"Unexpected error during validation: {str(e)}"


# Define file paths
ICHING_PRIMER = "/home/jw/src/iching_cli/book/iching_primer.md"
THOLONIC_PRIMER = "/home/jw/src/iching_cli/book/tholonic_primer.md"
JSON_DIR = "/home/jw/src/iching_cli/book/v2/"

# Ensure command line argument is provided
if len(sys.argv) != 2:
    print("Usage: script.py <hexagram_number>")
    sys.exit(1)

# Validate and format the hexagram number
hex_num = sys.argv[1]
if not hex_num.isdigit() or not (1 <= int(hex_num) <= 64):
    print("Error: Hexagram number must be an integer between 1 and 64.")
    sys.exit(1)

hex_str = f"{int(hex_num):02}"
hex_filename = f"{hex_str}.json"
json_path = os.path.join(JSON_DIR, hex_filename)

# Ensure the JSON file exists
if not os.path.exists(json_path):
    print(f"Error: JSON file {json_path} not found.")
    sys.exit(1)

# Load files
with open(ICHING_PRIMER, "r", encoding="utf-8") as f:
    iching_content = f.read()

with open(THOLONIC_PRIMER, "r", encoding="utf-8") as f:
    tholonic_content = f.read()

with open(json_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# Prepare the prompt
prompt = f"""
### **Instructions for Updating `{hex_str}.json` with I-Ching and Tholonic Insights**

Modify only the values within this JSON structure while preserving its exact format.
Do not add, remove, or rename any keys.

            "lines_in_transition": {{
                "6": "",
                "5": "",
                "4": "",
                "3": "",
                "2": "",
                "1": ""
            }}

- Use the context from **`iching_primer.md`** and **`tholonic_primer.md`** to enhance the existing content in `{hex_str}.json`.
- **Do not modify the JSON structure**—retain the exact same keys and values, updating only the existing fields.
- ** DO NOT CREATE NEW FIELDS OR KEYS** - use ONLY the fields and keys that already exist.
- **Enhance and Update the values of the keys "1',"2","3","4","5","6" in the "lines_in_transition" section to include the significance of each line *AND* the significane of each lines if it changes from yin to yang or yang to yin.  Keep response to one paragraph.
- **Return only the updated JSON file**—no additional text or commentary.
- **DO NOT INCLUDE ANYTHING ELSE IN YOUR RESPONSE EXCEPT THE UPDATED JSON FILE.**

"""

# """
# - **Enhance and Update the sections "negotiation", "limitation", "contribution" in the "tholonic_analysis" section by explaining how the tholonic attributes of negotiation, limitation, and contribution, are expressed or instantiated or represented in this hexagram.
# """

# Make API request
client = openai.OpenAI()
response = client.chat.completions.create(
    # model="gpt-4-turbo-preview",
    model="o3-mini-2025-01-31",
    messages=[
        {"role": "system", "content": "You are an expert in I-Ching analysis."},
        {"role": "user", "content": prompt},
        {"role": "user", "content": f"iching_primer.md content:\n{iching_content}"},
        {"role": "user", "content": f"tholonic_primer.md content:\n{tholonic_content}"},
        {"role": "user", "content": f"Current JSON content:\n{json.dumps(json_data)}"},
    ],
)

# Extract updated JSON
response_text = response.choices[0].message.content

# Try to find JSON content within the response
# Look for content between triple backticks if present
json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
if json_match:
    updated_json = json_match.group(1)
else:
    # If no code blocks found, use the entire response
    updated_json = response_text

try:
    updated_data = json.loads(updated_json)
except Exception as e:
# except json.JSONDecodeError:
    print(Fore.RED + f"{JSON_DIR}{hex_str}_v2.json - Error: Could not parse JSON from API response." + Style.RESET_ALL)
    exit(1)
    # save_json_to_file(updated_data, f"{JSON_DIR}{hex_str}_v2_BAD-parse-error.json")
    # print("Response content:")
    # print(Fore.YELLOW + response_text + Style.RESET_ALL)
    # sys.exit(1)

# Validate the JSON against the schema
schema_path = f"{JSON_DIR}includes/schema.json"
try:
    is_valid, validation_message = validate_json_schema(updated_data, schema_path, hex_str)
except:
    is_valid = False
    validation_message = "{new_json_filename} Error: Could not validate JSON against schema."


new_json_filename = f"{JSON_DIR}{hex_str}_v2.json"

if not is_valid:
    print(f"{new_json_filename}: {validation_message} : New JSON content does not match schema:")
    # sys.exit(1)
else:
    print(Fore.GREEN + f"{new_json_filename}: New JSON content matches schema:" + Style.RESET_ALL)

# Save the updated JSON file
with open(new_json_filename, "w", encoding="utf-8") as f:
    json.dump(updated_data, f, indent=4)

# print(Fore.GREEN + f"Updated JSON saved to {output_filename}" + Style.RESET_ALL)

