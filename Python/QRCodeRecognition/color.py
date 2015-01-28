import numpy as np
import cv2, cv
import time
import os

def isPiece(path):
    img = cv2.imread(path)
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    colorMin = np.array([0, 130, 130],np.uint8)
    colorMax = np.array([60, 255, 255],np.uint8)
    
    mask = cv2.inRange(hsv_img,colorMin, colorMax)
    blank_image = np.zeros(img.shape, np.uint8)
    blank_image[:,:] = (255,255,255)
    
    output = cv2.bitwise_and(blank_image, blank_image, mask = mask)
    
    #cv2.imshow("Image", mask)
    #cv2.waitKey(0)
    
    imgray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    ret = False
    
    #print len(contours)
    
    if len(contours) is not 0:
        ret = True
    
    return ret
    #cv2.imshow("Image", output)
    #cv2.waitKey(0)

#print (isPiece('testRouge.png'))