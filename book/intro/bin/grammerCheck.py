#!/usr/bin/env python

import sys
import re
import json
import requests
import os
import openai
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Custom sentence tokenizer that doesn't rely on NLTK
def custom_sent_tokenize(text):
    # Define sentence-ending patterns
    # Look for period, question mark, or exclamation mark followed by space and capital letter
    sentence_endings = re.finditer(r'([.!?])\s+([A-Z])', text)

    # Get the indices where sentences end
    end_indices = [match.start(1) for match in sentence_endings]

    # Add the end of the text as the final endpoint
    end_indices.append(len(text))

    # Extract sentences based on the endpoints
    sentences = []
    start_idx = 0

    for end_idx in end_indices:
        # Get the sentence including the ending punctuation
        sentence = text[start_idx:end_idx+1].strip()

        # Skip empty sentences
        if sentence:
            sentences.append(sentence)

        # Update the start index for the next sentence
        start_idx = end_idx + 1

    # If no sentences were found, return the original text as a single sentence
    if not sentences:
        return [text]

    return sentences

def correct_sentence(sentence, model="gpt-4o-mini"):
    """Send sentence to OpenAI for correction and return result"""
    # Skip correction for empty lines or whitespace-only strings
    if not sentence.strip():
        return sentence

    # Use unique tokens to bracket the sentence
    start_token = "<!@#>"
    end_token = "<#@!>"

    # Set up OpenAI client
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = """
I will provide a single sentence in markdown format enclosed between two special tokens:

Start token: <!@#>
End token: <#@!>
Your task is to correct only punctuation and spelling mistakes while strictly following these rules:
DO NOT add or remove periods "." as this is a complete sentence already.
DO NOT alter hyphenated words, for example: "5,000-year-old" or "in-depth", 'well-known' or "I-Ching" MUST NOT be changed.
DO NOT alter Markdown syntax (e.g., # Headings, **bold**, *italics*, [links](url), - lists, etc.).
DO NOT break hyphens in compound words, for example: "5,000-year-old" or "in-depth", 'well-known' or "I-Ching" MUST NOT be changed.
DO NOT modify or reformat new lines—preserve them exactly as they appear.
IGNORE any content inside HTML tags (<tag>...</tag>) and do not modify it.
IGNORE any content inside LaTeX math expressions ($...$ or \[...\]) and do not modify it.
DO NOT change code blocks (``` code ```) or inline code (\code``)—leave them untouched.
DO NOT change capitalization or phrasing unless it is required to fix a spelling or punctuation mistake.
DO NOT add periods before or after markdown formatting like *text* or **text**.
DO NOT add periods after colons (:).
DO NOT add periods before or after special characters like *, <, ~, $, #, -, _, `.
Return only the corrected Markdown text between the special tokens (<!@#> and <#@!>) without adding anything extra.

Here is the Markdown document:
"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that corrects spelling, grammar, and punctuation errors."},
                {"role": "user", "content": (
                    f"{prompt}\n{start_token}\n{sentence}\n{end_token}"
                )}
            ],
            temperature=0.0,
            max_tokens=1024
        )

        # Extract the corrected sentence from the response
        corrected = response.choices[0].message.content.strip()
        corrected = re.search(f"{start_token}(.*?){end_token}", corrected, re.DOTALL)
        if corrected:
            corrected = corrected.group(1).strip()
        else:
            corrected = sentence  # Fallback to original if extraction fails

        return corrected
    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        return sentence  # Return original sentence if API call fails

def process_markdown(input_file, output_file):
    """Process markdown file and write corrected content to output file as we go"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {input_file}: {e}", file=sys.stderr)
        sys.exit(1)

    # Remove <think> and </think> tags
    content = re.sub(r'</?think>', '', content)

    # Print the content for debugging
    # print("DEBUG: Original content:", file=sys.stderr)
    lines = content.split('\n')
    # for i, line in enumerate(lines):
    #     print(f"DEBUG: Line {i+1}: {repr(line)}", file=sys.stderr)

    # Pre-process to join hyphenated words that might be split across lines
    processed_lines = []
    i = 0
    while i < len(lines):
        current_line = lines[i]
        # If this line ends with a hyphen and there's a next line
        if i < len(lines) - 1 and current_line.strip().endswith('-'):
            # Check if it's a hyphenated word (no space before the hyphen)
            if re.search(r'\S-$', current_line.strip()):
                # Combine with the next line
                next_line = lines[i+1]
                # Remove leading whitespace from the next line
                next_line = next_line.lstrip()
                # Combine the lines
                combined_line = current_line.rstrip('-') + next_line
                processed_lines.append(combined_line)
                # print(f"DEBUG: Combined lines {i+1} and {i+2}: {repr(combined_line)}", file=sys.stderr)
                i += 2  # Skip the next line since we've combined it
            else:
                processed_lines.append(current_line)
                i += 1
        else:
            processed_lines.append(current_line)
            i += 1

    # Print the processed lines for debugging
    print("DEBUG: Processed lines:", file=sys.stderr)
    for i, line in enumerate(processed_lines):
        print(f"DEBUG: Line {i+1}: {repr(line)}", file=sys.stderr)

    # Process the content line by line to preserve newlines
    lines = processed_lines

    # Open output file for writing
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            total_sentences = 0
            current_paragraph = []

            for i, line in enumerate(lines):
                # Strip leading spaces from the line
                line = line.lstrip()

                # If it's an empty line, write out the current paragraph and reset
                if not line.strip():
                    if current_paragraph:
                        paragraph_text = '\n'.join(current_paragraph)
                        # print(f"DEBUG: Processing paragraph: {repr(paragraph_text)}", file=sys.stderr)
                        total_sentences = process_paragraph(paragraph_text, f, total_sentences)
                        current_paragraph = []
                    f.write('\n')
                    f.flush()
                    continue

                # Check if this line should be preserved as-is
                if (line.startswith('```') or
                    line.startswith('>') or
                    line.startswith('#') or
                    line.startswith('<') or
                    line.startswith('*') or
                    line.startswith('_') or
                    line.startswith('~') or
                    line.startswith('`') or
                    line.startswith('-')):

                    # Process any accumulated paragraph text
                    if current_paragraph:
                        paragraph_text = '\n'.join(current_paragraph)
                        # print(f"DEBUG: Processing paragraph: {repr(paragraph_text)}", file=sys.stderr)
                        total_sentences = process_paragraph(paragraph_text, f, total_sentences)
                        current_paragraph = []

                    # Write the preserved line directly
                    f.write(line + '\n')
                    f.flush()
                else:
                    # Add to current paragraph
                    current_paragraph.append(line)

            # Process any remaining paragraph text
            if current_paragraph:
                paragraph_text = '\n'.join(current_paragraph)
                # print(f"DEBUG: Processing paragraph: {repr(paragraph_text)}", file=sys.stderr)
                total_sentences = process_paragraph(paragraph_text, f, total_sentences)

    except Exception as e:
        print(f"Error writing to {output_file}: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

def process_paragraph(paragraph, output_file, total_sentences):
    """Process a single paragraph of text"""
    # Skip empty paragraphs
    if not paragraph.strip():
        return total_sentences

    # Print the paragraph for debugging
    # print(f"DEBUG: Processing paragraph in process_paragraph: {repr(paragraph)}", file=sys.stderr)

    # Process the entire paragraph as a single unit
    total_sentences += 1
    print(f"{total_sentences:03d}...", file=sys.stderr, flush=True)


    corrected = correct_sentence(paragraph)

    # Print the corrected paragraph in green if it was changed
    if corrected != paragraph:
        # Always print the input paragraph in yellow
        print("[INP]"+Fore.YELLOW + paragraph, flush=True)

        print("[COR]"+Fore.GREEN + corrected, flush=True)

    # Write the corrected paragraph to the output file
    output_file.write(corrected + '\n')
    output_file.flush()
    return total_sentences

def main():
    # Check if input file was provided
    if len(sys.argv) < 2:
        print("Usage: grammerCheck.py <input_markdown_file>", file=sys.stderr, flush=True)
        sys.exit(1)

    # Check if OpenAI API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set", file=sys.stderr, flush=True)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "clean.md"

    # Process the file and write to output as we go
    process_markdown(input_file, output_file)

    print(f"Completed writing corrected content to {output_file}", file=sys.stderr, flush=True)

if __name__ == "__main__":
    main()
