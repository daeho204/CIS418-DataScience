from PIL import Image
import os
import shutil

imageDir = "images"
greyDir = "imagesGrey"
if os.path.isdir(greyDir):
    shutil.rmtree(greyDir)
os.mkdir(greyDir)

images = os.listdir(imageDir)

for x in range(0, len(images)):
    filename = images[x]
    print("{}/{} - {}".format(x, len(images), filename))
    if('.png' not in filename):
        continue

    filePath = os.path.join(imageDir, filename)
    filePathDest = os.path.join(greyDir, filename)

    img = Image.open(filePath)
    imgGray = img.convert('L')
    imgGray.save(filePathDest)
