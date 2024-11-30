#!/bin/env python
import json
import sys

def load_and_print_description(json_file, key):
    try:
        # Load the JSON file
        with open(json_file, mode='r') as file:
            data = json.load(file)
            vnum = data[key]['num']
            vchar = data[key]['char']
            vpath = data[key]['path']
            vtype = data[key]['type']
            vtarot_num = data[key]['tarot_num']
            vtarot = data[key]['tarot']
            vdescription = data[key]['description']
            vassiah = data[key]['assiah']
            vtradnum = data[key]['pseq']
            vtheme = data[key]['theme']

            # Determine key class and functional key
            if int(key) > 31:
                key_class = "descending"
                opposite_key = str(63-int(key))
            else:
                key_class = "ascending"
                opposite_key = str(abs(int(key)-63))

            st = f"""
Related to the qabalah, the hexagram with a binary value of |{key}| (traditionally hex #|{vtradnum}|), represents the |{key_class}| aspect of |{vpath}| and the domain of |'{vtype}'|. It corresponds to the '|{vtarot}|' of the Tarot deck, and a theme of '|{vsudden_change}|', and generally understood as |'{vdescription}'|. Its spiritual influence in the material world is represented by |{vassiah}|."""

            print(st)

    except FileNotFoundError:
        print(f"Error: The file {json_file} was not found.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: script.py <json_file> <key>")
        sys.exit(1)

    # JSON file name and key from command line arguments
    json_file = sys.argv[1]
    key = sys.argv[2]

    # Load the JSON file and print the description and theme for a specific key
    load_and_print_description(json_file, key)

if __name__ == "__main__":
    main()
