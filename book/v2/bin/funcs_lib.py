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


def get_model_for_provider(provider):
    """Return the appropriate model name for the given provider."""
    provider_models = {
        'openai': 'gpt-4o',
        'grok': 'grok-beta',
        'anthropic': 'claude-3.5-sonnet',
        'google': 'gemini-1.5-pro'
    }
    return provider_models.get(provider, 'gpt-4o')  # default to gpt-4o if provider not found

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

    if provider == "openai":
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
    # elif provider == "XXXX":
    #     if not os.getenv("XXXX_API_KEY"):
    #         print(Fore.RED + "Error: XXXX_API_KEY environment variable is required" + Style.RESET_ALL)
    #         print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
    #         sys.exit(1)

    #     GROK_API_KEY = os.getenv("GROK_API_KEY")
    #     url = "https://api.x.ai/v1/chat/completions"  # Updated to correct URL

    #     headers = {
    #         "Authorization": f"Bearer {GROK_API_KEY}",
    #         "Content-Type": "application/json"
    #     }

    #     data = {
    #         'model': model,
    #         'messages': [
    #             {'role': 'system', 'content': system_message},
    #             {'role': 'user', 'content': prompt}
    #         ],
    #         'temperature': 0.7
    #     }

    #     try:
    #         response = requests.post(url, headers=headers, data=json.dumps(data))
    #         response.raise_for_status()

    #         # Parse the JSON response
    #         result = response.json()
    #         pprint(result)  # Keep this for debugging

    #         # Extract the content from the response
    #         if 'choices' in result and len(result['choices']) > 0:
    #             content = result['choices'][0]['message']['content'].strip()
    #             if not content:
    #                 raise Exception("Empty response from Grok API")
    #             return content
    #         else:
    #             raise Exception("Invalid response structure from Grok API")

    #     except requests.exceptions.RequestException as e:
    #         print(Fore.RED + f"Error calling Grok API: {e}" + Style.RESET_ALL)
    #         print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
    #         raise
    #     except Exception as e:
    #         print(Fore.RED + f"Error processing Grok response: {e}" + Style.RESET_ALL)
    #         print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
    #         raise

    else:
        print(Fore.RED + f"Unsupported provider: {provider}" + Style.RESET_ALL)
        print(Fore.RED + traceback.format_exc() + Style.RESET_ALL)
        raise ValueError(f"Unsupported provider: {provider}")

def clean_response(res):
    """
    Clean response text by removing markdown and JSON code block markers.

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

    # Remove leading markdown/json markers
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