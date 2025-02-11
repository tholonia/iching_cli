#!/bin/bash

# Loop from 1 to 64
for i in $(seq -f "%02g" 2 64); do
    # Execute the command with the current number
    ./regen_lines_in_history.py ../regen $i
done
