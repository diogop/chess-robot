import os

def parse(path):
    """Decode QRcode and return the value read"""
    f = os.popen('zbarimg '+path+' -q')
    out=[]
    for line in f:
        out.append(line.strip('QR-Code:').strip('\n'))

    return out