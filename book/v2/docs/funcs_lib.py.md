# funcs_lib.py

## Common Functions Library

### Description
A collection of utility functions for making API calls to various AI providers and handling common tasks across the I Ching CLI tools.

### Functions
- `call_ai_api(prompt, system_message, model, provider) -> str`  
  Makes API calls to various AI providers (OpenAI, Google, Anthropic, Grok) and returns the response text.

- `clean_response(res) -> str`  
  Cleans response text by removing markdown and code block markers.

- `get_model_for_provider(provider) -> str`  
  Returns the appropriate model name for the given provider.

### Usage
```python
from funcs_lib import call_ai_api, clean_response

response = call_ai_api(
    prompt="Your prompt here",
    system_message="System context here",
    model="gpt-4",
    provider="openai"
)
```

### Supported Providers
- **OpenAI (provider="openai")**  
  Models: gpt-4o  
  Requires: `OPENAI_API_KEY` environment variable

- **Google (provider="google")**  
  Models: gemini-pro  
  Requires: `GOOGLE_API_KEY` environment variable

- **Anthropic (provider="anthropic")**  
  Models: claude-3.5-sonnet  
  Requires: `ANTHROPIC_API_KEY` environment variable

- **Grok (provider="grok")**  
  Models: grok-beta  
  Requires: `GROK_API_KEY` environment variable

### Dependencies
- openai
- google-cloud-aiplatform
- anthropic
- colorama
- requests
- json

### Error Handling
- Validates required environment variables
- Handles API-specific errors and exceptions
- Returns clean, formatted error messages
- Includes traceback for debugging

*Author: JW*  
*Last Updated:* 03-01-2024 00:00

---

