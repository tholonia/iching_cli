#!/bin/bash

# Loop from 24 to 64
for i in $(seq -f "%02g" 23 64); do
    # Execute the command with the current number
    code /home/jw/src/iching_cli/defs/v2/${i}_hex.txt
done
