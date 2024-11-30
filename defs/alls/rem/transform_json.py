#!//bin//env python
import json

def transform_key_elements(data):
    """
    Recursively transform keyElements arrays into numbered objects
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'key_elements' and isinstance(value, list):
                # Transform the array into a numbered object
                data[key] = {str(6-i): item for i, item in enumerate(value)}
            elif isinstance(value, (dict, list)):
                transform_key_elements(value)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                transform_key_elements(item)
    
    return data

def process_file(filename):
    try:
        # Read the JSON file
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Transform the data
        transformed_data = transform_key_elements(data)
        
        # Write back to the same file with proper formatting
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(transformed_data, file, indent=4, ensure_ascii=False)
            
        print(f"Successfully transformed {filename}")
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except json.JSONDecodeError:
        print(f"Error: '{filename}' contains invalid JSON")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <json_file>")
        sys.exit(1)
    
    process_file(sys.argv[1])
