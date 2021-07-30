# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 18:54:48 2021

@author: DyningAida
"""

import cv2, time, os
from PIL import Image
camera = 0
video = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
faceDetection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('dataset/training.xml')
a = 0

while True:
    a = a+1
    check, frame = video.read()
    abu = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    wajah = faceDetection.detectMultiScale(abu,1.3,5)
    for(x,y,w,h) in wajah:
        #cv2.imwrite('dataset/user.'+str(id)+'.'+str(a)+'.jpg',abu[y:y+h,x:x+w])
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        id, conf = recognizer.predict(abu[y:y+h,x:x+w])
        if id > 0:
            cv2.putText(frame,str(id),(x+40,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0))
        else:
            cv2.putText(frame,'tidak dikenali',(x+40,y-10),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0))
    cv2.imshow("Face Recognition", frame)
    key = cv2.waitKey(1)
    if key==ord('a'):
        break
    #if (a>29):
    #   break
video.release()
cv2.destroyAllWindows()