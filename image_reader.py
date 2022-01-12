import easyocr
import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
import os

class ImageReader:
    def __init__(self):

        self.reader = easyocr.Reader(['en', 'tl'], recog_network='english_g2', gpu=True)

    def read_img(self, path):
        result = self.reader.readtext(path, detail = 1, paragraph=True)

        img = Image.open(path)
        img_arr = np.array(img)
        spacer = 100
        font = cv2.FONT_HERSHEY_SIMPLEX

        for detection in result:
            top_left = tuple(detection[0][0])
            bottom_right = tuple(detection[0][2])
            text = detection[1]
            img = cv2.rectangle(img_arr ,top_left,bottom_right,(0,255,0),3)
            img = cv2.putText(img_arr ,text,(20,spacer), font, 0.5,(0,255,0),2,cv2.LINE_AA)
            spacer+=15

        plt.imshow(img_arr)
        plt.show()

        message = [row[1] for row in result]
        message = ' '.join(message)

        return message