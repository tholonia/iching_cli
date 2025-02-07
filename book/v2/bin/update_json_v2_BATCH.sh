#!/bin/bash

# # Loop from 01 to 64
# for i in $(seq -f "%02g" 13 64); do
#     # Execute the command with the current number
#     ./update_json_v2.py "$i"
# done

numbers=(51)
for num in "${numbers[@]}"; do
    echo "./update_json_v2.py $num"
    ./update_json_v2.py $num
done