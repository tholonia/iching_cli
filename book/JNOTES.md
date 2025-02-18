# conversion

```sh
./iching-converter.py ../_v2 ../converted # convert from ../_v2 to ../converted
./fix-colon.py ../converted ../colon # fix : in lines in transition
./regen_lines_in_trans.py ../colon ../regen # updates lines_in_transition
./regen_lines_in_context.py ../regen <hex> <index: 0,1,2) # updates SRC file's 'lines_in_context'
	./regen_lines_in_context_BATCH.sh # run on all
	
alter_trigrams.py	



```









# RUN

```sh
cd /home/jw/src/iching_cli/book/v2/bin
./makebook.sh
```

Export document as HTML in /book/v2/includes

After saving , Typora will automatically run `./makebook.sh` and pop up the new PDF in Okular.






# The Publishing Process

 ```sh
conda activate cbot
cd /home/jw/src/iching_cli/defs/bin
export N=99  # determines which set to use (under ./final folder)
export OPENAI_API_KEY=sk-proj-GocJ9l8HATWvK2ZEj4w...
export H=/home/jw/store/src/iching_cli/defs

./makeallmd.py -o out.md -s ${SET} # create out.md
./makeallmd.py -o PAGE12.md -s ${SET} --hex 12 # print only 1 page w/o forward
./makeallmd.py -o OUT.MD -s ${SET} --content pages # print pages only, not forward

typora out.md # ensure it is configured correctly

# >>> export to out.pdf

./rm_empty_pages.py out.pdf # rm  empty pages to clean_out.pdf - BREAKS OUTLINE
./reorg.py # ensures images appear on right page. in=out.pdf out=reorg.pdf

# Add forward to book
pdftk \
/home/jw/books/iching/Latest/ICHING_THE_BOOK.pdf \
/home/jw/books/iching/chapters/150-PART-II.pdf \
out.pdf \
cat output book_merged.pdf



 ```



## Assumptions

```sh
export H=/home/jw/store/src/iching_cli/defs
```

image output is set to 1:0.7546875

                "height": 966,
                "width": 1280



### Make all the markdown files:



expects:

- `/home/jw/store/src/iching_cli/defs/BOOK_INTRO.md`
- JSON files in `${H}/final`
- `<ID>_descp.txt` files in `/home/jw/store/src/iching_cli/defs/final/descp`. If the files or the folder is not there, they will be created.

  - > `descp` files are the rewritten lines based on the list of individual attributes, to create a coherent and literay description instead of a list of attributes. This rewriting takes place in `makeallmd.py`


```sh
cd ${H}/bin
N=99 #99 = the curated set of images)
./makeallmd.py -o out.md -s 99
# NOTE: this does add the hex desc rewrite in folder filan/${N}/descp
# To add thos, do the following

# Update ALL image descriptions in the JSON files with '/update_image_data.py ${padded_value}'
./UPDATE_IMAGE_DATA ./update_image_data.py ${padded_value}


```

This creates the output file `${H}/out.md`

Use TYPORA to export to PDF



### Add fields to JSON

```sh
cd ${H}/bin￼
mkdir -p ${H}/BOOK_INTRO.md`
- JSON files in `${H}/final`
- `<ID>_descp.txt` files in `/home/jw/store/src/iching_cli/defs/final/descp`

# Update ALL json files with ./update_json.py
./UPDATE_JSON_ALL 

```

### Create image for hexagram

#### Method 1

```sh
cd ${H}/final
export OPENAI_API_KEY=sk-proj-66666666666666666666666666666666
./makeimg2.py --cfg 7.0 --denoise 0.7 --steps 40 --batch-size 1 --random-seed 20

# ImgDesc output = ./<ID>_<N>_.png_analysis.txt
# Image output = /home/jw/src/ComfyUI/output/<ID>_<N>_.png

```

#### Method 2

```sh
  ./batch_render.py --hexagram 01 --number 6 --cfg 10
  # or for all...
  RENDER_BATCH.sh
```



### Image extend

- uses ComfyUI workflows and VAE encoded images to create a new image of a new size

```sh
 ./extend_image.py r_36_00006__out.png /home/jw/src/iching_cli/defs/final/36.json
 # and/or BATCVH_FILLIN.sh
```



## Adding Sets



​    \# setnu,m is used to select whocui image and descriptions top use

​    \# s0 = 1280x1280, s1 = 1280x9-something

​    \# setnum = "_s1"



# To make a new set of images and their blurbs:

## Images

- First make the required target dirs:

```sh
  export N=8
  mkdir ${H}/final/s${N} # holds PNG files a image blurb files
  mkdir ${H}/final/s${N}/desq #holds rewritten literary hexagram definitions
```
- Next add the `README.md` and `prompt.md` files.  
```sh
touch ${H}/final/s${N}/README.md
touch ${H}/final/s${N}/prompt.md
```

Test image parameters with:

```sh
cd ${H}/bin
./makeimg.py --cfg 8.0 --denoise 0.8 --steps 40 --batch-size 1 --random-seed 03 # note 03 is ID no seed
# NOTE:
makeimg.py -> 
```

to change the resolution, edit line 217, 218
```
                "height": 966,
                "width": 1280
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
rename _00001_.png .png *.png
cd ${H}/bin
rename _00001_.png_analysis.txt .txt *.txt
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

- ***NOTE: there is (currently) one set of JSON files only, with multiple sets of images, blurbs, and hex description.***

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

# To update image and desc for a single hexagram

Generate new description based on the new image

```sh
./makeimg_desc.py 48 /home/jw/src/ComfyUI/output/r_48_00003__out_00001_.png
# This also create s txt file of teh new description in the folder where the 
# new image exists. You then most manually copy the new description to the live description.
cp \
  /home/jw/src/ComfyUI/output/r_48_00003__out_00001_.txt \
  /home/jw/src/iching_cli/defs/final/s99/48.txt


```
If accepted, update the live image with the new image with the following command:

```sh
./round_corners.py \
   /home/jw/src/ComfyUI/output/r_48_00003__out_00001_.png \
   /home/jw/src/iching_cli/defs/final/s99/48.png
```

---

---

---



`./MKRUN` *set env and create args list*

- calls `./MK` 

  - `export N=11`

    `export ARGS="--cfg 1.0 --denoise 0.7 --steps 40 --batch-size 1 ...`

  - calls `./MAKE_BATCH_IMAGES`
    - calls `./makeimg.py ${ARGS} 01`
    - NOTE: `makeimg.py` in a symlink to `makeimg_flux.py`
  - calls `./MK`  *clears output folder, makes new set folders* 
  - *creates `${N}.png` images and `${N}.txt` files in* `final/{set}` *folder. moves all files in output to set folders*
  - calls `./makeallmd.py -o out.md -s ${N}`



