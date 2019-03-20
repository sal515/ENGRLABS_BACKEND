#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# leave the following alone
import base64
import cStringIO
import sys
import tempfile

# adding model base path  
# adding the system variables with the directories
MODEL_BASE = '/opt/models/research'
sys.path.append(MODEL_BASE)
sys.path.append(MODEL_BASE + '/object_detection')
sys.path.append(MODEL_BASE + '/slim')

# tensorflow imports
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


			 
# TEST FUNCTION BELOW:			 
def imageReadFunc():
  print("Reading Image")
  
  # read the image
  img = Image.open('/home/salman_rahman515/TestingImageRead/demo-image1.jpg')
  # img = Image.open("demo-image1.jpg")
  
  # output image
  img.show()
  
  # printFormat of image
  print(img.format)
  
  # print mode of the image
  print(img.mode)
# TEST FUNCTION ABOVE:  
  
  
  
# essentially the main () for object detection
def detect_objects_count_people(orig_image_path, new_image_path):
  
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
	if scores[i] < 0.6: continue
	cls = classes[i]
	# cls == 1 --> is for detecting people; so we only draw boxes on people in the for loop
	if cls == 1:
	  peopleCounter = peopleCounter + 1
	  draw_bounding_box_on_image(new_image, boxes[i], thickness=int(scores[i]*10)-4)
	
	new_image.save(new_image_path)
	# new_image.save('/home/salman_rahman515/TestingImageRead/personDetected.png')

  # print(peopleCounter)

  return peopleCounter

def connect2Database():
  import firebase_admin
  from firebase_admin import credentials

  cred = credentials.Certificate('path/to/serviceAccountKey.json')
  default_app = firebase_admin.initialize_app(cred)
  
  

imageReadFunc()  
client = ObjectDetector()  
detect_objects_count_people("/home/salman_rahman515/TestingImageRead/demo-image1.jpg", 
									'/home/salman_rahman515/TestingImageRead/personDetected.png')

