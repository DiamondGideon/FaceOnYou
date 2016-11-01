from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
from PIL import Image
import website.settings
import urllib
import json
import cv2
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACE_DETECTOR_PATH = BASE_DIR + '/cascades/haar-face.xml'

def alpha_composite(background, mask, x, y, w, h):

    # mask = cv2.resize(mask, (w, h))
    if x < (background.shape[1]) and y < (background.shape[0]) :
        for i in range(x, min(x + w, (background.shape[1]))):
          for j in range(y, min(y + h, (background.shape[0]))):
               if not (mask[j - y, i - x, 2] == 255 and mask[j - y, i - x, 0] == 0 and mask[j - y, i - x, 1] == 0):
                   background[j,i] = mask[j - y, i - x]
    return background
#

def detect(img_url):
    photo = cv2.imread(BASE_DIR + img_url)
    # photo = cv2.resize(photo, (512, 512))
    mask = cv2.imread(BASE_DIR + '/media/happy.png')
    photo1 = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
    rectsi = face_cascade.detectMultiScale(photo1, 1.3, 5)
    for (x,y,w,h) in rectsi:
        photo = alpha_composite(photo, cv2.resize(mask, (w,h)), x, y, w, h)
    cv2.imwrite((BASE_DIR + img_url),photo)
	# update the data dictionary with the faces detected




