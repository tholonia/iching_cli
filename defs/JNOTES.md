### Make all the markdown files:

expects:

- `/home/jw/store/src/iching_cli/defs/BOOK_INTRO.md`
- JSON files in `/home/jw/src/iching_cli/defs/final`
- `<ID>_descp.txt` files in `/home/jw/store/src/iching_cli/defs/final/descp`

```sh
cd /home/jw/src/iching_cli/defs/bin
./makeallmd.py -o out.md
# NOTE: this does not add the hex desc rewrite
# To add thos, do the following

# Update ALL image descriptions with '/update_image_data.py ${padded_value}'
./UPDATE_IMAGE_DATA ./update_image_data.py ${padded_value}

# The hex desc rewrite is added when makeallmd.py is run

```

This creates the output file `/home/jw/src/iching_cli/defs/out.md`

Use TYPORA to export to PDF



### Add fields to JSON

```sh
cd /home/jw/src/iching_cli/defs/bin
# Update ALL json files with ./update_json.py
./UPDATE_JSON_ALL 

```

### Create image for hexagram

```sh
cd /home/jw/src/iching_cli/defs/final
export OPENAI_API_KEY=sk-proj-66666666666666666666666666666666
./makeimg2.py --cfg 7.0 --denoise 0.7 --steps 40 --batch-size 1 --random-seed 20

# ImgDesc output = ./<ID>_<N>_.png_analysis.txt
# Image output = /home/jw/src/ComfyUI/output/<ID>_<N>_.png

```

