import parserTesseract as parser
import imageCutter
import unbox
import os
import time

"""Take a picture with the webcam, crop it around the board, cut the board in 64 pieces, analyse the squares (either QRcode recognition or OCR)"""

def printMatrix(matrix):
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print '\n'.join(table)

def initialize(name):
    path = os.path.dirname(os.path.realpath(__file__))+'/'
    os.chdir(path)
    os.system('rm out/*')
    os.system('rm out.txt')
    os.system('rm test1.png') #change test !!
    os.system('mkdir out')

    takePicture = os.popen('ImageSnap/imagesnap -q test1.png') #change test !!
    
    time.sleep(3) #imagesnap is quite slow and the rest doesn t wait for it

    # CUT IMAGE IN SLICES
    imageCutter.cutImage(path+name+'.png', name)
    
    unbox.batchUnbox(name)



# PARSE ALL QR CODES

def parse(name):
    
    initialize(name)
    
    QRCodes = []
    for i in range(0,8):
        appendix = []
        for j in range(0,8):
            imagePath = 'out/'+name+str(i)+'-'+str(j)+'OUT.png'
            parsing = parser.parse(imagePath)
            appendix.extend(parsing)
            if not parsing:
                appendix.append('0')
        QRCodes.append(appendix)

    return QRCodes

printMatrix(parse('test3'))