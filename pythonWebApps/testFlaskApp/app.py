#!/usr/bin/python
# -*- coding: utf-8 -*-
# !/bin/bash
from flask import Flask
from flask import render_template
from flask import request

# importing my script with the methods to detect people and save to database
# import detectionHelper as detectionHelper

# importing my script with the methods parse the excel file and initialize the database
# import initializeDatabase as initializeDatabase

app = Flask(__name__)

# ================================================================================
#                       IMPORTS --> Detecting People
# ================================================================================


# leave the following alone
import base64
import cStringIO
import sys
import tempfile
# from pyparsing import unicode
import pyparsing

# Import gcloud
from google.cloud import storage

# Firebase admin sdk imports to connect to the databse
import firebase_admin
from firebase_admin import credentials, firestore

# adding model base path
# adding the system variables with the directories, then do the imports below
MODEL_BASE = '/opt/models/research'
sys.path.append(MODEL_BASE)
sys.path.append(MODEL_BASE + '/object_detection')
sys.path.append(MODEL_BASE + '/slim')

# tensorflow imports must be called after the system paths has been set
import numpy as np
from PIL import Image
from PIL import ImageDraw
import tensorflow as tf
from utils import label_map_util

PATH_TO_CKPT = '/opt/graph_def/frozen_inference_graph.pb'
PATH_TO_LABELS = MODEL_BASE + '/object_detection/data/mscoco_label_map.pbtxt'

content_types = {'jpg': 'image/jpeg',
                 'jpeg': 'image/jpeg',
                 'png': 'image/png'}
extensions = sorted(content_types.keys())

# ================================================================================
#                       Imports --> Initialize database
# ================================================================================


# file handling imports
import csv
import json
# Firebase CloudStore database imports
import firebase_admin
from firebase_admin import credentials, firestore


# from pyparsing import unicode


# ================================================================================
#                       Initialize database
# ================================================================================


# to convert the json into objects
class LabDetails:
    def __init__(self, data):
        self.__dict__ = json.loads(data)


def connectAndCreateBlankCollectionAndDB(default_app, privateKeyPath):
    try:
        # database connection setup variables
        cred = credentials.Certificate(privateKeyPath)
        default_app = firebase_admin.initialize_app(cred)
        db = firestore.client()
    except ValueError:
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
def saveJson2Db(db, jsonFilePath, privateKeyPath):
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
                    unicode(unicode("DynamicData")): {
                        u"NumberOfStudentsPresent": unicode("??SensorNotSetup??"),
                        u"LabAvailable": unicode("??SensorNotSetup??"),
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
                        u"LocationCode": unicode(item["LocationCode"]),
                        u'timestamp': firestore.SERVER_TIMESTAMP
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
            allLabsWithCoursesDict[labKeys][u"CurrentSemesterCourses"].update(tempLabDict[labKeys])

    # ================== Saving built object to databse =============================

    # getting all the labs in the allLabsWithCoursesDict
    labKeys = allLabsWithCoursesDict.keys()
    # print(labKeys)

    # creating a collection and a document with the lab key tag
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")

    # loop through every lab key and saving that lab to database
    for key in labKeys:
        if key in allLabsWithCoursesDict:
            if key.isalnum():
                # if not (key == "Building CodeRoom"):
                # print(key)
                # print(type(key))
                ### doc_ref.set({
                doc_ref.update({
                    unicode(key): {
                        unicode(unicode("DynamicData")): allLabsWithCoursesDict[key][u"DynamicData"],
                        unicode("CurrentSemesterCourses"): allLabsWithCoursesDict[key]["CurrentSemesterCourses"]
                    }
                })


# store IEEE as a lab separately
def storeIEEELABDetails(db):
    # setting up databse credentials
    # cred = credentials.Certificate(privateKeyPath)
    # default_app = firebase_admin.initialize_app(cred)
    # db = firestore.client()

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
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")
    # doc_ref.set({
    doc_ref.update({

        u"IEEELab": {

            unicode(unicode("DynamicData")): {
                u"NumberOfStudentsPresent": unicode("??SensorNotSetup??"),
                u"LabAvailable": unicode("??SensorNotSetup??"),
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
                },
                u"RoomCode": unicode(labTag),
                u"BuildingCode": unicode(building),
                u"Room": unicode(room),
                u"LocationCode": unicode("Bannex"),
                u'timestamp': firestore.SERVER_TIMESTAMP
            },
            unicode("CurrentSemesterCourses"): {}
        }

    })


def addAlwaysAvailableLabs(db):
    # setting up databse credentials
    # cred = credentials.Certificate(privateKeyPath)
    # default_app = firebase_admin.initialize_app(cred)
    # db = firestore.client()

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

    # # creating a collection and a document with the lab key tag
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")

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

        doc_ref.update({

            unicode(labTag): {

                unicode(unicode("DynamicData")): {
                    u"NumberOfStudentsPresent": unicode("??SensorNotSetup??"),
                    u"LabAvailable": unicode("Available"),
                    u"Temperature": unicode("??SensorNotSetup??"),
                    u"TotalCapacity": unicode(TotalCapacity),
                    u"AvailableSpots": unicode("AvailableSpotsVal"),
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
                    u'timestamp': firestore.SERVER_TIMESTAMP
                },
                unicode("CurrentSemesterCourses"): {}
            }

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
    # The private key is obtained from the web console - this key is for python sdk
    # privateKeyPath = "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
    privateKeyPath = "/opt/testFlaskApp/engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"

    csvFilePath = "/opt/testFlaskApp/labSchedulesRevised.csv"
    jsonFilePath = "/opt/testFlaskApp/results/openDataParsing.json"

    # global db
    # create default app as null
    default_app = None
    # Initialize the app database
    db = connectAndCreateBlankCollectionAndDB(default_app, privateKeyPath)
    # Parse the CSV to JSON
    generateJSONfromCSV(csvFilePath, jsonFilePath)
    # Adding the list of labs that doesn't have classes during the semester to the same document
    addAlwaysAvailableLabs(db)
    # Parse the JSON to Dictionaries and Store it in the database
    saveJson2Db(db, jsonFilePath, privateKeyPath)
    # Save IEEE as a Lab in the database
    storeIEEELABDetails(db)
    # TestPrint
    # datamodel(db)

    default_app = None


# ***** Main ******
# initializeDatabase()
# ***** END ******

# ================================================================================
#                      END ---  Initialize database
# ================================================================================#


# ================================================================================
#                       Detect People and Store to database
# ================================================================================


# objectDetector is the class with the methods to detect objects in the image
# This class is used in the <<-- called from detect_objects_count_people() func
class ObjectDetector(object):

    def __init__(self):
        self.detection_graph = self._build_graph()
        self.sess = tf.Session(graph=self.detection_graph)

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(
            label_map, max_num_classes=90, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    def _build_graph(self):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        return detection_graph

    def _load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def detect(self, image):
        image_np = self._load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)

        graph = self.detection_graph
        image_tensor = graph.get_tensor_by_name('image_tensor:0')
        boxes = graph.get_tensor_by_name('detection_boxes:0')
        scores = graph.get_tensor_by_name('detection_scores:0')
        classes = graph.get_tensor_by_name('detection_classes:0')
        num_detections = graph.get_tensor_by_name('num_detections:0')

        (boxes, scores, classes, num_detections) = self.sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})

        boxes, scores, classes, num_detections = map(
            np.squeeze, [boxes, scores, classes, num_detections])

        return boxes, scores, classes.astype(int), num_detections


# draw boxes around the detected objects func <<-- called from detect_objects_count_people() func
def draw_bounding_box_on_image(image, box, color='red', thickness=4):
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    ymin, xmin, ymax, xmax = box
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                  ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom),
               (right, top), (left, top)], width=thickness, fill=color)


# essentially the main () for object detection
def detect_objects_count_people(orig_image_path, new_image_path, client):
    # Results of the detection function are returned here
    image = Image.open(orig_image_path).convert('RGB')
    boxes, scores, classes, num_detections = client.detect(image)
    image.thumbnail((480, 480), Image.ANTIALIAS)
    # creating people counter variable
    peopleCounter = 0
    # copy of the original image is created so that boxes can be drawn on them
    new_image = image.copy()
    # looping through all the detections that occured in the image to find people that were detected
    for i in range(num_detections):
        # score is for how good is the accuracy of the detection
        if scores[i] < 0.6:
            continue
        cls = classes[i]
        # cls == 1 --> is for detecting people; so we only draw boxes on people in the for loop
        if cls == 1:
            peopleCounter = peopleCounter + 1
            draw_bounding_box_on_image(new_image, boxes[i], thickness=int(scores[i] * 10) - 4)

        new_image.save(new_image_path)
    # new_image.save('/home/salman_rahman515/TestingImageRead/personDetected.png')

    # print(peopleCounter)

    return str(peopleCounter)


def updateDatabase(default_app, numberOfPeople, privateKeyPath):
    # variables declartion
    LabAvailable = ""
    AvailableSpots = ""

    try:
        # database connection setup variables
        cred = credentials.Certificate(privateKeyPath)
        default_app = firebase_admin.initialize_app(cred)
        db = firestore.client()
    except ValueError:
        db = firestore.client()

    # writing to the database examples
    doc_ref = db.collection(u'PUBLIC_DATA').document(u"Labs")
    #  the .set is used to add or overwrite documents
    #  the .update function is used to update a document
    # doc_ref.set({
    # })

    # reading data from the database examples
    try:
        doc = doc_ref.get()
        docDict = doc.to_dict()

        TotalCapacity = (docDict[u"IEEELab"][u"DynamicData"][u"TotalCapacity"])
        AvailableSpots = int(TotalCapacity) - int(numberOfPeople)
        LabAvailable = "Available"
        if AvailableSpots <= 0:
            AvailableSpots = "0"
            LabAvailable = "Full"
        # print(u'Document data: {}'.format(doc.to_dict()))
    except:
        print(u'No such document found')

    doc_ref.update({
        u"IEEELab.DynamicData.NumberOfStudentsPresent": unicode(numberOfPeople),
        u"IEEELab.DynamicData.AvailableSpots": unicode(str(AvailableSpots)),
        u"IEEELab.DynamicData.LabAvailable": unicode(LabAvailable)
    })


def getImageFromFirestoreStorage(bucketName, imageName, downloadPath):
    # Enable Storage
    googleStorageClient = storage.Client()
    # Reference an existing bucket.
    bucket = googleStorageClient.get_bucket(bucketName)
    # Upload a local file to a new file to be created in your bucket.
    # zebraBlob = bucket.get_blob('zebra.jpg')
    # zebraBlob.upload_from_filename(filename='/photos/zoo/zebra.jpg')
    # Download a file from your bucket.
    readImageBlob = bucket.get_blob(imageName)
    readImageBlob.download_to_filename(downloadPath)
    # return readImageBlob.download_as_string()
    # Downloadint the image to be passed to the object detection function
    # return readImageBlob.download_to_file()


def grabImage_objectDetection_save():
    # Global Paths for the functions
    bucketname = 'engrlabs-10f0c.appspot.com'
    imageName = 'image.jpg'
    downloadPath = '/opt/testFlaskApp/results/downloaded_image.jpg'
    # savePath = '/home/salman_rahman515/TestingImageRead/B204.png'
    savePath = '/opt/testFlaskApp/results/processed_image.png'

    privateKeyPath = "/opt/testFlaskApp/engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"

    # creating a default app variable for the firebase database
    default_app = None

    # declarig global client object used in object detection functions
    # global client
    # download image from the firestore storage
    getImageFromFirestoreStorage(bucketname, imageName, downloadPath)
    # initialize an object detector object to be used in the object detection functions
    client = ObjectDetector()
    # numberOfPeople = detect_objects_count_people("/home/salman_rahman515/TestingImageRead/demo-image1.jpg",
    #                                              '/home/salman_rahman515/TestingImageRead/personDetected.png')
    # detect the number of people in the image downloaded
    numberOfPeople = detect_objects_count_people(downloadPath, savePath, client)
    # numberOfPeople = "10"
    # store the number of people in the image detected to the database
    updateDatabase(default_app, numberOfPeople, privateKeyPath)


# ================================================================================
#                      END ---  Detect People and Store to database
# ================================================================================


# ================================================================================
#                      REST API ROUTING FUNCTIONS
# ================================================================================

@app.route('/')
def home():
    # return 'Hello World!'
    return render_template('home.html', varString="Homepage")


@app.route('/rpi/detectPeople')
def detectPeople():
    render_template('home.html', varString="Detecting people in image... ")
    # call grabImage()
    # call objectDetection()
    # call save2DB()
    # detectionHelper.grabImage_objectDetection_save()
    grabImage_objectDetection_save()
    return render_template('home.html', varString="Detection Complete")


@app.route('/admin/initializeDB')
def initializeDB():
    render_template('home.html', varString="Initializing Database")
    # call initializeDB()
    # initializeDatabase.initializeDatabase()
    initializeDatabase()
    return render_template('home.html', varString="Database Initialization Complete")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
