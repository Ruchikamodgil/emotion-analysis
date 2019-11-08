#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import model_from_json
from keras.preprocessing import image
from tensorflow.keras.initializers import glorot_uniform
from keras.utils import CustomObjectScope
import json


# In[2]:


#load model
with CustomObjectScope({'GlorotUniform': glorot_uniform()}):
   model = model_from_json(open("fur.json", "r").read())
#load weights
model.load_weights('fur.h5')

face_haar_cascade = cv2.CascadeClassifier(r'C:\Users\HP LAPTOP\Anaconda3\Lib\site-packages\opencv\build\etc\haarcascades\haarcascade_frontalface_default.xml')



cap=cv2.VideoCapture(0)

while True:
    ret,test_img=cap.read()# captures frame and returns boolean value and captured image
    if not ret:
        continue
    gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)

    faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)


    for (x,y,w,h) in faces_detected:
        cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)
        roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from  image
        roi_gray=cv2.resize(roi_gray,(48,48))
        img_pixels = image.img_to_array(roi_gray)
        img_pixels = np.expand_dims(img_pixels, axis = 0)
        img_pixels /= 255

        predictions = model.predict(img_pixels)

        #find max indexed array
        max_index = np.argmax(predictions[0])

        emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
        predicted_emotion = emotions[max_index]
        
        data={emotions[max_index]:predictions[0][max_index]}
        with open('json_data.txt','a') as outfile:
            json.dumps(str(data))
            outfile.write("\n")
        cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('Facial emotion analysis ',resized_img)



    if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
        break

cap.release()
cv2.destroyAllWindows


# In[ ]:




