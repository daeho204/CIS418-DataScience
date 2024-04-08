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

labelFile = "feedData/trainLabels.txt"
with open(labelFile, newline='') as f:
    lines = f.readlines()

lines = [x.split(',')[0] for x in lines]
print(lines)

x = 0
os.mkdir(os.path.join(feedDir, 'train', '0'))
os.mkdir(os.path.join(feedDir, 'train', '1'))
os.mkdir(os.path.join(feedDir, 'train', '2'))
for root, dirs, files in os.walk(trainingDir):
    for f in files:
        os.rename(os.path.join(trainingDir, f), os.path.join(feedDir, 'train', lines[x], f))
        x = x + 1

labelFile = "feedData/validationLabels.txt"
with open(labelFile, newline='') as f:
    lines = f.readlines()

lines = [x.split(',')[0] for x in lines]
print(lines)

x = 0
os.mkdir(os.path.join(feedDir, 'validation', '0'))
os.mkdir(os.path.join(feedDir, 'validation', '1'))
os.mkdir(os.path.join(feedDir, 'validation', '2'))
for root, dirs, files in os.walk(testingDir):
    for f in files:
        os.rename(os.path.join(testingDir, f), os.path.join(feedDir, 'validation', lines[x], f))
        x = x + 1






