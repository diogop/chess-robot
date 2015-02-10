from PIL import Image
import os

def cropImage(path):
    """Crop the image around the board and saves it under OUTPUT.png"""
    img = Image.open(path)
    width, height = img.size
    
    #actual values. Depends on webcam configuration
    left = 213
    right = width-402
    top = height-138
    bottom = 158
    
    bbox = [left, bottom, right, top]
    bbox = map(int, bbox)
    bbox = tuple(bbox)
    workingSlide = img.crop(bbox)
    workingSlide.save('OUTPUT.png')

def cutImage(path, name):
    """Cut the image in 64 pieces after cropping it around the board"""
    cropImage(path)
    img = Image.open('OUTPUT.png')
    width, height = img.size
    boxwidth = round(width/8)
    boxheight = round(height/8)

    for i in range(0, 8):
        for j in range(0,8):
            left = j*boxwidth+10
            right = (j+1)*boxwidth-10
            if right>width:
                right = width
    
            up = i*boxheight+10
            bottom = (i+1)*boxheight-10
            if bottom>height:
                bottom = height
    
            bbox = [left, up, right, bottom]
            bbox = map(int, bbox)
            bbox = tuple(bbox)
            workingSlide = img.crop(bbox)
            workingSlide.save('out/'+name+str(i)+'-'+str(j)+'.png')

#cropImage('test1.png')