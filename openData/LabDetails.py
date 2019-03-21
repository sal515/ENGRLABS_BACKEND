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
    # setting up credentials
    cred = credentials.Certificate(privateKeyPath)
    default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    with open(jsonFilePath, 'r') as f:
        # load json data as a dictionary
        lab_details_dict = json.load(f)
    # load the dictionary to an object -- didn't work yet
    # labDetailsObj = LabDetails(lab_details_dict)

    for item in lab_details_dict:
        doc_ref = db.collection(u'PUBLIC_DATA').document(
            unicode(unicode(item["BuildingCode"]) + unicode(item["Room"])))
        doc_ref.set({
            unicode(unicode("DynamicData")): {
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

                },
                u"RoomCode": unicode(item["RoomCode"]),
                u"BuildingCode": unicode(item["BuildingCode"]),
                u"Room": unicode(item["Room"]),
                u"LocationCode": unicode(item["LocationCode"])
            },
            unicode(unicode(item["Subject"]) + unicode(item["CatalogNbr"])): [
                # {
                # u"CourseID": unicode(item["CourseID"]),
                # u"TermCode": unicode(item["TermCode"]),
                # u"TermDescr": unicode(item["TermDescr"]),
                # u"Session": unicode(item["Session"]),
                # u"Subject": unicode(item["Subject"]),
                # u"CatalogNbr": unicode(item["CatalogNbr"]),
                # u"Section": unicode(item["Section"]),
                # u"ComponentCode": unicode(item["ComponentCode"]),
                # u"ClassNbr": unicode(item["ClassNbr"]),
                # u"CourseTitle": unicode(item["CourseTitle"]),
                # u"InstructionModecode": unicode(item["InstructionModecode"]),
                # u"MeetingPatternNbr": unicode(item["MeetingPatternNbr"]),
                # u"StartHour": unicode(item["StartHour"]),
                # u"StartMin": unicode(item["StartMin"]),
                # u"StartSecond": unicode(item["StartSecond"]),
                # u"ClassStartTime": unicode(item["ClassStartTime"]),
                # u"EndHour": unicode(item["EndHour"]),
                # u"EndMin": unicode(item["EndMin"]),
                # u"EndSecond": unicode(item["EndSecond"]),
                # u"ClassEndTime": unicode(item["ClassEndTime"]),
                # u"Mon": unicode(item["Mon"]),
                # u"Tues": unicode(item["Tues"]),
                # u"Wed": unicode(item["Wed"]),
                # u"Thurs": unicode(item["Thurs"]),
                # u"Fri": unicode(item["Fri"]),
                # u"Sat": unicode(item["Sat"]),
                # u"Sun": unicode(item["Sun"]),
                # u"StartDD": unicode(item["StartDD"]),
                # u"StartMM": unicode(item["StartMM"]),
                # u"StartYYYY": unicode(item["StartYYYY"]),
                # u"StartDate(DD-MM-YYYY)": unicode(item["StartDate(DD-MM-YYYY)"]),
                # u"EndDD": unicode(item["EndDD"]),
                # u"EndMM": unicode(item["EndMM"]),
                # u"EndYYYY": unicode(item["EndYYYY"]),
                # u"EndDate(DD-MM-YYYY)": unicode(item["EndDate(DD-MM-YYYY)"])
                # }
            ]
        })


from collections import Counter

with open(jsonFilePath, 'r') as f:
    ##load json data as a dictionary
    lab_details_dict = json.load(f)
# print(len(lab_details_dict))

# print(type(lab_details_dict))
# print((lab_details_dict))

d = {
    'first': 's',
    'second':
        {
            'aa': 'bb'
        }
}

updatedic = {
    'updateVar': 'updated',
    'aa': 'zzz'
}
# update merges the 2 dictionaries
d['second'].update(updatedic)
print(cmp(d['second'], updatedic))

print(d['second'])


# c = Counter(lab_details_dict)
# print(dict(c.lab_details_dict))


def exampleConnectSave2Db():
    cred = credentials.Certificate(privateKeyPath)
    default_app = firebase_admin.initialize_app(cred)
    db = firestore.client()

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

# generateJSONfromCSV(csvFilePath, jsonFilePath)

# saveJson2Db(jsonFilePath, privateKeyPath)
