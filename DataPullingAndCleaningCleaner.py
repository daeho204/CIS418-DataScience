import os
import json
import requests
import shutil

#setting up surce directories
imageDir = os.path.join("source", "all-images-v2")
dataPrepDir = "dataPrep"
imgDir = os.path.join(dataPrepDir, "images")
if os.path.isdir(dataPrepDir):
    shutil.rmtree(dataPrepDir)
os.mkdir(dataPrepDir)
os.mkdir(imgDir)

#Loading all the source json files
images = os.listdir(imageDir)

patientInfo = []

#go through each of the json files
for x in range(0, len(images)):
    #read the json file
    with open("{}/{}".format(imageDir, images[x]), 'r') as f:
        dataId = x + 1
        data = json.load(f)
        #skip images flagged as Ignore
        for ann in data["annotations"]:
            if 'Ignore' in ann["name"]:
                continue

        #progress message
        print("ID: {} / {}".format(dataId, len(images)))
        
        #go through all the json tags and see set the values
        PneumoniaStatus = None
        HasCovid = False
        HasLungAnnotations = False
        Lung1Info = None
        Lung2Info = None
        Lung1BB = None
        Lung2BB = None
        ICU_admission = None
        Survival = None
        Sex = None
        Age = None
        for ann in data["annotations"]:
            if 'Pneumonia' in ann["name"]:
                #all pneumonia tags have 'Pneumonia' in the string
                PneumoniaStatus = ann["name"]
            if 'COVID' in ann["name"]:
                #tag is present only for covid patients
                HasCovid = True
            if 'Lung' in ann["name"]:
                #there is a lung path
                HasLungAnnotations = True
                if ann["polygon"]:
                    if not Lung1Info:
                        Lung1Info = ann["polygon"]
                        Lung1BB = ann["bounding_box"]
                    else:
                        #we already did one lung this one must be lung 2
                        Lung2Info = ann["polygon"]
                        Lung1BB = ann["bounding_box"]
            if 'ICU_admission' in ann["name"]:
                #ex ICU_admission/Y
                ICU_admission = ann["name"].split('/')[-1]
            if 'Survival' in ann["name"]:
                #ex Survival/Y
                Survival = ann["name"].split('/')[-1]
            if 'Sex' in ann["name"]:
                #ex Sex/M
                Sex = ann["name"].split('/')[-1]
            if 'Age' in ann["name"]:
                #ex Age:40
                Age = ann["name"].split(':')[-1]
            if 'age' in ann["name"]:
                #ex age:40-45
                ageRange = ann["name"].split(':')[-1].split('-')
                midAge = int((int(ageRange[0])+int(ageRange[1]))/2)
                Age = str(midAge)


        #These are a different kind of medical imaging
        if(not HasLungAnnotations):
            continue
        
        #this id is used to link to the github dataset
        imageID = data["image"]["url"].split("/")[-2]

        #build the patient entry and add it to the list
        patientDict = {}
        patientDict["ID"] = dataId
        patientDict["imageID"] = imageID
        patientDict["PneumoniaStatus"] = PneumoniaStatus
        patientDict["HasCovid"] = HasCovid
        patientDict["ICU_admission"] = ICU_admission
        patientDict["Survival"] = Survival
        patientDict["Sex"] = Sex
        patientDict["Age"] = Age
        patientInfo.append(patientDict)
        
        #save image to file
        r = requests.get(data["image"]["url"])
        outputFile = "{}_{}_image.png".format(dataId, imageID)
        open("{}/{}".format(imgDir, outputFile), 'wb').write(r.content)

        #save lung json files
        outputFile = "{}_{}_lung1.json".format(dataId, imageID)
        Lung1 = {"polygon": Lung1Info, "bounding_box": Lung1BB}
        open("{}/{}".format(imgDir, outputFile), 'w').write(json.dumps(Lung1))
        outputFile = "{}_{}_lung2.json".format(dataId, imageID)
        Lung2 = {"polygon": Lung2Info, "bounding_box": Lung2BB}
        open("{}/{}".format(imgDir, outputFile), 'w').write(json.dumps(Lung2))

#save the patient list to a csv file
infoCSVFile = os.path.join(dataPrepDir, "patientInfo.csv")
with open(infoCSVFile, "a") as f:
    f.write('ID,PneumoniaStatus,HasCovid,ICU_admission,Survival,Sex,Age\n')
    for inf in patientInfo:
        f.write("{},{},{},{},{},{},{}\n".format(inf["ID"],
            inf["PneumoniaStatus"],
            inf["HasCovid"],
            inf["ICU_admission"],
            inf["Survival"],
            inf["Sex"],
            inf["Age"]))

