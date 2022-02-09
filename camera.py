from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
import os
import cv2
import threading, queue
import numpy as np
import time
import pyrebase
from pathlib import Path

camerastream = Blueprint('camerastream',__name__)

from .camerastream.camera_opencv import camera

global start_time

config = {
  'apiKey': "TO-BE-CONFIGURED",
  'authDomain': "TO-BE-CONFIGURED",
  'databaseURL': "TO-BE-CONFIGURED",
  'projectId': "TO-BE-CONFIGURED",
  'storageBucket': "TO-BE-CONFIGURED",
  'messagingSenderId': "TO-BE-CONFIGURED",
  'appId': "TO-BE-CONFIGURED",
  'measurementId': "TO-BE-CONFIGURED"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

auth = firebase.auth()
user = auth.sign_in_with_email_and_password("TO-BE-CONFIGURED", "TO-BE-CONFIGURED")

@camerastream.route('/camera')
def index():
    return render_template('camera.html')

def gen(camera):
    """Video streaming generator function."""
    start_time = time.time()
    print(start_time)
    print(time.ctime(start_time))
    while True:
        image = camera.get_frame()
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        if time.time() - start_time >= 5: #in seconds #5mins
                print(time.time() - start_time)
                local_time = time.ctime(start_time)
                img_name = "{}.jpg".format(local_time)
                cv2.imwrite("./project/temp.jpg", image)
                firebasepath = storage.child('images').child(img_name).put("./project/temp.jpg")
                print("{} written!".format(img_name))
                start_time = time.time() #resets timer 

@camerastream.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


