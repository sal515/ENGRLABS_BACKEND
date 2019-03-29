# Firebase admin sdk import
import firebase_admin
# firebase realtime database import
from firebase_admin import credentials, db

import softwareParser


def connectAndCreateBlankCollectionAndDB(privateKeyPath):
    try:
        # realtime database connection setup variables
        cred = credentials.Certificate(privateKeyPath)
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://engrlabs-10f0c.firebaseio.com/'})
        ref = db.reference('/')

    except ValueError:
        # realtime database connection setup variables
        ref = db.reference('/')
        # print ref.get()

    return ref


def updateNumberOfPeopleAvailabilitySpots(numberOfPeople, privateKeyPath):
    # variables declartion
    LabAvailable = ""
    AvailableSpots = ""

    # try:
    #     # database connection setup variables
    #     cred = credentials.Certificate(privateKeyPath)
    #     default_app = firebase_admin.initialize_app(cred)
    #     db = firestore.client()
    # except ValueError:
    #     db = firestore.client()

    ref = connectAndCreateBlankCollectionAndDB(privateKeyPath)

    # writing to the database examples
    ref_B204 = ref.child('PUBLIC_DATA/DynamicData/B204')
    ref_B204_TotalCapacity = ref.child('PUBLIC_DATA/DynamicData/B204/TotalCapacity')

    #
    # # reading data from the database examples
    try:
        #     doc = ref_B204.get()
        #     docDict = doc.to_dict()
        #
        TotalCapacity = ref_B204_TotalCapacity.get()
        AvailableSpots = int(TotalCapacity) - int(numberOfPeople)
        LabAvailable = "Available"
        if AvailableSpots <= 0:
            AvailableSpots = "0"
            LabAvailable = "Full"
    except:
        print(u'No such document found')

    # print ref_B204_TotalCapacity.get()

    ref_B204.update({
        unicode("NumberOfStudentsPresent"): numberOfPeople,
        unicode("LabAvailable"): LabAvailable,
        unicode("AvailableSpots"): AvailableSpots
    })


def storeSoftwareLabs2DB():
    softLabDict = softwareParser.softwareParsingMain()

    # ============== Test Private key path =========================
    privateKeyPath = "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"

    # storing the data 2 db
    ref = connectAndCreateBlankCollectionAndDB(privateKeyPath)
    ref_softwares = ref.child('PUBLIC_DATA/Softwares')

    softKeys = dict(softLabDict).keys()

    for softKey in softKeys:
        numberOfLabs = len(list(dict(softLabDict).get(softKey)))
        # print len(list(dict(softLabDict).get(softKey)))
        # print type((dict(softLabDict).get(softKey)))

        listOflabs = list((dict(softLabDict).get(softKey)))

        # print softKey

        for lab in listOflabs:
            # print str(lab.softwareName)
            # print str(lab.classBuilding) + str(lab.classFloor) + str(lab.classRoom)
            # print unicode(str(softKey))

            # print lab.softwareName

            tempSoft = {
                unicode(str(softKey)): {
                    unicode(str(unicode(str(lab.classBuilding) + str(lab.classFloor) + str(lab.classRoom)))): {
                        unicode("Room"): unicode(str(lab.classFloor) + str(lab.classRoom)),
                        unicode("RoomCode"): unicode(str(lab.classBuilding) + str(lab.classFloor) + str(lab.classRoom)),
                        unicode("BuildingCode"): unicode(str(lab.classBuilding)),
                        unicode("floor"): unicode(str(lab.classFloor))
                    }
                }
            }

            dict(tempSoft).

    pause = 0


            # ref_softwares.update({

            # })


def serverSideComputationTest(numberOfPeople):
    # ================  Local Test paths - comment out before moving to the server  ===============
    # privateKeyPath = "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
    # ================  Test paths - comment out before moving to the server  ===============

    privateKeyPath = "/opt/testFlaskApp/engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"

    # numberOfPeople = 15
    updateNumberOfPeopleAvailabilitySpots(numberOfPeople, privateKeyPath)


# ***** Main ******
# serverSideComputation()
storeSoftwareLabs2DB()

# ***** END ******
