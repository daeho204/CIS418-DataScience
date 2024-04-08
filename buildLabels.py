from PIL import Image
import os
import shutil
import csv

feedDir = "feedData"
trainingDir = os.path.join(feedDir, 'train', 'images')
testingDir = os.path.join(feedDir, 'validation', 'images')


PneumoniaKey = {"No Pneumonia (healthy)":0,
    "Bacterial Pneumonia":1,
    "Viral Pneumonia":2,
}

HasCovidKey = {"False":0,
    "True":1
}

patientDict = {}

infoFile = "patientInfo.csv"
with open(infoFile, newline='') as f:
    reader = csv.reader(f)
    next(reader)
    pInfo = list(reader)

for info in pInfo:
    patientDict[info[0]] = (info[1], info[2])

#write the label files
trainingLabels = []
for root, dirs, files in os.walk(trainingDir):
    for f in files:
        pID = f.split("_")[0]
        pnKey = PneumoniaKey[patientDict[pID][0]]
        hcKey = HasCovidKey[patientDict[pID][1]]
        trainingLabels.append((pnKey, hcKey))
        print("{},{},{}".format(pID, pnKey, hcKey))

trainingFile = os.path.join(feedDir,'trainLabels.txt')
f = open(trainingFile, "w")
for l1, l2 in trainingLabels:
    f.write("{},{}\n".format(l1, l2))

testingLabels = []
for root, dirs, files in os.walk(testingDir):
    for f in files:
        pID = f.split("_")[0]
        pnKey = PneumoniaKey[patientDict[pID][0]]
        hcKey = HasCovidKey[patientDict[pID][1]]
        testingLabels.append((pnKey, hcKey))
        print("{},{},{}".format(pID, pnKey, hcKey))

testingFile = os.path.join(feedDir,'validationLabels.txt')
f = open(testingFile, "w")
for l1, l2 in testingLabels:
    f.write("{},{}\n".format(l1, l2))






