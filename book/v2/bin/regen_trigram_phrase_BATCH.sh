#!/bin/bash

# Loop from 1 to 64
for i in $(seq -f "%02g" 1 64); do
    # Execute the command with the current number
    ./regen_trigram_phrase.py ../regen $i
done
