# -*- coding: utf-8 -*-
"""
Created on Wed Feb  10 10:38:25 2016

@author: sdoerr
"""


############
############
# Step 1: Spelling Mistakes
############
############

############
# Correct by hand
############

import re
import bisect


# Need to add Zahstelle to first line for excerpt to work
with open("/Users/sdoerr/Documents/Dokumente/_ZurichGSE/_2015-16/gitproject/bld/out/data/HandbuchDtAGs_1925_1_Band.txt", "r+") as f:
     old = f.read() # read everything in the file
     f.seek(0) # rewind
     f.write("Zahlstelle: Ges.-Kasse.\n\n" + old) # write the new line before
     f.close()

# Import txt file as searchfile and then convert it to a string
with open('/Users/sdoerr/Documents/Dokumente/_ZurichGSE/_2015-16/gitproject/bld/out/data/HandbuchDtAGs_1925_1_Band.txt', 'r') as searchfile:
    data = searchfile.read().replace('\n', 'yyy') # save the txt file as string (need to replace all line breaks with some characters (here: yyy))

# Replace wrong spellings (loop not working yet )
"""
# SALDO
saldoGM = ['Sa, Gm.' 'Sa. Gm.' 'Sa. UM.'] # types of spelling Sa. GM.
saldoRM = ["Sa. Rm." "Sa.yyyRM."] # types of spelling Sa. GM.
for i in range(0,len(saldoGM)-1):
    data = data.replace(saldoGM[i], 'Sa. GM.')
for i in range(0,len(saldoRM)-1):
    data = data.replace(saldoRM[i], 'Sa. RM.')

# Bilanz
bilanz = ["ßilanz"] # types of spelling Bilanz
for i in range(0,len(bilanz)-1):
    data = data.replace(bilanz[i], "Bilanz")
"""

# Saldo GM
data = data.replace('Sa, Gm.', 'Sa. GM.')
data = data.replace('Sa. Gm.', 'Sa. GM.')
data = data.replace('Sa. UM.', 'Sa. GM.')
# Saldo RM
data = data.replace('Sa. Rm.', 'Sa. RM.')
data = data.replace('Sa.yyyRM.', 'Sa. RM.')
# Bilanz
data = data.replace('ßilanz', 'Bilanz')

############
############
# Step 2: Firm Data
############
############

############
# Step 2a: Find Firm Names
############

f_name = []

# firm name is wedged between "zahlstelle" and "gegründet"
beforename = [m.end() for m in re.finditer('Zahlstelle', data)] # find end of Zahlstelle position
aftername = [m.start() for m in re.finditer('Gegründet', data)] # find beginning of Gegründet position
aftername.append(len(data)) # for last entry (PROBLEM: REMOVE LATER)

# Find all characters between Zahlstelle and Gegründet and store them in f_name
# There might be more than one Zahlstelle in each paragraph
for i in range(0,len(aftername)-1):
    j = i
    if (beforename[i] < aftername[i]) & (beforename[i+1] > aftername[i]):
        f_name.append(data[beforename[i]:aftername[i]])
    if (beforename[i] < aftername[i]) & (beforename[i+1] < aftername[i]) & (i<len(aftername)-1):
        j = i+1
        f_name.append(data[beforename[j]:aftername[i]])
    #if (beforename[i] < aftername[i]) & (beforename[i+2] < aftername[i]) & (i<len(aftername)-2):
     #   j = i+2
      #  f_name.append(data[beforename[j]:aftername[i]])



# Clean up some mess
for i in range(0,len(f_name)):
    #print(f_name[i])
    test1 = f_name[i].find('yyyyyy') # get rid of beginning mess at firm name
    f_name[i] = (f_name[i][test1+6:len(f_name[i])])

for i in range(0,len(f_name)):
    #print(f_name[i])
    test2 = f_name[i].rfind('yyyyyy') # get rid of ending mess at firm name
    f_name[i] = (f_name[i][0:test2])

"""
for i in range(0,len(f_name)):
    print(f_name[i])
"""


############
# Step 2b: Find Firm Paragraphs (so far excluding Zahlstelle)
############

# Firm paragraph
f_paragraph = [] # Paragraph containing all info about firm (PROBLEM: but missing ZAHLSTELLE)
for i in range(0,len(f_name)-1):  # PROBLEM: misses last entry...
    startfirm = data.find(f_name[i]) # find start of firm entry in data
    endfirm =  data.find(f_name[i+1]) # find end of firm (i.e. next firm name) entry in data
    f_paragraph.append(data[startfirm:endfirm])
# For last entry (PROBLEM: maybe remove later)
startfirm = data.find(f_name[len(f_name)-1])
endfirm = len(data)
f_paragraph.append(data[startfirm:endfirm])

"""
print(len(f_paragraph))
for i in range(0,len(f_paragraph)):
    print(f_paragraph[i])
"""

############
# Step 2c: Find founding date (Gegründet)
############

# There is only one "Gegründet" between two firm names
# Strategy:
#   - search for string "Gegründet" between two firm names
#   - save 50+ characters following "gegründet" in file
#   - find minimum 4 digit sequence (e.g. 1896 in 1896, 1897)

# in Firm paragraph, find firm age
f_age = []
for i in range(0,len(f_paragraph)): # PROBLEM: misses last entry...
    founded = f_paragraph[i].find("Gegründet")
    # find string "Gegründet" and take 100 characters following "Gegründet"
    # then find all digits in founded, convert them to integers and sort them for bisect method
    results = sorted([int(k) for k in re.findall("[0-9]+", f_paragraph[i][founded:founded+100])])
    f_age.append(results[bisect.bisect_right(results,1800)]) # find the smallest number larger 1800 (for founding date)
"""
for i in range(0,len(f_age)):
    print(f_name[i])
    print(f_age[i])
"""

############
# Step 2d: Find Firm Size (Saldo Sa. GM. and variations)
############

f_saldoGM = [] # Balance sheet in Gold Mark
f_saldoRM = [] # Balance sheet in Reichs Mark
for i in range(0,len(f_paragraph)):
    bilanz = [m.end() for m in re.finditer('Bilanz', f_paragraph[i])] # find all values for bilanz
    sagm = [m.end() for m in re.finditer('Sa. GM.', f_paragraph[i])] # find all values for goldmark saldo
    sarm = [m.end() for m in re.finditer('Sa. RM.', f_paragraph[i])] # find all values for reichsmark saldo
    """
    print(bilanz)
    print(sagm)
    print(sarm)
    """
    # GOLDMARK
    if sagm == []:
        f_saldoGM.append('NA')
    else:
        if len(sagm) == 1:
            f_saldoGM.append(f_paragraph[i][sagm[0]:sagm[0]+15])
        if (len(sagm) > 1) & (len(bilanz) == 1):
            f_saldoGM.append(f_paragraph[i][sagm[0]:sagm[0]+15])
        if (len(sagm) > 1) & (len(bilanz) > 1):
            f_saldoGM.append(f_paragraph[i][sagm[0]:sagm[0]+15])
    # REICHSMARK
    if sarm == []:
        f_saldoRM.append('NA')
    else:
        if len(sarm) == 1:
            f_saldoRM.append(f_paragraph[i][sarm[0]:sarm[0]+15])
        if (len(sarm) > 1) & (len(bilanz) == 1):
            f_saldoRM.append(f_paragraph[i][sarm[0]:sarm[0]+15])
        if (len(sarm) > 1) & (len(bilanz) > 1):
            f_saldoRM.append(f_paragraph[i][sarm[0]:sarm[0]+15])
    f_saldoGM[i] = ''.join(x for x in f_saldoGM[i] if x.isdigit()) # Extract digits only
    f_saldoRM[i] = ''.join(x for x in f_saldoRM[i] if x.isdigit()) # Extract digits only

"""
print(f_saldoGM)
print(f_saldoRM)
"""

############
############
# Step 3: Write to Excel
############
############

import xlwt

book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("Sheet 1")

k = 0 # row headers
sheet1.write(k, 0, "Name")
sheet1.write(k, 1, "Age")
sheet1.write(k, 2, "Saldo GM")
sheet1.write(k, 3, "Saldo RM")

j = 1 # row for data
i=j # start of column for data

for n in f_name:
    i = i+1
    sheet1.write(i, 0, n)

i=j
for n in f_age:
    i = i+1
    sheet1.write(i, 1, n)

i=j
for n in f_saldoGM:
    i = i+1
    sheet1.write(i, 2, n)

i=j
for n in f_saldoRM:
    i = i+1
    sheet1.write(i, 3, n)

book.save("/Users/sdoerr/Documents/Dokumente/_ZurichGSE/_2015-16/gitproject/bld/out/analysis/datafirmdata.xls")


"""
# ALWAYS CHECK LENGTH
print(len(f_saldoGM))
print(len(f_saldoRM))
print(len(f_age))
print(len(f_paragraph))
print(len(f_name))
"""
