## Assumptions

```sh
H=/home/jw/store/src/iching_cli/defs
```

### Make all the markdown files:

expects:

- `/home/jw/store/src/iching_cli/defs/BOOK_INTRO.md`
- JSON files in `${H}/final`
- `<ID>_descp.txt` files in `/home/jw/store/src/iching_cli/defs/final/descp`

```sh
cd ${H}/bin
./makeallmd.py -o out.md
# NOTE: this does not add the hex desc rewrite
# To add thos, do the following

# Update ALL image descriptions with '/update_image_data.py ${padded_value}'
./UPDATE_IMAGE_DATA ./update_image_data.py ${padded_value}

# The hex desc rewrite is added when makeallmd.py is run

```

This creates the output file `${H}/out.md`

Use TYPORA to export to PDF



### Add fields to JSON

```sh
cd ${H}/bin
# Update ALL json files with ./update_json.py
./UPDATE_JSON_ALL 

```

### Create image for hexagram

```sh
cd ${H}/final
export OPENAI_API_KEY=sk-proj-66666666666666666666666666666666
./makeimg2.py --cfg 7.0 --denoise 0.7 --steps 40 --batch-size 1 --random-seed 20

# ImgDesc output = ./<ID>_<N>_.png_analysis.txt
# Image output = /home/jw/src/ComfyUI/output/<ID>_<N>_.png

```



## Adding Sets



​    \# setnu,m is used to select whocui image and descriptions top use

​    \# s0 = 1280x1280, s1 = 1280x9-something

​    \# setnum = "_s1"



# To make a new set of images and their blurbs:

## Images

- Ensure you have the folders... where `s[0,1,...]` is the set number 

```sh
${H}/final # holds JSON files
${H}/final/s[0,1,..] # holds PNG files a image blurb files
${H}/final/s[0,1,..]/descp # holds the rewritten literary hexagram definitions
```

Test image parameters with:

```sh
cd ${H}/bin
./makeimg2.py --cfg 8.0 --denoise 0.8 --steps 40 --batch-size 1 --random-seed 03m # note 03 is ID no seed
```

Once happy with results, run the following to make all images:

```sh
cd ${H}/bin
# make sure th output folder is empty before running the sceipt
./MAKE_IMAGES_BATCH "--cfg 8.0 --denoise 0.8 --steps 40 --batch-size 1 --random_seed "
```

The run `MAKE_IMAGES_BATCH` which look like:

```sh
cd ${H}/bin
./makeimg2.py ${ARGS} 01
./makeimg2.py ${ARGS} 02
./makeimg2.py ${ARGS} 03
./makeimg2.py ${ARGS} 04
./makeimg2.py ${ARGS} 05
./makeimg2.py ${ARGS} 06
...
```

This creates images files in `/home/jw/src/ComfyUI/output/`, i.e.:

```sh
/home/jw/src/ComfyUI/output/01_00001.png
/home/jw/src/ComfyUI/output/02_00001.png
/home/jw/src/ComfyUI/output/03_00001.png
...
# and
${H}/bin/01_.png_analysis.txt
${H}/bin/02_.png_analysis.txt
${H}/bin/03_.png_analysis.txt
...
```

These need to be renamed.

```sh
cd /home/jw/src/ComfyUI/output/
rename _00001 s1 *.png
cd ${H}/bin
rename _.png_analysis.txt .txt *.txt
```

which creates:

```sh
/home/jw/src/ComfyUI/output/01.png
/home/jw/src/ComfyUI/output/02.png
/home/jw/src/ComfyUI/output/03.png
# and 
${H}/bin/01.txt
${H}/bin/02.txt
${H}/bin/03.txt
```

These are then moved to the new set folder:

```sh
mv /home/jw/src/ComfyUI/output/* ${H}/final/s1
mv ${H}/bin/??.txt ${H}/final/s1
```

To make the entire doc (which will also make hex descriptions if they do not exist) - this also updates the JSON files in `${H}/final` with the sets `descp` files - run the following:

- ***NOTE: there is (currently) oner set of JSON files only, with multiple sets of images, blurbs, and hex description.***

```sh
cd ${H}/bin
./makeallmd.py -o out.md -s 1
```

this create a new set #1, and creates image blurbs in 

```sh
${H}/finsl/s1/NN_descp.txt
```

### Update JSON with image file and description

```sh
cd ${H}/bin
./UPDATE_IMAGE_DATA <setnum>
```





