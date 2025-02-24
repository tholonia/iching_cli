#!/bin/bash

# Check if first argument (hexagram number) exists
if [ -z "$1" ]; then
    echo "Error: Please provide hexagram number as first argument"
    exit 1
fi

# Check if second argument (provider) exists, default to openai if not specified
if [ -z "$2" ]; then
    PROVIDER="openai"
else
    PROVIDER="$2"
fi

./regen_story.py -f ../regen/${1}.json -i 0 --provider ${PROVIDER} --save
./regen_story.py -f ../regen/${1}.json -i 1 --provider ${PROVIDER} --save
./regen_story.py -f ../regen/${1}.json -i 2 --provider ${PROVIDER} --save
