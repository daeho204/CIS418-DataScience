import os
import random
import shutil

greyDir = "imagesGrey"
feedDir = "feedData"
trainingDir = os.path.join(feedDir, 'train', 'images')
testingDir = os.path.join(feedDir, 'validation', 'images')

if os.path.isdir(feedDir):
    shutil.rmtree(feedDir)
os.mkdir(feedDir)
os.mkdir(os.path.dirname(trainingDir))
os.mkdir(trainingDir)
os.mkdir(os.path.dirname(testingDir))
os.mkdir(testingDir)

images = os.listdir(greyDir)

numImages = len(images)
testingRatio = 0.1
numTestingImg = int(numImages * testingRatio)
testingIndexes = random.sample(range(numImages), numTestingImg)

for x in range(0, len(images)):
    if x in testingIndexes:
        print("{}/{} TESTING - {}".format(x, len(images), images[x]))
        shutil.copyfile(os.path.join(greyDir, images[x]), 
            os.path.join(testingDir, images[x]))
    else:
        print("{}/{} TRAINING - {}".format(x, len(images), images[x]))
        shutil.copyfile(os.path.join(greyDir, images[x]), 
            os.path.join(trainingDir, images[x]))

print("Total: {}".format(numImages))
print("Training: {}".format(numImages - numTestingImg))
print("Testing: {}".format(numTestingImg))
