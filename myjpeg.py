#!/usr/bin/env python

from math import ceil
from statistics import mean
import logging


#check i, j each time

def ppm_tokenize(stream):
    
    for i in stream:
        split = i.split()
        for x in split:
            if "#" in x:
                break
            yield x
            
            
def ppm_load(stream):
    
    temp = [0,0,0]
    res = []
    line = []
    itere = ppm_tokenize(stream)
   
    _ = next(itere)
   
    wedth = next(itere)
    w = int(wedth)
   
   
    height = next(itere)
    h = int(height)
   
    for i, t in enumerate(itere):
        logging.debug("{} {}".format(i, t))
        if (i/3)%w == 0 and i != 0:
            res.append(line)
            line = []
        
        if i%3 == 0:
            try:
                temp[0] = int(t)
            except ValueError:
                temp[0] = 0
        if i%3 == 1:
            temp[1] = int(t)
        if i%3 == 2:
            temp[2] = int(t)
            line.append(tuple(temp))
    
    return (h, w, res)
    
    
def ppm_save(w, h, img, output):
    
    
    pass
    #ask ta on what i have to do
    #save image as matrix so that it could be opened as ppm file
    #open file and rewrite with rgb values
def RGB2YCbCr(r, g, b):
    Y = 0 + 0.299*r + 0.587*g + 0.114*b
    cb = 128 - 0.168736*r - 0.331264*g + 0.5*b
    cr = 128 + 0.5*r - 0.418688*g - 0.081312*b
    
    return (Y, cb, cr)

def YCbCr2RGB(Y, cb, cr):
    R = Y + 1.402*(cr - 128)
    G = Y - 0.344136 * (cb - 128) - 0.714136 * (cr-128)
    B = Y + 1.772*(cb-128)
    
    return (R, G, B)


def img_RGB2YCbCr(img):
    
    h = len(img)
    if h !=0:
        w = len(img[0])
    else:
        return [[],[],[]]
    
    Y = [ [ None for y in range( w ) ]
             for x in range( h ) ]
    cb =  [ [ None for y in range( w ) ]
             for x in range( h ) ]
    cr =  [ [ None for y in range( w ) ]
             for x in range( h ) ]
    
    for j in range(len(img)):
        for i in range(len(img[j])):
            Y[i][j], cb[i][j], cr[i][j] = RGB2YCbCr(**img[i][j])
    
    return [Y, cb, cr]
            
def img_YCbCr2RGB(Y, cb, cr):
    
    h = len(Y)
    if h !=0:
        w = len(Y[0])
    else:
        return [[],[],[]]
    
    img =  [ [ None for y in range( w ) ]
             for x in range( h ) ]
    
    for j in range(len(img)):
        for i in range(len(img[j])):
            img[i][j]= img_YCbCr2RGB(Y[i][j], cb[i][j], cr[i][j])
            
    return img
   
def average(C):
    return mean([mean(x) for x in C])
         
            
def subsamlpling(w, h, C, a, b):
    
    
    width = ceil(float(w)/float(a))
    height = ceil(float(h)/float(b))
   
    mat = [ [ None for y in range( width ) ]
             for x in range( height ) ]
    
    for j in range(width):
        for i in range(height):
            x_beg = j * a
            x_end = min(x_beg + (a-1), w-1)
            y_beg = i * b
            y_end = min(y_beg + (b-1), h-1)
            mat[j][i] = average(C[x_beg:x_end][y_beg:y_end])
            
    return mat
            
def extrapolate(w, h, C, a, b):
    mat = [ [ None for y in range( w ) ]
             for x in range( h ) ]
    
    for j in range(len(C)):
        for i in range(len(C[j])):
            x_beg = j * a
            x_end = min(x_beg + (a-1), w-1)
            y_beg = i * b
            y_end = min(y_beg + (b-1), h-1)
            for x in range(x_beg, x_end):
                for y in range(y_beg, y_end):
                    mat[x][y] = C[j][i]
                    
    return mat
    
def block_splitting(w, h, C):
    nb_block_w = w/8
    nb_block_h = h/8



#############################################################################################################
if __name__ == "__main__":
    import sys
    import getopt

    logging.basicConfig(format='%(levelname)-5s : %(message)s',level=logging.INFO)

    def usage():
        print(f"""
    Usage : {sys.argv[0]}
                [--help  | -h] 
                [--debug | -d]
            """) 

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hd', ['help','debug'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(2)
        elif opt in ('-d','--debug'):
            logging.getLogger().setLevel(logging.DEBUG)
    
    # 1
    with open('test.ppm') as stream:
        for token in ppm_tokenize(stream):
            logging.info(f"#1 : {token}")
    
    # 2
    with open('test.ppm') as stream:   
        img=ppm_load(stream)
        for i in range(img[0]):
            logging.info(f"#2: {img[2][i]}")

    
    # 16
    C = [
            [ 1,  2,  3,  4,  5,  6,  7,  8,  9, 10],
            [ 2,  3,  4,  5,  6,  7,  8,  9, 10,  1],
            [ 3,  4,  5,  6,  7,  8,  9, 10,  1,  2],
            [ 4,  5,  6,  7,  8,  9, 10,  1,  2,  3],
            [ 5,  6,  7,  8,  9, 10,  1,  2,  3,  4],
            [ 6,  7,  8,  9, 10,  1,  2,  3,  4,  5],
            [ 7,  8,  9, 10,  1,  2,  3,  4,  5,  6],
            [ 8,  9, 10,  1,  2,  3,  4,  5,  6,  7],
            [ 9, 10,  1,  2,  3,  4,  5,  6,  7,  8],
        ]
    block_splitting(len(C[0]),len(C),C)

