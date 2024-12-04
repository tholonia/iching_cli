#!/bin/env python
def capitalize_words_in_file(filename):
    try:
        # Read the content of the file
        with open(filename, 'r') as file:
            content = file.read()

        # Process each line separately to preserve formatting
        lines = content.splitlines()
        modified_lines = []
        for line in lines:
            # Split line into words and update capitalized words
            words = line.split()
            modified_words = [word.capitalize() if word.isupper() else word for word in words]
            # Preserve original spacing by joining with original whitespace
            if words:
                last_index = 0
                modified_line = ''
                for word in words:
                    word_index = line.find(word, last_index)
                    modified_line += line[last_index:word_index]
                    modified_line += modified_words[words.index(word)]
                    last_index = word_index + len(word)
                modified_line += line[last_index:]  # Add any remaining whitespace
            else:
                modified_line = line  # Preserve empty lines
            modified_lines.append(modified_line)

        # Join lines back together with original line endings
        modified_content = '\n'.join(modified_lines)

        # Write the modified content back to the original file
        with open(filename, 'w') as file:
            file.write(modified_content)

        print(f"The file '{filename}' has been updated successfully.")
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# ... rest of the code ...

# Usage example

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Capitalize words in a text file.')
    parser.add_argument('filename', help='The path to the text file to process')

    args = parser.parse_args()
    capitalize_words_in_file(args.filename)