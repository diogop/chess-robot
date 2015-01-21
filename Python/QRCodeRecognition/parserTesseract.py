import os
import time

path = os.path.dirname(os.path.realpath(__file__))+'/'
os.chdir(path)

def getFileDataListe(path):
    with open (path, "r") as f:
        lines = f.read().splitlines()
    return lines

def parse(path):
    os.system('tesseract '+path+' out 2>/dev/null')
    text = getFileDataListe('out.txt')
    text = filter(None, text)
    return text

#print parse('test2.png')