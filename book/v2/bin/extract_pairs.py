#!/bin/env python

import os
import json

# Get all json files in ../regen directory
regen_dir = "../regen"
json_files = [f for f in os.listdir(regen_dir) if f.endswith('.json')]

# Process each json file
for json_file in json_files:
    file_path = os.path.join(regen_dir, json_file)

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Extract pairpath if it exists
        pstr = ""
        if 'pairpath' in data:
            pairpath = data['pairpath']
            pstr +=  f"{pairpath['ascending_hex_num']},"
            pstr +=  f"{pairpath['ascending_hex_name']},"
            pstr +=  f"{pairpath['descending_hex_num']},"
            pstr +=  f"{pairpath['descending_hex_name']},"
            pstr += f"{pairpath['title']}"

        print(pstr)

    except json.JSONDecodeError:
        print(f"Error decoding JSON from {json_file}")
    except Exception as e:
        print(f"Error processing {json_file}: {str(e)}")
