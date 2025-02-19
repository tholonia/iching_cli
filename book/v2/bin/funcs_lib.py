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

Usage:
    from funcs_lib import call_ai_api

    response = call_ai_api(
        prompt="Your prompt here",
        system_message="System context here",
        model="gpt-4",
        provider="openai"
    )

Supported Providers:
    - OpenAI (provider="openai")
        Models: gpt-4, gpt-3.5-turbo, etc.
        Requires: OPENAI_API_KEY environment variable

    - Google (provider="google")
        Models: gemini-pro, etc.
        Requires: GOOGLE_API_KEY environment variable

    - Anthropic (provider="anthropic")
        Models: claude-3, etc.
        Requires: ANTHROPIC_API_KEY environment variable

    - Grok (provider="grok") [Not yet implemented]
        Requires: GROK_API_KEY environment variable

Dependencies:
    - openai
    - google-cloud-aiplatform
    - anthropic
    - colorama
    - python-dotenv (recommended for API key management)

Author: JW
Last Updated: 2024
=============================================================================
"""

import os
import sys
from openai import OpenAI
from colorama import Fore, Style

def call_ai_api(prompt, system_message="You are an expert assistant.", model="gpt-4o", provider="openai"):
    """
    Make an AI API call to various providers and return the response.

    Args:
        prompt (str): The user prompt to send
        system_message (str): The system context message
        model (str): The AI model to use
        provider (str): AI provider to use ('openai', 'google', 'anthropic', 'grok')

    Returns:
        str: The response content

    Raises:
        Exception: If API call fails or provider is not supported
    """

    if provider == "openai":
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not os.getenv("OPENAI_API_KEY"):
            print(Fore.RED + "Error: OPENAI_API_KEY environment variable is required" + Style.RESET_ALL)
            sys.exit(1)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
            return clean_response(response.choices[0].message.content.strip())

        except Exception as e:
            print(Fore.RED + f"Error calling OpenAI API: {e}" + Style.RESET_ALL)
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
        if not os.getenv("GROK_API_KEY"):
            print(Fore.RED + "Error: GROK_API_KEY environment variable is required" + Style.RESET_ALL)
            sys.exit(1)

        try:
            # Placeholder for Grok API implementation
            # Update when API becomes available
            raise NotImplementedError("Grok API not yet implemented")

        except Exception as e:
            print(Fore.RED + f"Error calling Grok API: {e}" + Style.RESET_ALL)
            raise

    else:
        raise ValueError(f"Unsupported AI provider: {provider}")

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