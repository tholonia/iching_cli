#!/bin/bash

D="/home/jw/src/iching_cli/book/v2/bin"

rm ${D}/../includes/iching.html
rm ${D}/../includes/iching.md

#! need to copy latrest css for typora
lessc ${D}/../includes/iching.less ${D}/../includes/iching.css
cp ${D}/../includes/iching.css /home/jw/.config/Typora/themes/iching_7_44-9_68.css


# make the copyright page
#! prince-books ../docs/COPYRIGHT_PAGE.md  -o ../includes/copyright.pdf

# make the coverpage
#! PDF export doc/COVERPAGE.html to includes/coverpage.pdf

#./makeallmd.py --content all
./makeallmd.py --content pages


typora ${D}/../includes/iching.md

# after export./ makebook_postonly.sh in called from Typora