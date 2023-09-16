# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 18:57:44 2019

@author: seraj
"""
import time
import cv2 
from flask import Flask, render_template, Response, request


#Save data in firebase
from firebase_admin import db
import firebase_admin
import time



cred = firebase_admin.credentials.Certificate('credent.json')
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://modified-media-390212-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/")


#model for detection 
# Load the pre-trained Haar Cascade classifier for face detection
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    #cap = cv2.VideoCapture('768x576.avi')
    cam_id ='http://192.168.1.5:81/stream'
    cap = cv2.VideoCapture(cam_id)
    # Read until video is completed
    while(cap.isOpened()):
      # Capture frame-by-frame
        ret, img = cap.read()
        img1 = cv2.flip(img, 1)
        if not ret:
            break
        # Perform human detection
        # Returns a list of rectangles (x, y, width, height)
        # Use scale and winStride parameters for better detection
        humans, _ = hog.detectMultiScale(img, winStride=(8, 8), padding=(16, 16), scale=1.05)
        
        # Draw rectangles around the detected humans
        for (x, y, w, h) in humans:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        

        if ret == True:
            img = cv2.resize(img, (0,0), fx=0.8, fy=0.8) 
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else: 
            break
        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json.get('data')
    # Process the received data as needed
    ref.child('Angle').update({"item1":data})
    print("Received data:", data)
    return "Data received by Flask"
if __name__ == '__main__':
    app.run()

