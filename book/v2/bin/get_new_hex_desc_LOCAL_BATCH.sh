#!/bin/bash

# Loop from 1 to 64
for i in $(seq -f "%02g" 1 64); do
    # Execute the command with the current number
    ./get_new_hex_desc_LOCAL.py "$i" --save
done
