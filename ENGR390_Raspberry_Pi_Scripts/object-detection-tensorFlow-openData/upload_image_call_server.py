# importing the storage Firebase SDK to save the image to the firebase cloud storage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# http library to upload the images
import requests

# importing Picamera module to capture images
from picamera import PiCamera
import time
import datetime

# FIXME
# import temperatureScript

directory = "/home/pi/object-detection-tensorFlow-openData/"


def captureImage():
    camera = PiCamera()
    camera.resolution = (2592, 1944)
    camera.capture(str(directory) + 'image.jpg')


# this function connects to the firebase storage to upload the captured image
def connect2FirebaseStorageAndSave():
    # path of image to upload
    imgPath = (str(directory) + "image.jpg")
    # The private key is obtained from the web console - this key is for python sdk
    privateKeyPath = (str(directory) + "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json")

    try:
        cred = credentials.Certificate(privateKeyPath)
        firebase_admin.initialize_app(cred, {
            'storageBucket': 'engrlabs-10f0c.appspot.com'
        })
        bucket = storage.bucket()

    except:
        bucket = storage.bucket()
    # The following commented out code is to download and image from the web and store it to the cloud storage
    # imageData = requests.get(imgPath).content
    blob = bucket.blob('image.jpg')
    blob.upload_from_filename(imgPath, content_type='image/jpg')
    print(blob.public_url)


def callServer():
    t0 = time.time()
    r = requests.get('http://34.73.44.43/rpi/detectPeople')
    t1 = time.time()
    # print("total time : " + str(t1 - t0) + "s")
    return (str(t1 - t0) + "s")


# =============== loggin ----------------------------------


# added to sudo crontab -e to run every minute
# * * * * * python /home/pi/engrLabs_390_log_generator.py

# restart the crontab after the job was installed
# sudo /etc/init.d/cron restart


def logger(processingDetails):
    # print(datetime.datetime.now().time())
    # var = datetime.datetime.now().time()
    # with open("engrLabs_390_log.txt", 'a') as outfile:
    with open(str(directory) + "engrLabs_390_log.txt", 'a') as outfile:
        # with open("/home/pi/engrLabs_390_log.txt", 'a') as outfile:
        outfile.write(str(datetime.datetime.now().time()) + " " + str(processingDetails) + "\n")


# # ------- main --------------------
try:

    logger("Started")

    # FIXME

    # # updating the temperature of B204
    # temperatureScript.temperatureReading()

    # capturing image and storing it to the cloud storage
    captureImage()

    # FIXME

    connect2FirebaseStorageAndSave()
    processingTime = callServer()
    #
    #
    #
    #
    # # processingTime = "25"
    # logger(("Ended - took " + processingTime + " s"))

except:
    logger(-1)

# ------- main --------------------
