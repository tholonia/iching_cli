#!/bin/bash

# Loop from 01 to 64
for i in $(seq -f "%02g" 01 64); do
    # Execute the command with the current number
    ./get_new_hex_desc_OPENAI.py "$i" --save
done
