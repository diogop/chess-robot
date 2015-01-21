import parserTesseract as parser
import imageCutter
import os
import time

def printMatrix(matrix):
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print '\n'.join(table)

def initialize(name):
    path = os.path.dirname(os.path.realpath(__file__))+'/'
    os.chdir(path)
    #os.system('rm out/*')
    os.system('rm test1.png') #change test !!

    takePicture = os.popen('ImageSnap/imagesnap -q test1.png') #change test !!
    
    time.sleep(3) #imagesnap is quite slow and the rest doesn t wait for it

    # CUT IMAGE IN SLICES
    #imageCutter.cutImage(path+name+'.png', name)



# PARSE ALL QR CODES

def parse(name):
    
    initialize(name)
    imagePath = name+'.png'
    parsing = parser.parse(imagePath)
    
    if parsing:
        return parsing
    else:
        return 0

print(parse('test1'))