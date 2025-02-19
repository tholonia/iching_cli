#!/bin/bash

# Array of hexagram pairs and their pair numbers


    # "11 12 01"
    # "54 53 02"
    # "55 59 03"
    # "32 42 04"
    # "60 56 05"
    # "63 64 06"
    # "48 21 07"
    # "17 18 08"
    # "47 22 09"
    # "31 41 10"
    # "49 04 11"
    # "34 20 12"

declare -a pairs=(
    "28 27 13"
    "43 23 14"
    "08 14 15"
    "03 50 16"
    "29 30 17"
    "16 09 18"
    "51 57 19"
    "39 38 20"
    "40 37 21"
    "15 10 22"
    "36 06 23"
    "07 13 24"
    "05 35 25"
    "24 44 26"
    "02 01 27"
    "45 26 28"
    "62 61 29"
    "46 25 30"
    "19 33 31"
    "58 52 32"
)

# Loop through the pairs array
for pair in "${pairs[@]}"; do
    # Split each pair into its components
    read -r el1 el2 el3 <<< "$pair"

    # Execute regen_pairings.py with the components
    echo "./regen_pairings.py "$el1" "$el2" "$el3" --save"
    ./regen_pairings.py "$el1" "$el2" "$el3" --save
done

