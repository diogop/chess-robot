from PIL import Image
import os

def cutImage(path, name):

    img = Image.open(path)
    width, height = img.size
    boxwidth = round(width/8)
    boxheight = round(height/8)

    for i in range(0, 8):
        for j in range(0,8):
            left = j*boxwidth
            right = (j+1)*boxwidth
            if right>width:
                right = width
    
            up = i*boxheight
            bottom = (i+1)*boxheight
            if bottom>height:
                bottom = height
    
            bbox = [left, up, right, bottom]
            bbox = map(int, bbox)
            bbox = tuple(bbox)
            workingSlide = img.crop(bbox)
            workingSlide.save('out/'+name+str(i)+'-'+str(j)+'.png')