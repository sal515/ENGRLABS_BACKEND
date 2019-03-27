# ================================================================================
#                       Imports --> Initialize database
# ================================================================================


# file handling imports
import csv
import json
# Firebase admin sdk import
import firebase_admin
# firebase realtime database import
from firebase_admin import credentials, db


# firebase firestore database import
# from firebase_admin import credentials, firestore


# from pyparsing import unicode


# ================================================================================
#                       Initialize database
# ================================================================================


# to convert the json into objects
class LabDetails:
    def __init__(self, data):
        self.__dict__ = json.loads(data)


def connectAndCreateBlankCollectionAndDB(privateKeyPath):
    try:
        # realtime database connection setup variables
        cred = credentials.Certificate(privateKeyPath)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://engrlabs-10f0c.firebaseio.com/'})
        ref = db.reference('/')

        # examples of adding nodes of the tree
        # removing public node from the json tree: the db.reference('/') is always the same
        # users_ref = ref.child('users')
        # users_ref.set({
        #     'users': None
        # })

        # examples of removing nodes of the tree
        # users_ref = ref.child('users')
        # users_ref.set({
        #     'alanisawesome': {
        #         'date_of_birth': 'June 23, 1912',
        #         'full_name': 'Alan Turing'
        #     },
        #     'gracehop': {
        #         'date_of_birth': 'December 9, 1906',
        #         'full_name': 'Grace Hopper'
        #     }
        # })

        # cloud firestore database connection variables
        # default_app = firebase_admin.initialize_app(cred)
        # db = firestore.client()
    except ValueError:
        # realtime database connection setup variables
        ref = db.reference('/')
        # print ref.get()

    # creating a collection and a document with the lab key tag in firestore database
    # doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")
    # doc_ref.set({
    #     creating the document
    # })

    return ref


def generateJSONfromCSV(csvFilePath, jsonFilePath):
    # Open the CSV
    try:
        with open(csvFilePath, 'r') as f:
            # Change each fieldname to the appropriate field name. I know, so difficult.
            reader = csv.DictReader(f, fieldnames=(
                "TermDescr",
                "Session",
                "Subject",
                "CatalogNbr",
                "Section",
                "ComponentCode",

                "CourseTitle",
                "LocationCode",
                "InstructionModecode",

                "RoomCode",
                "BuildingCode",
                "Room",
                "StartHour",
                "StartMin",
                "StartSecond",

                "EndHour",
                "EndMin",
                "EndSecond",

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

                "EndDD",
                "EndMM",
                "EndYYYY",

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
def saveJson2Db(ref, jsonFilePath, privateKeyPath):
    # ================== Building object to save to databse =============================

    # parsing the json document to a dict
    with open(jsonFilePath, 'r') as f:
        # load json data as a dictionary
        lab_details_dict = json.load(f)

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
                    unicode(unicode("DynamicData")): {
                        u"NumberOfStudentsPresent": unicode("Sensor Not Installed"),
                        u"LabAvailable": unicode("Sensor Not Installed"),
                        u"Temperature": unicode("Sensor Not Installed"),
                        u"TotalCapacity": unicode(item["EstimatedCapacity"]),
                        u"AvailableSpots": unicode("Sensor Not Installed"),
                        u"UpcommingClass": {
                            unicode("Subject"): unicode("SubjectVal"),
                            unicode("Category"): unicode("CategoryVal"),
                            unicode("Title"): unicode("TitleVal"),
                            unicode("StartHour"): unicode("HourVal"),
                            unicode("StartMin"): unicode("MinVal"),
                            unicode("StartSec"): unicode("SecVal")
                        },
                        u"RoomCode": unicode(item["RoomCode"]),
                        u"BuildingCode": unicode(item["BuildingCode"]),
                        u"Room": unicode(item["Room"]),
                        u"LocationCode": unicode(item["LocationCode"]),
                        # u'timestamp': firestore.SERVER_TIMESTAMP
                    },
                    unicode("CurrentSemesterCourses"):
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
                            # u"CourseID": unicode(item["CourseID"]),
                            # u"TermCode": unicode(item["TermCode"]),
                            u"TermDescr": unicode(item["TermDescr"]),
                            u"Session": unicode(item["Session"]),
                            u"Subject": unicode(item["Subject"]),
                            u"CatalogNbr": unicode(item["CatalogNbr"]),
                            u"Section": unicode(item["Section"]),
                            u"ComponentCode": unicode(item["ComponentCode"]),
                            # u"ClassNbr": unicode(item["ClassNbr"]),
                            u"CourseTitle": unicode(item["CourseTitle"]),
                            u"InstructionModecode": unicode(item["InstructionModecode"]),
                            # u"MeetingPatternNbr": unicode(item["MeetingPatternNbr"]),
                            u"StartHour": unicode(item["StartHour"]),
                            u"StartMin": unicode(item["StartMin"]),
                            u"StartSecond": unicode(item["StartSecond"]),
                            # u"ClassStartTime": unicode(item["ClassStartTime"]),
                            u"EndHour": unicode(item["EndHour"]),
                            u"EndMin": unicode(item["EndMin"]),
                            u"EndSecond": unicode(item["EndSecond"]),
                            # u"ClassEndTime": unicode(item["ClassEndTime"]),
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
                            # u"StartDate(DD-MM-YYYY)": unicode(item["StartDate(DD-MM-YYYY)"]),
                            u"EndDD": unicode(item["EndDD"]),
                            u"EndMM": unicode(item["EndMM"]),
                            u"EndYYYY": unicode(item["EndYYYY"])
                            # u"EndDate(DD-MM-YYYY)": unicode(item["EndDate(DD-MM-YYYY)"])
                        }
                }
        }

        # if labKeys exit in the allLabsWithCoursesDict,
        # update the courses dict in the  allLabsWithCoursesDict with the courses in the temp dict
        if labKeys in allLabsWithCoursesDict:
            allLabsWithCoursesDict[labKeys][u"CurrentSemesterCourses"].update(tempLabDict[labKeys])

    # ================== Saving built object to databse =============================

    # getting all the labs in the allLabsWithCoursesDict
    labKeys = allLabsWithCoursesDict.keys()
    # print(labKeys)

    # creating a collection and a document with the lab key tag
    doc_ref = ref.child('PUBLIC_DATA/DynamicData')

    # loop through every lab key and saving that lab to database
    for key in labKeys:
        if key in allLabsWithCoursesDict:
            if key.isalnum():
                # if not (key == "Building CodeRoom"):
                # print(key)
                # print(type(key))
                ### doc_ref.set({
                doc_ref.update({
                    unicode(key): allLabsWithCoursesDict[key][u"DynamicData"]
                })

    # creating a collection and a document with the lab key tag
    doc_ref = ref.child('PUBLIC_DATA/CurrentSemesterCourses')

    # loop through every lab key and saving that lab to database
    for key in labKeys:
        if key in allLabsWithCoursesDict:
            if key.isalnum():
                # if not (key == "Building CodeRoom"):
                # print(key)
                # print(type(key))
                ### doc_ref.set({
                doc_ref.update({
                    unicode(key): allLabsWithCoursesDict[key]["CurrentSemesterCourses"]
                })


# store IEEE as a lab separately
def storeIEEELABDetails(ref):
    labTag = "B204"
    labTag = labTag.upper()

    building = ''
    building = building.join(char for char in labTag if char.isalpha())
    room = ''
    room = room.join(char for char in labTag if not char.isalpha())

    # print(building)
    # print(room)
    # print(''.join(char for char in labTag if char.isalpha()))
    # print(''.join(char for char in labTag if char.isnumeric()))

    # creating a collection and a document with the lab key tag
    doc_ref = ref.child('PUBLIC_DATA/DynamicData')

    # doc_ref.set({
    doc_ref.update({

        unicode(labTag): {
            u"NumberOfStudentsPresent": unicode("Sensor Not Installed"),
            u"LabAvailable": unicode("Sensor Not Installed"),
            u"Temperature": unicode("Sensor Not Installed"),
            u"TotalCapacity": unicode(10),
            u"AvailableSpots": unicode("Sensor Not Installed"),
            u"UpcommingClass": {
                unicode("Subject"): unicode("NA"),
                unicode("Category"): unicode("NA"),
                unicode("Title"): unicode("NA"),
                unicode("StartHour"): unicode("NA"),
                unicode("StartMin"): unicode("NA"),
                unicode("StartSec"): unicode("NA")
            },
            u"RoomCode": unicode(labTag),
            u"BuildingCode": unicode(building),
            u"Room": unicode(room),
            u"LocationCode": unicode("Bannex"),
            # u'timestamp': firestore.SERVER_TIMESTAMP
        }

    })


def addAlwaysAvailableLabs(ref):
    alwaysAvailableLabs = [
        {
            u"labtag": u"h807",
            u'TotalCapacity': u"20"
        },
        {
            u"labtag": u"h815",
            u"TotalCapacity": u"16"
        },
        {
            u"labtag": u"h837",
            u"TotalCapacity": u"20"
        },
        {
            u"labtag": u"h841",
            u"TotalCapacity": u"16"
        },
        {
            u"labtag": u"h849",
            u"TotalCapacity": u"20"
        },
        {
            u"labtag": u"h905",
            u"TotalCapacity": u"30"
        },
        {
            u"labtag": u"h915",
            u"TotalCapacity": u"50"
        },
        {
            u"labtag": u"h928",
            u"TotalCapacity": u"20"
        },
        {
            u"labtag": u"h931",
            u"TotalCapacity": u"50"
        },
        {
            u"labtag": u"h933",
            u"TotalCapacity": u"40"
        }
    ]

    # creating a collection and a document with the lab key tag
    CurrentSemesterCoursesDOC = ref.child('PUBLIC_DATA/CurrentSemesterCourses')
    DynamicDataDOC = ref.child('PUBLIC_DATA/DynamicData')

    for item in alwaysAvailableLabs:
        # print(item)

        labTag = item["labtag"]
        labTag = labTag.upper()

        building = ''
        building = building.join(char for char in labTag if char.isalpha())
        room = ''
        room = room.join(char for char in labTag if char.isnumeric())

        TotalCapacity = item["TotalCapacity"]
        if building == "H" or building:
            LocationCode = "SGW"
        else:
            LocationCode = ""

        DynamicDataDOC.update({

            unicode(labTag): {

                u"NumberOfStudentsPresent": unicode("Sensor Not Installed"),
                u"LabAvailable": unicode("Available"),
                u"Temperature": unicode("Sensor Not Installed"),
                u"TotalCapacity": unicode(TotalCapacity),
                u"AvailableSpots": unicode("Sensor Not Installed"),
                u"UpcommingClass": {
                    unicode("Subject"): unicode("NA"),
                    unicode("Category"): unicode("NA"),
                    unicode("Title"): unicode("NA"),
                    unicode("StartHour"): unicode("NA"),
                    unicode("StartMin"): unicode("NA"),
                    unicode("StartSec"): unicode("NA")
                },
                u"RoomCode": unicode(labTag),
                u"BuildingCode": unicode(building),
                u"Room": unicode(room),
                u"LocationCode": unicode(LocationCode),
                # u'timestamp': firestore.SERVER_TIMESTAMP
            }

        })

        CurrentSemesterCoursesDOC.update({
            unicode(labTag): {}
        })


def datamodel(db):
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")
    try:
        doc = doc_ref.get()
        testDict = doc.to_dict()

        print(testDict)
        # print(u'Document data: {}'.format(doc.to_dict()))

    except:
        print(u'No such document found')


def initializeDatabase():
    # ================  Local Test paths - comment out before moving to the server  ===============
    # privateKeyPath = "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
    # csvFilePath = "labSchedulesRevised.csv"
    # jsonFilePath = "openDataParsing.json"
    # ================  Test paths - comment out before moving to the server  ===============

    # =============== Actual server paths =======================================
    privateKeyPath = "/opt/testFlaskApp/engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
    csvFilePath = "/opt/testFlaskApp/labSchedulesRevised.csv"
    jsonFilePath = "/opt/testFlaskApp/results/openDataParsing.json"
    # =============== Actual server paths =======================================

    # Initialize the app database
    # ref = connectAndCreateBlankCollectionAndDB(default_app, privateKeyPath)
    ref = connectAndCreateBlankCollectionAndDB(privateKeyPath)
    # ref = db.reference('/')

    # Parse the CSV to JSON
    generateJSONfromCSV(csvFilePath, jsonFilePath)
    # Adding the list of labs that doesn't have classes during the semester to the same document
    addAlwaysAvailableLabs(ref)
    # Parse the JSON to Dictionaries and Store it in the database
    saveJson2Db(ref, jsonFilePath, privateKeyPath)
    # Save IEEE as a Lab in the database
    storeIEEELABDetails(ref)
    # TestPrint
    # datamodel(db)

# ***** Main ******
# initializeDatabase()
# ***** END ******

# ================================================================================
#                      END ---  Initialize database
# ================================================================================#