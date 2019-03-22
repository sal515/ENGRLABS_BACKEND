# !/usr/bin/python
# -*- coding: utf-8 -*-

# from decorator import requires_auth
# from flask import redirect
# from flask import render_template
# from flask import request
# from flask import url_for
# from flask_wtf.file import FileField
# from wtforms import Form
# from wtforms import ValidationError
# from FlaskApp.testFile import testFunction
from flask import Flask
from testFile import *
from detectCountPeopleSave2DB import *

app = Flask(__name__)


@app.route('/')
def successMessage():
    print("working?")
    return testFunction()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
