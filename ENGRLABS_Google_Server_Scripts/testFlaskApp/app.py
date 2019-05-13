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

# importing script containing code to save parsed data to the database
import parseNStore2DB

# importing script containing computed results to the database
import serverSideComputation

# importing software parsing script
import softwareParser

import upcomingClassesTest

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
# import firebase_admin
# from firebase_admin import credentials, firestore

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


#
# def updateDatabase(default_app, numberOfPeople, privateKeyPath):
#     # variables declartion
#     LabAvailable = ""
#     AvailableSpots = ""
#
#     # try:
#     #     # database connection setup variables
#     #     cred = credentials.Certificate(privateKeyPath)
#     #     default_app = firebase_admin.initialize_app(cred)
#     #     db = firestore.client()
#     # except ValueError:
#     #     db = firestore.client()
#
#     ref = parseNStore2DB.connectAndCreateBlankCollectionAndDB(privateKeyPath)
#
#     # writing to the database examples
#     doc_ref = ref.child('PUBLIC_DATA/DynamicData/B204')
#
#     # reading data from the database examples
#     try:
#         doc = doc_ref.get()
#         docDict = doc.to_dict()
#
#         TotalCapacity = (docDict[u"IEEELab"][u"DynamicData"][u"TotalCapacity"])
#         AvailableSpots = int(TotalCapacity) - int(numberOfPeople)
#         LabAvailable = "Available"
#         if AvailableSpots <= 0:
#             AvailableSpots = "0"
#             LabAvailable = "Full"
#         # print(u'Document data: {}'.format(doc.to_dict()))
#     except:
#         print(u'No such document found')
#
#     doc_ref.update({
#        unicode("B204") : {
#
#        }
#     })


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
    # requires importing serversideComputation file
    # updateDatabase(default_app, numberOfPeople, privateKeyPath)
    serverSideComputation.updateNumberOfPeopleAvailabilitySpots(numberOfPeople, privateKeyPath)
    # serverSideComputation.serverSideComputation(numberOfPeople)


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

    # updating the database with Upcoming class time data
    serverSideComputation.updateUpcommingClass()


    return render_template('home.html', varString="Detection Complete")


@app.route('/admin/initializeDB')
def initializeDB():
    render_template('home.html', varString="Initializing Database")
    # call initializeDB()
    # initializeDatabase.initializeDatabase()
    parseNStore2DB.initializeDatabase()
    # initializeDatabase()
    privateKeyPath = "/opt/testFlaskApp/engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
    serverSideComputation.storeSoftwareLabs2DB(privateKeyPath)
    return render_template('home.html', varString="Database Initialization Complete")

@app.route('/admin/upcomingClassTimeTest')
def upcomingClassTime():
    upcomingClassesTest.updateUpcommingClass()
    return render_template('home.html', varString="Test Data loaded to db for ---> Tuesday at 820 min of the day")


@app.route('/admin/generateSoftWaresForLabs')
def softwaresForLabs():
    privateKeyPath = "/opt/testFlaskApp/engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
    serverSideComputation.storeLabSoftware2DB(privateKeyPath)
    return render_template('home.html', varString="Generated software list")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
