# funcs_lib.py

## Common Functions Library

### Description
A collection of utility functions for making API calls to various AI providers and handling common tasks across the I Ching CLI tools.

### Functions
`call_ai_api(prompt, system_message, model, provider) -> str`  
Makes API calls to various AI providers (OpenAI, Google, Anthropic, Grok) and returns the response text.

### Usage
```python
from funcs_lib import call_ai_api

response = call_ai_api(
    prompt="Your prompt here",
    system_message="System context here",
    model="gpt-4",
    provider="openai"
)
```

### Supported Providers
- **OpenAI** (`provider="openai"`)  
  Models: gpt-4, gpt-3.5-turbo, etc.  
  Requires: `OPENAI_API_KEY` environment variable

- **Google** (`provider="google"`)  
  Models: gemini-pro, etc.  
  Requires: `GOOGLE_API_KEY` environment variable

- **Anthropic** (`provider="anthropic"`)  
  Models: claude-3, etc.  
  Requires: `ANTHROPIC_API_KEY` environment variable

- **Grok** (`provider="grok"`) [Not yet implemented]  
  Requires: `GROK_API_KEY` environment variable

### Dependencies
- openai
- google-cloud-aiplatform
- anthropic
- colorama
- python-dotenv (recommended for API key management)

*Last Updated:* 10-21-2023 15:00

---

