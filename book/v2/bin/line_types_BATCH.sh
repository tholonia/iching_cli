#!/bin/bash

# Loop from 24 to 64
for i in $(seq -f "%02g" 1 64); do
    # Execute the command with the current number
    ./line_types.py ../regen/${i}.json --save
done
