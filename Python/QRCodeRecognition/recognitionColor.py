import parserTesseract as parser
import imageCutter
import unbox
import os
import time
import color

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
    
    time.sleep(5) #imagesnap is quite slow and the rest doesn t wait for it

    # CUT IMAGE IN SLICES
    imageCutter.cutImage(path+name+'.png', name)

def parse(name):
    
    initialize(name)
    
    results = []
    for i in range(0,8):
        appendix = []
        for j in range(0,8):
            #print 'image'+str(i)+'-'+str(j)
            imagePath = 'out/'+name+str(i)+'-'+str(j)+'.png'
            if color.isPiece(imagePath):
                appendix.append(1)
            else:
                appendix.append(0)
        results.append(appendix)

    return results

#printMatrix(parse('test1'))
#unBoxing('out/test3-2.png', 'test5OUT.png')