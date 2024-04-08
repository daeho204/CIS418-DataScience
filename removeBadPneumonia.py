from PIL import Image
import os
import shutil
import csv

typesOfPnemonia = {}
typesOfCovid = {}

infoFile = "patientInfo.csv"
with open(infoFile) as f:
    reader = csv.reader(f)
    next(reader)
    pInfo = list(reader)

for info in pInfo:
    if(info[1] not in typesOfPnemonia.keys()):
        typesOfPnemonia[info[1]] = [info[0]]
    else:
        typesOfPnemonia[info[1]].append(info[0])

    if(info[2] not in typesOfCovid.keys()):
        typesOfCovid[info[2]] = [info[0]]
    else:
        typesOfCovid[info[2]].append(info[0])

for key in typesOfPnemonia.keys():
    print("{} - {}".format(key, len(typesOfPnemonia[key])))   

exit()
'''
From this it looks like there are a number of Pneumonias that don't have a lot of examples.
Removing them from the dataset.
Undefined Pneumonia - 
None - 
Fungal Pneumonia - 
Pneumonia - 
'''

idsToRemove = typesOfPnemonia["Undefined Pneumonia"] + typesOfPnemonia["None"] + typesOfPnemonia["Fungal Pneumonia"] + typesOfPnemonia["Pneumonia"] 

greyDir = "imagesGrey"
images = os.listdir(greyDir)

numFound = 0
for img in images:
    fileComponents = img.split("_")
    if(fileComponents[0] in idsToRemove):
        numFound += 1
        os.remove(os.path.join(greyDir, img))

print("Removed {}/{} files".format(numFound, len(idsToRemove)))




