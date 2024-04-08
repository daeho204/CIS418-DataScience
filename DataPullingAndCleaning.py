import os
import json
import requests
import shutil

imageDir = os.path.join("source", "all-images-v2")
dataPrepDir = "dataPrep"
imgDir = os.path.join(dataPrepDir, "images")

if os.path.isdir(dataPrepDir):
    shutil.rmtree(dataPrepDir)
os.mkdir(dataPrepDir)
os.mkdir(imgDir)

images = os.listdir(imageDir)

patientInfo = []

#with open("{}/{}".format(imageDir, images[1361]), 'r') as f:
#    data = json.load(f)
#    print(data)

#fields we don't want additional diagnosis
secondaryConditions = ('Streptococcus',
        'E.Coli',
        'Mycoplasma',
        'Pneumocystis',
        'SARS',
        'Chlamydophila',
        'Klebsiella',
        'ARDS',
        'No Finding',
        'Legionella',
        'Lipoid',
        'Influenza',
        'Varicella',
        'Lipoid pneumonia')

#fields we don't want (unreliable sourcing)
'''
Lymphocyte_count_on_admission
Leukocyte_count
Neutrophil_count
pO2_saturation
View
In_ICU_scan
PatientID
location
presents
view
outcome
Intubation
Intubated
Needed_supplemental_O2
Temperature
Extubated
'''

for x in range(0, len(images)):
    with open("{}/{}".format(imageDir, images[x]), 'r') as f:
        dataId = x + 1
        data = json.load(f)
        #skip images flagged as Ignore
        for ann in data["annotations"]:
            if 'Ignore' in ann["name"]:
                continue
            #just checking for any unknown fields
            if ann["name"] not in ("Lung", "COVID-19", "X-ray", "CT") and \
                    ann["name"] not in secondaryConditions and \
                    "Pneumonia" not in ann["name"] and \
                    "Lymphocyte_count_on_admission" not in ann["name"] and \
                    "Leukocyte_count" not in ann["name"] and \
                    "Neutrophil_count" not in ann["name"] and \
                    "View" not in ann["name"] and \
                    "ICU_admission" not in ann["name"] and \
                    "Sex" not in ann["name"] and \
                    "age" not in ann["name"] and \
                    "Age" not in ann["name"] and \
                    "In_ICU_scan" not in ann["name"] and \
                    "atientID" not in ann["name"] and \
                    "location" not in ann["name"] and \
                    "presents" not in ann["name"] and \
                    "view" not in ann["name"] and \
                    "outcome" not in ann["name"] and \
                    "Survival" not in ann["name"] and \
                    "Intubation" not in ann["name"] and \
                    "Intubated" not in ann["name"] and \
                    "Needed_supplemental_O2" not in ann["name"] and \
                    "Temperature" not in ann["name"] and \
                    "Extubated" not in ann["name"] and \
                    "pO2_saturation" not in ann["name"] and \
                    not ann["name"].isdigit() and \
                    not (ann["name"].startswith('-') and ann["name"][1:].isdigit()):
                print("{} - {}".format(x, ann))

        print("ID: {} / {}".format(dataId, len(images)))
        
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
                PneumoniaStatus = ann["name"]
            if 'COVID' in ann["name"]:
                HasCovid = True
            if 'Lung' in ann["name"]:
                HasLungAnnotations = True
                if ann["polygon"]:
                    if not Lung1Info:
                        Lung1Info = ann["polygon"]
                        Lung1BB = ann["bounding_box"]
                    else:
                        Lung2Info = ann["polygon"]
                        Lung1BB = ann["bounding_box"]
            if 'ICU_admission' in ann["name"]:
                ICU_admission = ann["name"].split('/')[-1]
            if 'Survival' in ann["name"]:
                Survival = ann["name"].split('/')[-1]
            if 'Sex' in ann["name"]:
                Sex = ann["name"].split('/')[-1]
            if 'Age' in ann["name"]:
                Age = ann["name"].split(':')[-1]
            #it looks like lowercase age is used for estimetes ex age:40-49
            if 'age' in ann["name"]:
                ageRange = ann["name"].split(':')[-1].split('-')
                midAge = int((int(ageRange[0])+int(ageRange[1]))/2)
                Age = str(midAge)


        #These are a different kind of medical imaging
        if(not HasLungAnnotations):
            continue
        
        imageID = data["image"]["url"].split("/")[-2]

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
        
        #save image
        r = requests.get(data["image"]["url"])
        outputFile = "{}_{}_image.png".format(dataId, imageID)
        open("{}/{}".format(imgDir, outputFile), 'wb').write(r.content)

        #save lungFiles
        outputFile = "{}_{}_lung1.json".format(dataId, imageID)
        Lung1 = {"polygon": Lung1Info, "bounding_box": Lung1BB}
        open("{}/{}".format(imgDir, outputFile), 'w').write(json.dumps(Lung1))
        outputFile = "{}_{}_lung2.json".format(dataId, imageID)
        Lung2 = {"polygon": Lung2Info, "bounding_box": Lung2BB}
        open("{}/{}".format(imgDir, outputFile), 'w').write(json.dumps(Lung2))

exit()
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

