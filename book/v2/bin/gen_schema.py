#!/usr/bin/env python3

"""
=============================================================================
create_schema.py - JSON Schema Generator
=============================================================================

Description:
  This script takes a JSON file as input and generates a JSON schema that
  describes the structure of the input JSON. The schema is saved to
  'schema.json'.

Usage:
  ./create_schema.py <input_json_file>

Example:
  ./create_schema.py data.json

Dependencies:
  - Python 3.x
  - json module (standard library)

Output:
  - schema.json: The generated JSON schema
=============================================================================
"""

import json
import sys
from typing import Any, Dict, List, Union

def infer_type(value: Any) -> Dict[str, Any]:
    """Infer the JSON schema type from a value."""
    if value is None:
        return {"type": "null"}
    elif isinstance(value, bool):
        return {"type": "boolean"}
    elif isinstance(value, int):
        return {"type": "integer"}
    elif isinstance(value, float):
        return {"type": "number"}
    elif isinstance(value, str):
        return {"type": "string"}
    elif isinstance(value, list):
        if not value:  # Empty list
            return {"type": "array", "items": {}}
        # Get schema for all items
        item_schemas = [create_schema(item) for item in value]
        # Combine schemas if they're different
        return {
            "type": "array",
            "items": item_schemas[0] if len(set(str(s) for s in item_schemas)) == 1
                    else {"anyOf": item_schemas}
        }
    elif isinstance(value, dict):
        return create_schema(value)
    else:
        return {"type": "string"}  # Default to string for unknown types

def create_schema(data: Union[Dict, Any]) -> Dict[str, Any]:
    """Create a JSON schema from a data structure."""
    if not isinstance(data, dict):
        return infer_type(data)

    properties = {}
    required = []

    for key, value in data.items():
        properties[key] = infer_type(value)
        if value is not None:  # Consider non-null values as required
            required.append(key)

    schema = {
        "type": "object",
        "properties": properties
    }

    if required:
        schema["required"] = required

    return schema

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Read input JSON file
        with open(input_file, 'r') as f:
            data = json.load(f)

        # Generate schema
        schema = create_schema(data)

        # Add schema version and other metadata
        full_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            **schema
        }

        # Write schema to file
        with open('schema.json', 'w') as f:
            json.dump(full_schema, f, indent=2)

        print(f"Schema has been generated and saved to schema.json")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{input_file}' is not a valid JSON file")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()