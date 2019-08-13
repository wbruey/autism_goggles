from PIL import Image
import csv
import logging
import pandas as pd
import numpy as np
import time
import math


foreground = Image.open("blue_dot.jpg")
xs=[]
ys=[]

for t in range(0,100):
    xs.append(1280/2-5)
    ys.append(720/2-5)
    
for t in range(0,50):
    xs.append(0+300-5)
    ys.append(0+200-5)

for t in range(0,50):
    xs.append(1280/2-5)
    ys.append(0+200-5)
    
for t in range(0,50):
    xs.append(1280-300-5)
    ys.append(0+200-5)

for t in range(0,50):
    xs.append(1280-300-5)
    ys.append(720/2-5)
    
for t in range(0,50):
    xs.append(1280-300-5)
    ys.append(720-200-5)
    
for t in range(0,50):
    xs.append(1280/2-5)
    ys.append(720-200-5)
 
for t in range(0,50):
    xs.append(0+300-5)
    ys.append(720-200-5)

for t in range(0,50):
    xs.append(0+300-5)
    ys.append(720/2-5)
    

for t in range(0,50):
    xs.append(0+300-5)
    ys.append(0+200-5)
    
    
for frame in range(0,550):
    with Image.open('blank.jpg') as background:
        try:
            background.paste(foreground, (int(xs[frame]), int(ys[frame])))
            background.save('thumb'+str(frame)+'.jpg')
        except:
            print('exception at frame')