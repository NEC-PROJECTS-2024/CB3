from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np
import os
import cv2
import joblib
os.environ['KERAS_BACKEND'] = 'tensorflow'


def bone_image(path):
    print(path)
    img = cv2.resize(cv2.imread(path), (350, 350) )
    img =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img=clahe.apply(img)  #enhance image
    img = cv2.Canny(img, 50, 80)  # Apply Canny Edge Detection
    if img.shape[0] !=350:
        img = cv2.resize (img , (350, 350))
    test=np.array([img])
    test_batches = test.reshape((-1, 350, 350, 1))
    test_flat = test_batches.reshape((test_batches.shape[0], -1))

    model = joblib.load('svm_model.pkl')
    pred_svm = model.predict(test_flat)
    
    print(pred_svm)
    return pred_svm
