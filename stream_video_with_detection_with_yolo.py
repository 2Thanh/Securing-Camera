from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
from cvzone.FaceDetectionModule import FaceDetector
from upload_drive.upload import uploadFile

#Alert to telegram bot
from alert_telegram import send_img_telegram


#Save data in firebase
from firebase_admin import db
import firebase_admin
import time

cred = firebase_admin.credentials.Certificate('credent.json')
default_app = firebase_admin.initialize_app(cred, {
	'databaseURL':'https://modified-media-390212-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference("/")


global capture,rec_frame, switch, face, rec, out ,face_frame,frame_to_send
capture=0
face=0
switch=1
rec=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
    os.mkdir('./videos')
except OSError as error:
    pass

#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

cam_id ='http://192.168.1.5:81/stream'
camera = cv2.VideoCapture(0)
detector = FaceDetector()

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)


last_alert = None
def detect_face(frame):
    global net, last_alert
    img, bboxs = detector.findFaces(frame)
    if bboxs:
        # bboxInfo - "id","bbox","score","center"
        center = bboxs[0]["center"]
        
    return img, bboxs

def alert():
    global last_alert, face
    # New thread to send telegram after 15 seconds
    while(face):
        if (last_alert is None) or ((datetime.datetime.utcnow() - last_alert).total_seconds()) > 15:
            #cv2.imwrite('horse.png',frame_to_send)
            last_alert = datetime.datetime.utcnow()
            thread = Thread(target = send_img_telegram(frame_to_send))
            thread.start()
            print('Sent!!')
        
name = '' # Use to upload image which is this name to google drive

def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame,frame_to_send, face_frame, name #use to send image
    while True:
        success, frame = camera.read() 
        if success:
            if(face):                
                frame,box= detect_face(frame)
                if box:
                    face_frame = True #if has face
                    frame_to_send = frame
                else:
                    face_frame = False
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                name = "shot_{}.png".format(str(now).replace(":",''))
                cv2.imwrite(p, frame)
                
                
            
            if(rec):
                rec_frame=frame
                frame= cv2.putText(frame,"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
                #frame=cv2.flip(frame,1)
            
                
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass

@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST'])
def tasks():
    global switch,camera
    button_id = request.form['button_id']
    if button_id == "Capture":
        global capture
        capture=1
        Thread(target = uploadFile(name)).start()

    elif button_id == "Face Detection":
        global face
        face=not face 
        if(face):
            time.sleep(4)
            alert() #Canh bao khi co nguoi
                    
    elif  button_id == 'Start/Stop Recording':
            global rec, out
            rec= not rec
            if(rec):
                now=datetime.datetime.now() 
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('videos/vid_{}.avi'.format(str(now).replace(":",'')), fourcc, 20.0, (640, 480))
                #Start new thread for recording the video
                thread = Thread(target = record, args=[out,])
                thread.start()
            elif(rec==False):
                out.release()
    else:
        print('EEll')
        data = request.json.get('data')
        # Process the received data as needed
        ref.child('Angle').update({"item1":data})
        print("Received data:", data)
    return "Variable updated successfully"
    # elif request.method=='GET':
    #     return render_template('index.html')
    
    # return render_template('index.html')

@app.route('/send_data', methods=['POST'])
def receive_data():
    data = request.json.get('data')
    # Process the received data as needed
    ref.child('Angle').update({"angle1":data['newValue1'], "angle2":data['newValue2']})
    print("Received data:", data)
    return "Data received by Flask"
if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     