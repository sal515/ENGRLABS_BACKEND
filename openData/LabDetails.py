# file handling imports
import csv
import json
# Firebase CloudStore database imports
import firebase_admin
from firebase_admin import credentials, firestore

from pyparsing import unicode

# The private key is obtained from the web console - this key is for python sdk
privateKeyPath = "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"

csvFilePath = "labSchedulesRevised.csv"
jsonFilePath = "openDataParsing.json"


# to convert the json into objects
class LabDetails:
    def __init__(self, data):
        self.__dict__ = json.loads(data)


def initializeAppDatabase():
    cred = credentials.Certificate(privateKeyPath)
    default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    # creating a collection and a document with the lab key tag
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")
    doc_ref.set({
        #     creating the document
    })

    return db


def generateJSONfromCSV(csvFilePath, jsonFilePath):
    # Open the CSV
    try:
        with open(csvFilePath, 'r') as f:
            # Change each fieldname to the appropriate field name. I know, so difficult.
            reader = csv.DictReader(f, fieldnames=("CourseID",
                                                   "TermCode",
                                                   "TermDescr",
                                                   "Session",
                                                   "Subject",
                                                   "CatalogNbr",
                                                   "Section",
                                                   "ComponentCode",
                                                   "ClassNbr",
                                                   "CourseTitle",
                                                   "LocationCode",
                                                   "InstructionModecode",
                                                   "MeetingPatternNbr",
                                                   "RoomCode",
                                                   "BuildingCode",
                                                   "Room",
                                                   "StartHour",
                                                   "StartMin",
                                                   "StartSecond",
                                                   "ClassStartTime",
                                                   "EndHour",
                                                   "EndMin",
                                                   "EndSecond",
                                                   "ClassEndTime",
                                                   "Mon",
                                                   "Tues",
                                                   "Wed",
                                                   "Thurs",
                                                   "Fri",
                                                   "Sat",
                                                   "Sun",
                                                   "StartDD",
                                                   "StartMM",
                                                   "StartYYYY",
                                                   "StartDate(DD-MM-YYYY)",
                                                   "EndDD",
                                                   "EndMM",
                                                   "EndYYYY",
                                                   "EndDate(DD-MM-YYYY)",
                                                   "EstimatedCapacity"

                                                   ))
            # Parse the CSV into JSON
            output = json.dumps([row for row in reader])
            # print("JSON parsed!")
            # f.close()
    except:
        print("Couldn't open CSV file")
    try:
        with open(jsonFilePath, 'w') as f:
            # Save the JSON
            f.write(output)
            # f.close()
            # print("JSON saved!")
    except:
        print("Couldn't save the JSON file")


# Reference: https://linuxconfig.org/how-to-parse-data-from-json-into-python
def saveJson2Db(jsonFilePath, privateKeyPath):
    # setting up databse credentials
    # cred = credentials.Certificate(privateKeyPath)
    # default_app = firebase_admin.initialize_app(cred)
    # db = firestore.client()

    # ================== Building object to save to databse =============================

    # parsing the json document to a dict
    with open(jsonFilePath, 'r') as f:
        # load json data as a dictionary
        lab_details_dict = json.load(f)
    # load the dictionary to an object -- didn't work yet
    # labDetailsObj = LabDetails(lab_details_dict)

    # variables used throughout this function
    allLabsWithCoursesDict = {}
    labKeys = {}
    labKeys = ""

    # adding the dict of labs with its details
    for item in lab_details_dict:
        labKeys = (unicode(unicode(item["BuildingCode"]) + unicode(item["Room"])))
        tempLabDict = {
            labKeys:
                {
                    unicode(unicode("DynamicDataDict")): {
                        u"NumberOfStudentsPresent": unicode("??SensorNotSetup??"),
                        u"Temperature": unicode("??SensorNotSetup??"),
                        u"TotalCapacity": unicode(item["EstimatedCapacity"]),
                        u"AvailableSpots": unicode("AvailableSpotsVal"),
                        u"UpcommingClass": {
                            unicode("Subject"): unicode("SubjectVal"),
                            unicode("Category"): unicode("CategoryVal"),
                            unicode("Title"): unicode("TitleVal"),
                            unicode("StartHour"): unicode("HourVal"),
                            unicode("StartMin"): unicode("MinVal"),
                            unicode("StartSec"): unicode("SecVal")
                        }
                    },
                    unicode("CoursesDict"):
                        {
                            unicode(unicode(item["Subject"]) + unicode(item["CatalogNbr"])): {}
                        }

                }
        }

        # if the labKeys doesn't exit, save that tmpdict to the allLabsWithCoursesDict
        if not (labKeys in allLabsWithCoursesDict):
            # tempLabDict[labKeys][unicode(item["Subject"]) + unicode(item["CatalogNbr"])].clear()
            # the update function is used to add members to the dict
            allLabsWithCoursesDict.update(tempLabDict)

    # updating the courses for a lab during the current semester
    for item in lab_details_dict:
        labKeys = (unicode(unicode(item["BuildingCode"]) + unicode(item["Room"])))
        tempLabDict = {
            labKeys:
                {
                    unicode(unicode(item["Subject"]) + unicode(item["CatalogNbr"])):
                        {
                            u"CourseID": unicode(item["CourseID"]),
                            u"TermCode": unicode(item["TermCode"]),
                            u"TermDescr": unicode(item["TermDescr"]),
                            u"Session": unicode(item["Session"]),
                            u"Subject": unicode(item["Subject"]),
                            u"CatalogNbr": unicode(item["CatalogNbr"]),
                            u"Section": unicode(item["Section"]),
                            u"ComponentCode": unicode(item["ComponentCode"]),
                            u"ClassNbr": unicode(item["ClassNbr"]),
                            u"CourseTitle": unicode(item["CourseTitle"]),
                            u"InstructionModecode": unicode(item["InstructionModecode"]),
                            u"MeetingPatternNbr": unicode(item["MeetingPatternNbr"]),
                            u"StartHour": unicode(item["StartHour"]),
                            u"StartMin": unicode(item["StartMin"]),
                            u"StartSecond": unicode(item["StartSecond"]),
                            u"ClassStartTime": unicode(item["ClassStartTime"]),
                            u"EndHour": unicode(item["EndHour"]),
                            u"EndMin": unicode(item["EndMin"]),
                            u"EndSecond": unicode(item["EndSecond"]),
                            u"ClassEndTime": unicode(item["ClassEndTime"]),
                            u"Mon": unicode(item["Mon"]),
                            u"Tues": unicode(item["Tues"]),
                            u"Wed": unicode(item["Wed"]),
                            u"Thurs": unicode(item["Thurs"]),
                            u"Fri": unicode(item["Fri"]),
                            u"Sat": unicode(item["Sat"]),
                            u"Sun": unicode(item["Sun"]),
                            u"StartDD": unicode(item["StartDD"]),
                            u"StartMM": unicode(item["StartMM"]),
                            u"StartYYYY": unicode(item["StartYYYY"]),
                            u"StartDate(DD-MM-YYYY)": unicode(item["StartDate(DD-MM-YYYY)"]),
                            u"EndDD": unicode(item["EndDD"]),
                            u"EndMM": unicode(item["EndMM"]),
                            u"EndYYYY": unicode(item["EndYYYY"]),
                            u"EndDate(DD-MM-YYYY)": unicode(item["EndDate(DD-MM-YYYY)"])
                        }
                }
        }

        # if labKeys exit in the allLabsWithCoursesDict,
        # update the courses dict in the  allLabsWithCoursesDict with the courses in the temp dict
        if labKeys in allLabsWithCoursesDict:
            allLabsWithCoursesDict[labKeys][u"CoursesDict"].update(tempLabDict[labKeys])

    # ================== Saving built object to databse =============================

    # getting all the labs in the allLabsWithCoursesDict
    labKeys = allLabsWithCoursesDict.keys()
    # print(labKeys)

    # creating a collection and a document with the lab key tag
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")

    # loop through every lab key and saving that lab to database
    for key in labKeys:
        # print(key)
        if key in allLabsWithCoursesDict:
            # doc_ref.set({
            doc_ref.update({
                unicode(key): {
                    unicode(unicode("DynamicDataDict")): allLabsWithCoursesDict[key][u"DynamicDataDict"],
                    unicode("CoursesDict"): allLabsWithCoursesDict[key]["CoursesDict"]
                }
            })


# store IEEE as a lab separately
def storeIEEELABDetails():
    # setting up databse credentials
    # cred = credentials.Certificate(privateKeyPath)
    # default_app = firebase_admin.initialize_app(cred)
    # db = firestore.client()

    # creating a collection and a document with the lab key tag
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")
    # doc_ref.set({
    doc_ref.update({

        u"IEEELab": {

            unicode(unicode("DynamicDataDict")): {
                u"NumberOfStudentsPresent": unicode("??SensorNotSetup??"),
                u"Temperature": unicode("??SensorNotSetup??"),
                u"TotalCapacity": unicode(10),
                u"AvailableSpots": unicode("AvailableSpotsVal"),
                u"UpcommingClass": {
                    unicode("Subject"): unicode("NA"),
                    unicode("Category"): unicode("NA"),
                    unicode("Title"): unicode("NA"),
                    unicode("StartHour"): unicode("NA"),
                    unicode("StartMin"): unicode("NA"),
                    unicode("StartSec"): unicode("NA")
                }
            },
            unicode("CoursesDict"): {}
        }

    })


def datamodel():
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"H821")
    try:
        doc = doc_ref.get()
        testDict = doc.to_dict()

        print(testDict[u"Subject"])
        # print(u'Document data: {}'.format(doc.to_dict()))

    except:
        print(u'No such document found')


# ***** Main ******
# Initialize the app database
db = initializeAppDatabase()
# Parse the CSV to JSON
generateJSONfromCSV(csvFilePath, jsonFilePath)
# Parse the JSON to Dictionaries and Store it in the database
saveJson2Db(jsonFilePath, privateKeyPath)
# Save IEEE as a Lab in the database
storeIEEELABDetails()


# TestPrint
# datamodel()


# ***** END ******


# =================================BELOEW: Example codes only ==========================================================
def exampleConnectSave2Db():
    # writing to the database examples
    building = "H"
    roomCode = "835"
    doc_ref = db.collection(u'sampleDa').document(u'inspiration')
    #  the .set is used to add or overwrite documents
    #  the .update function is used to update a document
    # doc_ref.set({
    # })
    # doc_ref.update({
    # })
    # doc_ref.set({
    #     unicode(building + roomCode): {
    #         u'building': unicode(unicode(building)),
    #         u'roomCode': unicode(unicode(roomCode))
    #         # u'building': u"H",
    #         # u'roomCode': u"835"
    #     }
    # })
    # reading data from the database examples
    try:
        doc = doc_ref.get()
        print(u'Document data: {}'.format(doc.to_dict()))
    except:
        print(u'No such document found')

# from collections import Counter
#
# with open(jsonFilePath, 'r') as f:
#     ##load json data as a dictionary
#     lab_details_dict = json.load(f)
# # print(len(lab_details_dict))
#
# # print(type(lab_details_dict))
# # print((lab_details_dict))
#
# d = {
#     'first': 's',
#     'second':
#         {
#             'aa': 'bb'
#         }
#
# }
#
# updatedic = {
#     'updateVar': 'updated',
#     'aa': 'zzz'
# }
# # update merges the 2 dictionaries
# d['second'].update(updatedic)
# # print(cmp(d['second'], updatedic))
# print(d['second'])
#
# # c = Counter(lab_details_dict)
# # print(dict(c.lab_details_dict))
