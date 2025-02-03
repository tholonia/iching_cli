#!/bin/bash

# Loop from 24 to 64
for i in $(seq -f "%02g" 24 64); do
    # Execute the command with the current number
    ./get_new_image_desc.py "$i"
done
