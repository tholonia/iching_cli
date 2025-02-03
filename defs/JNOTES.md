

# Tree

```
./final
```

```
./final/99
```

- holds the various sets in numbered folders.  99 is the set that represent the latest working version.
- Each set contains
  - Images - numbered PNG files
  - Image description - numbered TXT files

```
./final/99/descp
```

- numbered TXT files that hold the description of the hexagram

```
./final/99/alts	
```

- Optional folder that holds alternatives text or images.  More like a archive folder



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



Publishers

inding a publisher with a strong focus on metaphysical, alchemical, spiritual, or philosophical works, especially those with experience in publishing I Ching literature, is essential for your book's success.Here are several reputable publishers that align with your criteria: **1. Red Wheel/Weiser**

stablished in 1956, Red Wheel/Weiser is renowned for its extensive catalog of occult and New Age publications.hey have a history of publishing works related to the I Ching and other esoteric subjects.heir imprints, including Weiser Books, specialize in topics such as Eastern religions, mysticism, and divination.citeturn0search13 **2. Arkana Publishing**

s an imprint of Penguin Group, Arkana Publishing focuses on esoteric literature.hey have published works by notable authors in the fields of spirituality and philosophy, including titles related to the I Ching.citeturn0search10 **3. North Atlantic Books**

orth Atlantic Books is known for its diverse range of publications encompassing spirituality, philosophy, and alternative health.hey have published comprehensive guides on the I Ching, such as "I Ching, the Oracle: A Practical Guide to the Book of Changes."citeturn0search0 **4. Simon & Schuster**

imon & Schuster has ventured into publishing works that explore the I Ching from unique perspectives.n example is "The Occult I Ching" by Maja D'Aoust, which delves into the mystical aspects of the text.citeturn0search3 **5. Inner Traditions – Bear & Company**

pecializing in metaphysical and spiritual books, Inner Traditions has a catalog that includes works on alchemy, mysticism, and Eastern philosophies.hey have published titles that explore the I Ching and its applications in various spiritual practices. **6. Llewellyn Worldwide**

lewellyn is a well-known publisher in the realm of metaphysical literature.heir publications cover a broad spectrum of spiritual and philosophical topics, including the I Ching. **7. Shambhala Publications**

hambhala focuses on books that present creative and conscious ways of transforming the individual, the society, and the planet.hey have a selection of works related to Eastern philosophy and the I Ching. **Next Steps:**

- **Research Submission Guidelines:** isit each publisher's official website to understand their submission process and ensure your manuscript aligns with their current interests.
- **Prepare a Proposal:** raft a compelling book proposal that highlights the unique aspects of your work and its relevance to the publisher's audience.
- **Consider Literary Agents:** ngaging a literary agent with experience in metaphysical or philosophical literature can enhance your chances of securing a publishing deal. y targeting these publishers, you align your work with those who appreciate and specialize in the profound themes presented in the I Ching.

Red Wheel/Weiser

 Arkana Publishing

North Atlantic Books. 

Inner Traditions – Bear & Company

Llewellyn Worldwide



SUBMISSION GUIDELINES

**1. Red Wheel/Weiser**

Red Wheel/Weiser welcomes submissions that align with their focus on spirituality, occult, and esoteric subjects. They request a comprehensive proposal including:

- A cover letter with author information and a brief description of the proposed work.
- An overview of the book, complete table of contents, market/audience analysis (including similar titles), details of your marketing and publicity experience or plans, your qualifications to write the book, and two or three sample chapters.
- If applicable, sample illustrations or photographs (duplicates, not originals).

Ensure your submission includes your phone number, email, and mailing address. For more detailed information, please refer to their submission guidelines.

**2. Arkana Publishing**

Arkana Publishing is an imprint of Penguin Random House focusing on esoteric literature. Currently, they do not accept unsolicited manuscripts. It's advisable to consult their official page for any updates or consider submitting through a literary agent.

**3. North Atlantic Books**

North Atlantic Books accepts both agented and unagented works that promote healing of self, spirit, and society. They prefer electronic submissions sent to submissions@northatlanticbooks.com, formatted as a Word document or PDF (Google Docs or Pages files are not accepted). Your proposal should include:

- A cover letter introducing yourself and your work.
- A detailed book proposal with an overview, target audience, market analysis, promotion ideas, and a chapter outline.
- Two to three sample chapters.

They aim to respond within three months but may not reply to all proposals due to the volume received. For comprehensive guidelines, visit their [submission page](https://www.northatlanticbooks.com/submission-guidelines/).

**4. Inner Traditions – Bear & Company**

Inner Traditions specializes in spiritual and esoteric subjects. They request that you review their imprints to ensure your work fits their criteria before submitting. Due to the high volume of submissions, they may not respond to every proposal. If you haven't heard back within eight weeks, it's likely your work isn't a fit for their publishing house. For submission instructions, please see their [publishing page](https://www.innertraditions.com/publish).

**5. Llewellyn Worldwide**

Llewellyn Worldwide accepts submissions directly from authors, including first-time authors, as well as from literary agents. They focus on mind, body, and spirit topics. For detailed submission instructions, please review their [author submissions page](https://www.llewellyn.com/about/author_submissions.php).

**General Tips:**

- **Align Your Proposal:** Ensure your manuscript aligns with the publisher's focus and guidelines.
- **Follow Submission Instructions:** Adhere strictly to each publisher's submission requirements to enhance the likelihood of consideration.
- **Consider Literary Representation:** For publishers not accepting unsolicited manuscripts, engaging a literary agent may be beneficial.

By carefully tailoring your submissions to each publisher's guidelines, you increase the chances of finding the right home for your I Ching manuscript.

LITERARY AGENTS

**1. Aevitas Creative Management**

Aevitas Creative Management is a full-service literary agency with agents specializing in religion and spirituality. Their team includes experienced agents who have represented a diverse range of authors in the spiritual and philosophical domains. 

[aevitascreative.com](https://www.aevitascreative.com/agent-genre/agents-religion-and-spirituality?utm_source=chatgpt.com)



**2. Rita Rosenkranz Literary Agency**

Rita Rosenkranz represents adult non-fiction titles, including spirituality. She has a keen interest in works that offer new perspectives and contribute meaningfully to their respective fields. 

[writingtipsoasis.com](https://writingtipsoasis.com/literary-agents-for-spiritual-books/?utm_source=chatgpt.com)



**3. Writers House**

Lisa DiMona of Writers House focuses on non-fiction, encompassing spirituality and personal development. She is interested in authors who provide unique insights into spiritual practices and philosophies. 

[writingtipsoasis.com](https://writingtipsoasis.com/literary-agents-for-spiritual-books/?utm_source=chatgpt.com)



**4. The Knight Agency**

Elaine Spencer at The Knight Agency is open to non-fiction projects related to spirituality, religion, and self-help. She values innovative approaches to spiritual topics that can engage a broad audience. 

[writingtipsoasis.com](https://writingtipsoasis.com/literary-agents-for-spiritual-books/?utm_source=chatgpt.com)



**5. FinePrint Literary Management**

Peter Rubie, CEO of FinePrint Literary Management, represents non-fiction works in spirituality and well-being. He seeks authors who can present profound spiritual concepts in an accessible manner. 

[writingtipsoasis.com](https://writingtipsoasis.com/literary-agents-for-spiritual-books/?utm_source=chatgpt.com)



**6. Writers House**

Johanna V. Castillo of Writers House has a history of working with authors who explore spiritual themes. She is interested in narratives that delve into personal growth and spiritual journeys. 

[writingtipsoasis.com](https://writingtipsoasis.com/literary-agents-for-spiritual-books/?utm_source=chatgpt.com)



# V2 process

- Export to `iching.docx`
  - Open in libreoffice
    - apply style (in `ching_stype.odt`)
    - add TOC
    - Export tp PDF (`iching.pdf`)
- run `reorg.py` to right-align chapter images, produced `reorg.pdf`

