#!/bin/bash

#./makeallmd.py
#typora docs/iching.md

D="/home/jw/src/iching_cli/book/v2/bin"

lessc docs/iching.less docs/iching.css

prince-books \
	--style=${D}/docs/iching.css \
	--media=print \
	-o ${D}/docs/iching.pdf \
	${D}/docs/iching.html



	# --page-size="7.44in 9.68in" \
	# --page-margin=0mm \

# pdftk ${D}/docs/iching_all.pdf cat 2-end output ${D}/docs/iching.pdf

# cd ${D}/

# ${D}/rm_empty_pages.py ${D}/docs/iching_nocover.pdf

# ${D}/reorg.py  ${D}/docs/clean_iching_nocover.pdf ${D}/docs/iching.pdf

okular ${D}/docs/iching.pdf

