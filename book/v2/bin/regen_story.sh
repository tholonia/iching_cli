#!/bin/bash


H=$1
./regen_story.py -f ../regen/$H.json -i 0 --save
./regen_story.py -f ../regen/$H.json -i 1 --save
./regen_story.py -f ../regen/$H.json -i 2 --save

