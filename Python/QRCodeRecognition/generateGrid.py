from PIL import Image
"""generates a complete image based on 64 copies of one image"""

#opens an image:
im = Image.open("qrcode.png")
#creates a new empty image, RGB mode, and size 400 by 400.
new_im = Image.new('RGB', (1600,1600))

#Here I resize my opened image, so it is no bigger than 100,100
#im.thumbnail((100,100))
#Iterate through a 4 by 4 grid with 100 spacing, to place my image
for i in xrange(0,1600,200):
    for j in xrange(0,1600,200):
        #I change brightness of the images, just to emphasise they are unique copies.
        #im=Image.eval(im,lambda x: x+(i+j)/30)
        #paste the image at location i,j:
        new_im.paste(im, (i,j))

new_im.save("result.png","PNG")