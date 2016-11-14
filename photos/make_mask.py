from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from resizeimage import resizeimage
import numpy as np
from PIL import Image
import website.settings
import urllib
import json
import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACE_DETECTOR_PATH = BASE_DIR + '/cascades/haar-face.xml'
LEFT_EYE_DETECTOR_PATH = BASE_DIR + '/cascades/ojol.xml'
RIGHT_EYE_DETECTOR_PATH = BASE_DIR + '/cascades/ojoD.xml'

def alpha_composite(background, mask, x, y):
    background.paste(mask, (x, y), mask)
    return background
#

def detect(img_url):
    photo = cv2.imread(BASE_DIR + img_url)
    photo1 = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
    leye_cascade = cv2.CascadeClassifier(LEFT_EYE_DETECTOR_PATH)
    reye_cascade = cv2.CascadeClassifier(RIGHT_EYE_DETECTOR_PATH)
    rectsi = face_cascade.detectMultiScale(photo1, 1.3, 5)
    bg = Image.open(BASE_DIR + img_url)
    img = Image.open(BASE_DIR + '/media/happy.png')
    for (x,y,w,h) in rectsi:
        face = bg.crop((x, y, w, h))
        leye = leye_cascade(face, 1.3, 5)
        leye_x, leye_y, leye_w, leye_h = leye[0]
        reye = reye_cascade(face, 1.3, 5)
        reye_x, reye_y, reye_w, reye_h = leye[0]
        bg = alpha_composite(bg, resizeimage.resize_cover(img, [w, h]), x, y)
    bg.save(BASE_DIR + img_url)




