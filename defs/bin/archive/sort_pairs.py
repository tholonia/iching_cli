import json

# Read the current file
with open('pairs.json', 'r') as f:
    data = json.load(f)

# Sort the keys numerically
sorted_data = dict(sorted(data.items(), key=lambda x: int(x[0])))

# Write back to file with pretty printing
with open('pairs.json', 'w') as f:
    json.dump(sorted_data, f, indent=4)