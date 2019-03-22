# Import gcloud
from google.cloud import storage

# Enable Storage
client = storage.Client()

# Reference an existing bucket.
bucket = client.get_bucket('engrlabs-10f0c.appspot.com')

# Upload a local file to a new file to be created in your bucket.
# zebraBlob = bucket.get_blob('zebra.jpg')
# zebraBlob.upload_from_filename(filename='/photos/zoo/zebra.jpg')

# Download a file from your bucket.
readImageBlob = bucket.get_blob('B204-snapshot.jpg')
# giraffeBlob.download_as_string()
readImageBlob.download_to_filename("B204-snapshot.jpg")











# # importing the storage Firebase SDK to save the image to the firebase cloud storage
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage
#
# # http library to upload the images
# import requests
#
# # path of image to upload
# imgPath = "B204.jpg"
#
# # The private key is obtained from the web console - this key is for python sdk
# privateKeyPath = "engrlabs-10f0c-firebase-adminsdk-oswwf-ebef7d1bf1.json"
#
# cred = credentials.Certificate(privateKeyPath)
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'engrlabs-10f0c.appspot.com'
# })
#
# bucket = storage.bucket()
#
# # The following commented out code is to download and image from the web and store it to the cloud storage
# # imageData = requests.get(imgPath).content
#
# blob = bucket.blob('B204-snapshot.jpg')
#
# blob.do
#
# # blob.upload_from_filename(imgPath, content_type='image/jpg')
#
# print(blob.public_url)
