#!/bin/bash

#./makeallmd.py
#typora docs/iching.md

D="/home/jw/src/iching_cli/book/v2/bin"

rm ${D}/../docs/FINAL_iching.pdf

prince-books \
	--style=${D}/../includes/iching.css \
	--media=print \
	-o ${D}/../includes/iching.pdf \
	${D}/../includes/iching.html

# add copyrigth and cover tp pdfg
pdftk ../includes/coverpage.pdf \
      ../includes/copyright.pdf \
      ../includes/iching.pdf \
      cat output ${D}/../docs/FINAL_iching.pdf

okular ${D}/../docs/FINAL_iching.pdf

