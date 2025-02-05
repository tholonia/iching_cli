#!/bin/bash

rm docs/iching.html

#./makeallmd.py --content all
./makeallmd.py --content pages

typora docs/iching.md

# prince-books \
# 	--style=/home/jw/.config/Typora/themes/iching_7_44-9_68.css \
# 	--media=print \
# 	--page-size="7.44in 9.68in" \
# 	--page-margin=0mm \
# 	-o docs/iching_all.pdf \
# 	docs/iching.html

# pdftk docs/iching_all.pdf cat 2-end output docs/iching_nocover.pdf

# ./rm_empty_pages.py docs/iching_nocover.pdf

# ./reorg.py  docs/clean_iching_nocover.pdf docs/iching.pdf

# okular docs/iching.pdf

