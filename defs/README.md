`questions.md' - questions and reference notes
`popjson.py` - build JSON from AI outoput - WARNING! IT MAKES DIFFERNT JSON FORMATS FOR EACH RUN :(
`tholonic_primer.md` - used to build AI context
`template*.md` - templated to control the output
`capquote.py`, `uncap.py` - change all uppercase to first_upoer case



Numbered folders hold the outoput from the AI queries (in `questions.md`) and otehr hexagram related file.

`./alls` -  holds t1he merged content
`./alls/core` - core the core content 
`./alls/rem` -  holsd the remaining content
`./alls/out` - hold the JSON conversions of each core MD file and rem MD file, and their combined JSON file.


## Notes
After makign any chages to the rom.md or core.md files, you need to rebuild the combined files with `./RUNMERGE` in `./defs`.
This runs `merge.py` which combined the two JSON file data into one file save in `./out`

To make a MD output file:
```sh
./makemd.py -o out.md template_alls.md  alls/out/01_c.json
```

