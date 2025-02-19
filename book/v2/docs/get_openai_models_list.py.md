Below is the markdown format of the provided docstring:

```markdown
# get_openai_models_list.py

## OpenAI Models List Generator

### Description
This script retrieves and displays a list of all available OpenAI models with their creation dates. The output is sorted chronologically, making it easy to see the evolution of available models.

### Usage
```bash
python get_openai_models_list.py
```

### Output Format
```
(creation_date, model_id)
```
Example: `('2023-12-01 12:00:00', 'gpt-4-1106-preview')`

### Process
1. Connects to OpenAI API using provided credentials
2. Retrieves complete list of available models
3. Converts Unix timestamps to readable dates
4. Sorts models by creation date
5. Displays formatted results

### Dependencies
- OpenAI Python package (v1.0.0 or later)
- Valid OpenAI API key set in OPENAI_API_KEY environment variable

### Environment Variables
OPENAI_API_KEY: Your OpenAI API key (required)

### Author
JW

*Last Updated:* 10-04-2023 10:00

---

