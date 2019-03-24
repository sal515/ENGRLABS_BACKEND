#!/usr/bin/python
# -*- coding: utf-8 -*-
# !/bin/bash
from flask import Flask
from flask import render_template
from flask import request
import detectionHelper as detectionHelper

app = Flask(__name__)


@app.route('/')
def home():
    # return 'Hello World!'
    return render_template('home.html', varString="Homepage")


@app.route('/rpi/detectPeople')
def detectPeople():
    # call grabImage()
    # call objectDetection()
    # call save2DB()
    detectionHelper.grabImage_objectDetection_save()
    return render_template('home.html', varString="Detecting people in image ... ")


@app.route('/admin/initializeDB')
def initializeDB():
    # call initializeDB()
    return render_template('home.html', varString="Initializing Database")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
