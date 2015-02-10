import numpy as np
import cv2, cv
import time
import os

"""Crop the image of one square around the piece of paper where the text is written"""

def subimage(image, centre, theta, width, height):
    if height>width:
        add = 90
    else:
        add = 0
    rows,cols, a = image.shape
    #mapping = np.array([[np.cos(theta), -np.sin(theta), centre[0]],
    #                   [np.sin(theta), np.cos(theta), centre[1]]])
    M = cv2.getRotationMatrix2D(centre, theta+add, 1) 
    output_image = cv2.warpAffine(image,M,(cols,rows))
    return output_image

def contour(im):
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    contoursSorted = sorted(contours, key = cv2.contourArea, reverse = True)
    
    if cv2.arcLength(contoursSorted[0],True)> 1.5* cv2.arcLength(contoursSorted[1],True):
        c = contoursSorted[0]
    else:
        c = contoursSorted[2]

    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.cv.BoxPoints(rect))
    return rect, box, contours

def unBox(path, pathOut):
    im = cv2.imread(path)
    rect, box, contours = contour(im)
    #cv2.drawContours(im, [box], -1, (0,255,0), 3)
    #cv2.imshow("Image", im)

    rotated = subimage(im, rect[0], int(rect[2]), int(rect[1][0]), int(rect[1][1]))
    rect1, box1, contours1 = contour(rotated)
    #cv2.drawContours(rotated, [box1], -1, (0,255,0), 3)
    #cv2.imshow("Image", rotated)

    out = rotated[box1[1][1]+2:box1[0][1]-2, box1[0][0]+2:box1[2][0]-2]
    #cv2.imshow("Image", out)
    #cv2.waitKey(0)
    if out.size>100:
        cv2.imwrite(pathOut,out)
    else:
        os.system('cp '+path+' '+pathOut)

def batchUnbox(name):
    for i in range(0,8):
        for j in range(0,8):
            imagePath = 'out/'+name+str(i)+'-'+str(j)+'.png'
            imagePathOut = 'out/'+name+str(i)+'-'+str(j)+'OUT.png'
            try:
                unBox(imagePath, imagePathOut)
            except:
                os.system('cp '+imagePath+' '+imagePathOut)

unBox('out/test30-0.png', 'test2OUT.png')
#test('test3')