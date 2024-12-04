import os
import glob

def get_json_files():
    """
    Get all JSON files from the specified directory.

    Returns:
        list: List of paths to JSON files in the directory
    """
    directory = "/home/jw/src/iching_cli/defs/alls/out/update1"
    json_files = glob.glob(os.path.join(directory, "*.json"))
    return sorted(json_files)

# Example usage:
if __name__ == "__main__":
    files = get_json_files()
    for file in files:
        print(file)