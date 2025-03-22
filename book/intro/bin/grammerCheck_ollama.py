#!/usr/bin/env python

import sys
import re
import json
import requests
import nltk
from nltk.tokenize import sent_tokenize
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Download NLTK data for sentence tokenization if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def correct_sentence(sentence, model="deepseek-r1"):
    """Send sentence to Ollama for correction and return result"""
    # Skip correction for empty lines or whitespace-only strings
    if not sentence.strip():
        return sentence

    url = "http://localhost:11434/api/generate"

    # Use unique tokens to bracket the sentence
    start_token = "<!@#>"
    end_token = "<#@!>"

    payload = {
        "model": model,
        "prompt": (
            "Correct only critical spelling, grammar, and punctuation errors in the following sentence. "
            "Preserve the original structure, special characters like *, **, ***, ~, etc., and the case of words in ALL CAPS. "
            "Do not change the following words: tholon, tholonic, holon, parton, NDC. "
            "Return ONLY the corrected sentence between the tokens without any explanations, comments, or additional text:\n\n"
            f"{start_token}{sentence}{end_token}"
        ),
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        result = response.json()
        # Extract the corrected sentence between the tokens
        corrected = result.get("response", "").strip()
        corrected = re.search(f"{start_token}(.*?){end_token}", corrected, re.DOTALL)
        if corrected:
            corrected = corrected.group(1).strip()
        else:
            corrected = sentence  # Fallback to original if extraction fails

        # Ensure the sentence ends with a period if it doesn't already
        if corrected and not corrected.endswith(('.', '!', '?')):
            corrected += '.'

        return corrected
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}", file=sys.stderr)
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

    # Patterns to identify and preserve
    code_block_pattern = r'(```[^\n]*\n[\s\S]*?\n```)'  # Code blocks
    inline_code_pattern = r'(`[^`]+`)'                  # Inline code
    html_tag_pattern = r'(<\/?(?:a|abbr|acronym|b|bdo|big|blockquote|body|br|button|caption|cite|code|col|colgroup|dd|del|dfn|div|dl|dt|em|fieldset|form|h1|h2|h3|h4|h5|h6|head|hr|html|i|img|input|ins|kbd|label|legend|li|link|map|meta|noscript|object|ol|optgroup|option|p|param|pre|q|samp|script|select|small|span|strong|style|sub|sup|table|tbody|td|textarea|tfoot|th|thead|title|tr|tt|ul|var)[^>]*>)'  # Valid HTML tags
    latex_block_pattern = r'(\$\$[\s\S]*?\$\$)'         # Block LaTeX
    latex_inline_pattern = r'(\$[^$]+\$)'               # Inline LaTeX
    link_pattern = r'(\[[^\]]+\]\([^)]+\))'             # Markdown links
    image_pattern = r'(!\[[^\]]*\]\([^)]+\))'           # Markdown images
    heading_pattern = r'(#{1,6} .+)$'                   # Markdown headings
    blockquote_pattern = r'(^>.*$)'                     # Markdown blockquotes (entire line)
    markdown_special_chars_pattern = r'([*~]+)'         # Markdown special characters
    html_comment_pattern = r'(<!--[\s\S]*?-->)'         # HTML comments
    sub_sup_pattern = r'(<sub>[\s\S]*?</sub>|<sup>[\s\S]*?</sup>)'  # Subscript and superscript
    section_break_pattern = r'(^#{1,6}.*$)'             # Section headings

    # Combine all patterns to find special content to preserve
    special_patterns = [
        code_block_pattern, inline_code_pattern,
        html_tag_pattern, latex_block_pattern,
        latex_inline_pattern, link_pattern,
        image_pattern, heading_pattern,
        blockquote_pattern, markdown_special_chars_pattern,
        html_comment_pattern, sub_sup_pattern,
        section_break_pattern
    ]

    preserve_pattern = '|'.join(f'({p})' for p in special_patterns)

    # Process the content line by line to preserve newlines
    lines = content.split('\n')

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
                        process_paragraph(paragraph_text, f, total_sentences)
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
                    line.startswith('`')):

                    # Process any accumulated paragraph text
                    if current_paragraph:
                        paragraph_text = '\n'.join(current_paragraph)
                        process_paragraph(paragraph_text, f, total_sentences)
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
                process_paragraph(paragraph_text, f, total_sentences)

    except Exception as e:
        print(f"Error writing to {output_file}: {e}", file=sys.stderr, flush=True)
        sys.exit(1)

def process_paragraph(paragraph, output_file, total_sentences):
    """Process a single paragraph of text"""
    # Skip empty paragraphs
    if not paragraph.strip():
        return total_sentences

    # Patterns to identify and preserve
    code_block_pattern = r'(```[^\n]*\n[\s\S]*?\n```)'  # Code blocks
    inline_code_pattern = r'(`[^`]+`)'                  # Inline code
    html_tag_pattern = r'(<\/?(?:a|abbr|acronym|b|bdo|big|blockquote|body|br|button|caption|cite|code|col|colgroup|dd|del|dfn|div|dl|dt|em|fieldset|form|h1|h2|h3|h4|h5|h6|head|hr|html|i|img|input|ins|kbd|label|legend|li|link|map|meta|noscript|object|ol|optgroup|option|p|param|pre|q|samp|script|select|small|span|strong|style|sub|sup|table|tbody|td|textarea|tfoot|th|thead|title|tr|tt|ul|var)[^>]*>)'  # Valid HTML tags
    latex_block_pattern = r'(\$\$[\s\S]*?\$\$)'         # Block LaTeX
    latex_inline_pattern = r'(\$[^$]+\$)'               # Inline LaTeX
    link_pattern = r'(\[[^\]]+\]\([^)]+\))'             # Markdown links
    image_pattern = r'(!\[[^\]]*\]\([^)]+\))'           # Markdown images
    heading_pattern = r'(#{1,6} .+)$'                   # Markdown headings
    blockquote_pattern = r'(^>.*$)'                     # Markdown blockquotes (entire line)
    markdown_special_chars_pattern = r'([*~]+)'         # Markdown special characters
    html_comment_pattern = r'(<!--[\s\S]*?-->)'         # HTML comments
    sub_sup_pattern = r'(<sub>[\s\S]*?</sub>|<sup>[\s\S]*?</sup>)'  # Subscript and superscript

    # Combine all patterns to find special content to preserve
    special_patterns = [
        code_block_pattern, inline_code_pattern,
        html_tag_pattern, latex_block_pattern,
        latex_inline_pattern, link_pattern,
        image_pattern, heading_pattern,
        blockquote_pattern, markdown_special_chars_pattern,
        html_comment_pattern, sub_sup_pattern
    ]

    preserve_pattern = '|'.join(f'({p})' for p in special_patterns)

    # Split the paragraph into parts that should be preserved and parts to be corrected
    parts = []
    last_end = 0

    # Find all special parts to preserve
    for match in re.finditer(preserve_pattern, paragraph, re.MULTILINE):
        # Add text before this special part (to be corrected)
        if match.start() > last_end:
            parts.append((paragraph[last_end:match.start()], False))

        # Add the special part (to be preserved)
        parts.append((match.group(0), True))
        last_end = match.end()

    # Add any remaining text after the last special part
    if last_end < len(paragraph):
        parts.append((paragraph[last_end:], False))

    # Process each part
    for part_text, preserve in parts:
        if preserve or not part_text.strip():
            # Write preserved parts directly
            output_file.write(part_text)
        else:
            # Process regular text by sentences
            sentences = sent_tokenize(part_text)
            corrected_sentences = []

            for i, sentence in enumerate(sentences):
                total_sentences += 1
                print(f"{total_sentences:03d}...", file=sys.stderr, flush=True)
                corrected = correct_sentence(sentence)
                corrected_sentences.append(corrected)

                # Print the sentence in red if it was corrected
                if corrected != sentence:
                    print(Fore.RED + sentence, flush=True)
                    print(Fore.GREEN + corrected, flush=True)
                else:
                    print(Fore.YELLOW + sentence, flush=True)

            # Join the corrected sentences with spaces
            corrected_text = ' '.join(corrected_sentences)
            output_file.write(corrected_text)

    output_file.write('\n')
    output_file.flush()
    return total_sentences

def main():
    # Check if input file was provided
    if len(sys.argv) < 2:
        print("Usage: grammerCheck.py <input_markdown_file>", file=sys.stderr, flush=True)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "clean.md"

    # Process the file and write to output as we go
    process_markdown(input_file, output_file)

    print(f"Completed writing corrected content to {output_file}", file=sys.stderr, flush=True)

if __name__ == "__main__":
    main()
