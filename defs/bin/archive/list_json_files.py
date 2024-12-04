import os
import glob

directory = "/home/jw/src/iching_cli/defs/alls/out/update1"
json_files = glob.glob(os.path.join(directory, "*.json"))

for file in sorted(json_files):
    print(file)