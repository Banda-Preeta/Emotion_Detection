from urllib.request import url2pathname

from flask import url_for
import imutils
import cv2
from keras.models import load_model
import numpy as np
import argparse
import matplotlib.pyplot as plt
from tensorflow.keras.utils import img_to_array
import json

detection_model_path = '../Models/haarcascade_frontalface_default.xml'
#emotion_model_path = 'models/new'
emotion_model_path='../Models/grayscalemodel_1_new.hdf5'

face_detection = cv2.CascadeClassifier(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
EMOTIONS = ["angry" ,"confident","confused","contempt","crying","disgust","fear", "happy","neutral", "sad","shy" ,"sleepy","surprised"]






class Video(object):
    def __init__(self) -> None:
        self.video=cv2.VideoCapture(0)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()
        frame = imutils.resize(frame,width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detection.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags=cv2.CASCADE_SCALE_IMAGE)
        canvas = np.zeros((450, 500, 3), dtype="uint8")
        frameClone = frame.copy()
        jsn={"detected": False, "pred": {"angry": 0, "confident": 0, "confused": 0, "contempt": 0, "crying": 0, "disgust": 0, "fear": 0, "happy": 0, "neutral": 0, "sad": 0, "shy": 0, "sleepy": 0, "surprised": 0}}
        
        if len(faces)>0 :

            faces = sorted(faces, reverse=True,
            key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces

            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]
            #print(preds)
            jsn['detected']=True
            for i,value in enumerate(EMOTIONS):
                jsn['pred'][value]=eval(str(preds[i]))
            
            for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                
              

                w = int(prob * 300)
                cv2.putText(frameClone, label, (fX, fY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH),
                              (0, 0, 255), 2)
        with open('static/result/result.json', 'w') as f:
            json.dump(jsn, f)

        ret,jpg=cv2.imencode('.jpg',frameClone)
        return jpg.tobytes()