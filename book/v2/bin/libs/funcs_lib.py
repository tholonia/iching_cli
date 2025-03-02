"""
=============================================================================
funcs_lib.py - Common Functions Library
=============================================================================

Description:
    A collection of utility functions for making API calls to various AI providers
    and handling common tasks across the I Ching CLI tools.

Functions:
    call_ai_api(prompt, system_message, model, provider) -> str
        Makes API calls to various AI providers (OpenAI, Google, Anthropic, Grok)
        and returns the response text.

    clean_response(res) -> str
        Cleans response text by removing markdown and code block markers.

    get_model_for_provider(provider) -> str
        Returns the appropriate model name for the given provider.

Usage:
    from funcs_lib import call_ai_api, clean_response

    response = call_ai_api(
        prompt="Your prompt here",
        system_message="System context here",
        model="gpt-4",
        provider="openai"
    )

Supported Providers:
    - OpenAI (provider="openai")
        Models: gpt-4o
        Requires: OPENAI_API_KEY environment variable

    - Google (provider="google")
        Models: gemini-pro
        Requires: GOOGLE_API_KEY environment variable

    - Anthropic (provider="anthropic")
        Models: claude-3.5-sonnet
        Requires: ANTHROPIC_API_KEY environment variable

    - Grok (provider="grok")
        Models: grok-beta
        Requires: GROK_API_KEY environment variable

Dependencies:
    - openai
    - google-cloud-aiplatform
    - anthropic
    - colorama
    - requests
    - json

Error Handling:
    - Validates required environment variables
    - Handles API-specific errors and exceptions
    - Returns clean, formatted error messages
    - Includes traceback for debugging

Author: JW
Last Updated: 2024-03
=============================================================================
"""

import os
import sys
from openai import OpenAI
from colorama import Fore, Style
import requests
import json
from pprint import pprint
import traceback
import argparse
from vertexai.language_models import ChatModel
import re
from dotenv import load_dotenv

load_dotenv()

wen_values = {
    1: [1, 63, "111111", 6],
    2: [2, 0, "000000", 0],
    3: [3, 17, "010001", 2],
    4: [4, 34, "100010", 2],
    5: [5, 23, "010111", 4],
    6: [6, 58, "111010", 4],
    7: [7, 2, "000010", 2],
    8: [8, 16, "010000", 1],
    9: [9, 55, "110111", 5],
    10: [10, 59, "111011", 5],
    11: [11, 7, "000111", 3],
    12: [12, 56, "111000", 3],
    13: [13, 61, "111101", 5],
    14: [14, 47, "101111", 5],
    15: [15, 4, "000100", 1],
    16: [16, 8, "001000", 1],
    17: [17, 25, "011001", 3],
    18: [18, 38, "100110", 3],
    19: [19, 3, "000011", 2],
    20: [20, 48, "110000", 2],
    21: [21, 41, "101001", 3],
    22: [22, 37, "100101", 3],
    23: [23, 32, "100000", 1],
    24: [24, 1, "000001", 1],
    25: [25, 57, "111001", 4],
    26: [26, 39, "100111", 4],
    27: [27, 33, "100001", 2],
    28: [28, 30, "011110", 4],
    29: [29, 18, "010010", 2],
    30: [30, 45, "101101", 4],
    31: [31, 28, "011100", 3],
    32: [32, 14, "001110", 3],
    33: [33, 60, "111100", 4],
    34: [34, 15, "001111", 4],
    35: [35, 40, "101000", 2],
    36: [36, 5, "000101", 2],
    37: [37, 53, "110101", 4],
    38: [38, 43, "101011", 4],
    39: [39, 20, "010100", 2],
    40: [40, 10, "001010", 2],
    41: [41, 35, "100011", 3],
    42: [42, 49, "110001", 3],
    43: [43, 31, "011111", 5],
    44: [44, 62, "111110", 5],
    45: [45, 24, "011000", 2],
    46: [46, 6, "000110", 2],
    47: [47, 26, "011010", 3],
    48: [48, 22, "010110", 3],
    49: [49, 29, "011101", 4],
    50: [50, 46, "101110", 4],
    51: [51, 9, "001001", 2],
    52: [52, 36, "100100", 2],
    53: [53, 52, "110100", 3],
    54: [54, 11, "001011", 3],
    55: [55, 13, "001101", 3],
    56: [56, 44, "101100", 3],
    57: [57, 54, "110110", 4],
    58: [58, 27, "011011", 4],
    59: [59, 50, "110010", 3],
    60: [60, 19, "010011", 3],
    61: [61, 51, "110011", 4],
    62: [62, 12, "001100", 2],
    63: [63, 21, "010101", 3],
    64: [64, 42, "101010", 3]
}

def get_model_for_provider(provider):
    """Return the appropriate model name for the given provider."""
    provider_models = {
        'openai': 'gpt-4o',
        'grok': 'grok-beta',
        'anthropic': 'claude-3.5-sonnet',
        'google': 'gemini-1.5-pro',
        # 'perplexity': 'sonar-reasoning-pro'  # gets a bit too 'out there' when writing storiesUpdated model name
        # 'perplexity': 'sonar-reasoning'
        # 'perplexity': 'sonar-pro'
        'perplexity': 'sonar'
    }
    return provider_models.get(provider, 'gpt-4o')

def call_ai_api(prompt, system_message="You are an expert assistant.", model=None, provider="openai"):
    """
    Make an AI API call to various providers and return the response.

    Args:
        prompt (str): The user prompt to send
        system_message (str): The system context message
        model (str): Optional - will be determined by provider if not specified
        provider (str): AI provider to use ('openai', 'google', 'anthropic', 'grok')

    Returns:
        str: The response content

    Raises:
        Exception: If API call fails or provider is not supported
    """
    # Get the appropriate model for the provider if not specified
    model = model or get_model_for_provider(provider)
    API_KEY = os.getenv("OPENAI_API_KEY")
    if provider == "openai":
        # Initialize the OpenAI client
        client = OpenAI(api_key=API_KEY)

        if not os.getenv("OPENAI_API_KEY"):
            print(Fore.RED + "Error: OPENAI_API_KEY environment variable is required" + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            sys.exit(1)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract the content and ensure it's not empty
            content = response.choices[0].message.content.strip()
            if not content:
                raise Exception("Empty response from OpenAI API")
            return clean_response(content)

        except Exception as e:
            print(Fore.RED + f"Error calling OpenAI API: {e}" + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            raise

    elif provider == "google":
        if not os.getenv("GOOGLE_API_KEY"):
            print(Fore.RED + "Error: GOOGLE_API_KEY environment variable is required" + Style.RESET_ALL)
            sys.exit(1)

        try:
            # Import Google API client
            from vertexai.language_models import ChatModel

            chat_model = ChatModel.from_pretrained(model)
            response = chat_model.predict(prompt, temperature=0.7)
            return response.text

        except Exception as e:
            print(Fore.RED + f"Error calling Google API: {e}" + Style.RESET_ALL)
            raise

    elif provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            print(Fore.RED + "Error: ANTHROPIC_API_KEY environment variable is required" + Style.RESET_ALL)
            sys.exit(1)

        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            response = client.messages.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content

        except Exception as e:
            print(Fore.RED + f"Error calling Anthropic API: {e}" + Style.RESET_ALL)
            raise

    elif provider == "grok":
        # Replace 'YOUR_API_KEY' with your actual xAI API key
        GROK_API_KEY = os.getenv('GROK_API_KEY')

        # Define the API endpoint
        url = 'https://api.x.ai/v1/chat/completions'

        # Set up the headers with the API key
        headers = {
            'Authorization': f'Bearer {GROK_API_KEY}',
            'Content-Type': 'application/json'
        }

        # Define the prompt and other parameters
        data = {
            'model': model,  # Specify the model you want to use
            'messages': [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.7  # Adjust the creativity of the response
        }

        # Send the POST request
        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))

            # Check if the request was successful
            if response.status_code == 200:
                result = response.json()
                # Extract and print the assistant's reply
                reply = result['choices'][0]['message']['content']
                content = clean_response(reply)
                return content
            else:
                print(f'Error: {response.status_code}')
                print(response.text)
        except Exception as e:
            print(Fore.RED + f"Error calling OpenAI API: {e}" + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            raise

    elif provider == "perplexity" or provider == "ppx":
        if not os.getenv("PERPLEXITY_API_KEY"):
            print(Fore.RED + "Error (e01): PERPLEXITY_API_KEY environment variable is required" + Style.RESET_ALL)
            sys.exit(1)

        try:
            url = "https://api.perplexity.ai/chat/completions"
            headers = {
                "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            # Enhanced system message with explicit JSON and formatting instructions
            enhanced_system_message = (
                f"{system_message} "
                "Provide direct responses without explaining your thinking process. "
                "Format your response as valid JSON with these requirements:\n"
                "1. All string values MUST be enclosed in double quotes\n"
                "2. No trailing commas\n"
                "3. All property names must be in double quotes\n"
                "4. All newlines in text must be escaped as \\n\n"
                "5. Ensure all JSON syntax is strictly valid\n"
                "6. For the 'short_story' field:\n"
                "   - Format text in proper paragraphs\n"
                "   - Only use newlines between paragraphs\n"
                "   - Do not split sentences across lines\n"
                "   - Keep dialogue and action in the same paragraph\n"
                "Do not include any explanation or commentary outside the JSON."
            )

            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": enhanced_system_message},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 4096,
                "stream": False,
                "top_p": 1.0,
                "top_k": 50
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code != 200:
                print(Fore.RED + f"Error (e02): API Error Response: {response.text}" + Style.RESET_ALL)
                response.raise_for_status()

            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content'].strip()
                if not content:
                    raise Exception("Error (e03): Empty response from Perplexity API")

                # Try to fix common JSON formatting issues
                content = content.replace('": ', '":')  # Remove space after colons
                content = content.replace(', }', '}')   # Remove trailing commas
                content = content.replace(',}', '}')    # Remove trailing commas
                content = content.replace('",\n  }', '"\n  }')  # Remove trailing commas

                # Escape newlines in string values
                def escape_string_newlines(match):
                    key = match.group(1).strip('"')  # Get the key name without quotes
                    value = match.group(2)  # Get the value

                    # # Special handling for short_story field
                    # if key == "short_story":
                    #     # First, join all content into a single line
                    #     value = re.sub(r'\s*\n\s*', ' ', value)

                    #     # Split into sentences
                    #     sentences = re.split(r'([.!?])\s+', value)

                    #     # Rebuild paragraphs
                    #     paragraphs = []
                    #     current_para = []

                    #     for i in range(0, len(sentences)-1, 2):
                    #         sentence = sentences[i].strip()
                    #         ending = sentences[i+1] if i+1 < len(sentences) else '.'

                    #         if sentence:
                    #             current_para.append(sentence + ending + ' ')

                    #         # Start new paragraph on strong narrative breaks
                    #         if ending in '.!?' and len(current_para) >= 2:
                    #             paragraphs.append(''.join(current_para).strip())
                    #             current_para = []

                    #     # Add any remaining sentences
                    #     if current_para:
                    #         paragraphs.append(''.join(current_para).strip())

                    #     # Join paragraphs with double newlines
                    #     value = '\n\n'.join(paragraphs)

                    # Process newlines and sentence endings
                    escaped = value.replace('\n', '\\n')
                    escaped = ensure_sentence_endings(escaped, key)

                    return f'"{key}": "{escaped}"'

                # Match both key and value in JSON, including short_story
                content = re.sub(r'("(?:meaning|changing|short_story)")\s*:\s*"([^"]*)"',
                               escape_string_newlines, content)

                return clean_response(content)
            else:
                raise Exception("Error (e04): Invalid response structure from Perplexity API")

        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"Error (e05): Error calling Perplexity API: {e}" + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            raise
        except Exception as e:
            print(Fore.RED + f"Error (e06): Error processing Perplexity response: {e}" + Style.RESET_ALL)
            print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
            raise

    else:
        print(Fore.RED + f"Error (e07): Unsupported provider: {provider}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        raise ValueError(f"Error (e07): Unsupported provider: {provider}")

def clean_response(res):
    """
    Clean response text by removing markdown and JSON code block markers.
    First attempts to extract content between ```json and ``` markers.
    If that fails, falls back to general cleaning.

    Args:
        res (str): The response text to clean

    Returns:
        str: Cleaned response text with code block markers removed

    Example:
        >>> text = '''```json
        ... {"key": "value"}
        ... ```'''
        >>> clean_response(text)
        '{"key": "value"}'
    """
    if not isinstance(res, str):
        return res

    # First try to extract content between ```json and ``` markers
    json_pattern = r"```json\n(.*?)```"
    matches = re.findall(json_pattern, res, re.DOTALL)
    if matches:
        return matches[0].strip()

    try:
        # If no JSON block found, proceed with general cleaning
        lines = res.split('\n')
        if lines and lines[0].startswith('```'):
            lines = lines[1:]

        # Remove trailing markers
        if lines and lines[-1].strip() == '```':
            lines = lines[:-1]

        # Rejoin and strip whitespace
        cleaned = '\n'.join(lines).strip()

        # Remove code block markers from start/end only
        if cleaned.startswith('```markdown'):
            cleaned = cleaned[11:]
        elif cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]

        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]

        return cleaned.strip()
    except Exception as e:
        print(Fore.RED + f"Error (e08): Error cleaning response: {e}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        raise

def ensure_sentence_endings(text, key=None):

    """
    Ensure each sentence in the text ends with a period.
    Only processes text for specified keys.

    Args:
        text (str): The text to process
        key (str): The JSON key being processed. If None, skips processing.
    """
    try:
        # Only process text for specific keys
        if key not in ["meaning", "changing"]:
            return text

        if not text:
            return text

        # Split on common sentence endings while preserving them
        sentences = re.split(r'([.!?])\s*', text)

        # Recombine sentences, ensuring each ends with a period
        result = []
        for i in range(0, len(sentences)-1, 2):
            sentence = sentences[i].strip()
            ending = sentences[i+1] if i+1 < len(sentences) else '.'
            if sentence:
                result.append(sentence + ending)

        # Handle the last sentence if it doesn't end with punctuation
        if sentences[-1].strip():
            result.append(sentences[-1].strip() + '.')

        return ' '.join(result)
    except Exception as e:
        print(Fore.RED + f"Error (e09): Error ensuring sentence endings: {e}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        raise

def get_json_version(f):
    """
    Read version string from includes/VER_JSON.txt file.
    Returns empty string if file is empty or doesn't exist.
    Skips lines that begin with #.
    """
    try:
        with open(f, 'r', encoding='utf-8') as f:
            # Read all non-comment lines into a list
            lines = [line.strip() for line in f.readlines() if not line.strip().startswith('#')]
            return lines[0] if lines else ""
    except (FileNotFoundError, IOError):
        return ""


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

