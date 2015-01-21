import os

def parse(path):
    f = os.popen('zbarimg '+path+' -q')
    out=[]
    for line in f:
        out.append(line.strip('QR-Code:').strip('\n'))

    return out