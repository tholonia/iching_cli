

# execute_pair_workflow.py

## ComfyUI Workflow Executor

### Description
This script executes a generated ComfyUI workflow for image pair blending. It connects to a local ComfyUI server, queues the workflow, and monitors its execution progress.

### Usage
```bash
./execute_pair_workflow.py <workflow.json>
```

### Arguments
- `workflow.json`  
  JSON workflow file to execute

### Dependencies
- Python 3.x
- requests
- websocket-client
- json

### Output
- Status updates during execution
- Generated image in ComfyUI output directory

### Example
```bash
./execute_pair_workflow.py workflow.json
```

### Author
JW

*Last Updated:* 10-04-2023 11:59

---

# funcs_lib.py

## Common Functions Library

### Description
A collection of utility functions for making API calls to various AI providers and handling common tasks across the I Ching CLI tools.

### Functions
#### `call_ai_api(prompt, system_message, model, provider) -> str`
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
- **OpenAI (provider="openai")**
  - Models: gpt-4, gpt-3.5-turbo, etc.
  - Requires: OPENAI_API_KEY environment variable

- **Google (provider="google")**
  - Models: gemini-pro, etc.
  - Requires: GOOGLE_API_KEY environment variable

- **Anthropic (provider="anthropic")**
  - Models: claude-3, etc.
  - Requires: ANTHROPIC_API_KEY environment variable

- **Grok (provider="grok") [Not yet implemented]**
  - Requires: GROK_API_KEY environment variable

### Dependencies
- openai
- google-cloud-aiplatform
- anthropic
- colorama
- python-dotenv (recommended for API key management)

*Last Updated:* 01-01-2024 12:00

---

# gen_pair_images.py

## ComfyUI Image Pair Blending Workflow Generator

### Description
This script generates and optionally executes a ComfyUI workflow that blends two input images using a VAE-based latent space blending technique.

### Usage
```bash
./gen_pair_images.py <image1> <image2> [options]
```
Batch with:
```bash
cat ../includes/pairs.csv \
| awk -F "," '{printf "./gen_pair_images.py %02d.png %02d.png --prefix %02d --execute --queue\n", $2, $3, $1}' |tail -32 > x.sh
```

### Arguments
- `image1`: First input image filename
- `image2`: Second input image filename
- `--prefix PREFIX`: Prefix for output filename (default: p06)
- `--output OUTPUT`: Output JSON filename (default: workflow.json)
- `--server SERVER`: ComfyUI server URL (default: http://localhost:8188)
- `--execute`: Execute the workflow after generation
- `--queue`: Queue the workflow to ComfyUI server (deprecated, use --execute)

### Dependencies
- Python 3.x
- requests
- websocket-client
- uuid
- json
- argparse
- random

### Output
- JSON workflow file
- Generated image with specified prefix (when executed)

### Example
```bash
./gen_pair_images.py image1.png image2.png --prefix blend01 --execute
```

*Last Updated:* 01-01-2024 00:00

---

