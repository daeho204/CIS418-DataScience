##### Note
This folder is splits processing into multople seperate steps
This is done to reduce the overall run time, as well  as for faster and easier debugging
Before running the CNN
#####

##### directory descriptions
images - the image data that is the result of the initial data pulling script
imagesGrey - all for the images (with original names) converted into greyscale images
patientInfo.csv - csv file made during the initial data pulling step that links to images
feedData - contains all of the testing and training data
feedData/testingLabels.txt - contains a tuple of labels for testing data
feedData/trainingLabels.txt - contains a tuple of labels for training data
feedData/training - contains the training images
feedData/testing - contains the testing images
#####

##### Processing Order
copy in images to images dir
python convertImagesToGrey.py
python removeBadPneumonia.py
python splitTestingAndTrainingData.py
python buildLabels.py
python sortIntoClasses.py
remove the feedData/.../images dir (the non class sorted dir)
run CNN.ipynb  
#####
