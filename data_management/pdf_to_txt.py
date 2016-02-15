# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 11:54:56 2016

@author: sdoerr
"""


############
# Step 0: Pick PDF file and transform into .txt file
############

# open terminal and type:
# pdftotext -layout -enc 'UTF-8'  /Users/sdoerr/Desktop/Akt.pdf
#-enc 'UTF-8' is for umlaute
#-layout is for keeping the default layout

# Convert pdf file to text through Terminal command via Python:

import os
os.system("cd /Users/sdoerr/Documents/Dokumente/_ZurichGSE/_2015-16/gitproject/src/original_data/ \n pdftotext -layout -enc 'UTF-8'  ./HandbuchDtAGs_1925_1_Band.pdf")
os.system("mv /Users/sdoerr/Documents/Dokumente/_ZurichGSE/_2015-16/gitproject/src/original_data/HandbuchDtAGs_1925_1_Band.txt /Users/sdoerr/Documents/Dokumente/_ZurichGSE/_2015-16/gitproject/bld/out/data/")

