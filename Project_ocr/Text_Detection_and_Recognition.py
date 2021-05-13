#!/usr/bin/env python
# coding: utf-8

# In[2]:

import os
import numpy as np
import cv2
from imutils.object_detection import non_max_suppression
import pytesseract
import argparse
import time
import sys
from PIL import Image as im
from scipy.ndimage import interpolation as inter
from matplotlib import pyplot as plt


# In[3]:


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# In[4]:


def decode_predictions(scores, geometry):
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the
        # geometrical data used to derive potential bounding box
        # coordinates that surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]
        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability,
            # ignore it
            if scoresData[x] < args["min_confidence"]:
                continue
            # compute the offset factor as our resulting feature
            # maps will be 4x smaller than the input image
            (offsetX, offsetY) = (x * 3.9, y * 4.1)
            # extract the rotation angle for the prediction and
            # then compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            # use the geometry volume to derive the width and height
            # of the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])
    return (rects, confidences)


# In[5]:

filen = "frozen_east_text_detection.pb"
path = os.path.abspath(filen)
args = {"image":"../input/text-detection/example-images/Example-images/ex24.jpg", "east":os.path.abspath(filen), "min_confidence":0.5, "width":320, "height":320,"padding":0.0}

#args = {"image":"../input/text-detection/example-images/Example-images/ex24.jpg", "east":r"C:\Users\Acer\Desktop\New folder\Project_ocr/frozen_east_text_detection.pb", "min_confidence":0.5, "width":320, "height":320,"padding":0.0}


# In[6]:


def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,               borderMode=cv2.BORDER_REPLICATE)

    return best_angle, rotated


# In[7]:
def outputfunc(path):
    
    ##args["image"]=r"C:\Users\Ved\Documents\GitHub\Optical-Character-Recognition\OCR Samples\OCR2.jpg"
    ##image = cv2.imread(args['image'])
    image = cv2.imread(path)
    angle, rotated = correct_skew(image)
    orig = rotated.copy()
    (origH, origW) = rotated.shape[:2]
    (newW, newH) = (args["width"], args["height"])
    rW = origW / float(newW)
    rH = origH / float(newH)
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    
    
    # In[8]:
    
    
    # define the two output layer names for the EAST detector model that
    # we are interested in -- the first is the output probabilities and the
    # second can be used to derive the bounding box coordinates of text
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]
    net = cv2.dnn.readNet(args["east"]) 
    
    
    # In[9]:
    
    
    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
        (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    
    
    # In[45]:
    
    
    results = []
    output=''
    for (startX, startY, endX, endY) in boxes:
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box 
        dX = int((endX - startX) * args["padding"])
        dY = int((endY - startY) * args["padding"])
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))
        roi = orig[startY:endY, startX:endX]  
        configuration = ("-l eng --oem 1 --psm 8")
        text = pytesseract.image_to_string(roi, config=configuration)
        output = output+text
        results.append(((startX, startY, endX, endY), text))
    return output

# In[46]:



# In[47]:

