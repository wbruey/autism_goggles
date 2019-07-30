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

for t in range(0,150):
    xs.append(350*math.cos(t*2*3.14159/150)+600)
    ys.append(250*math.sin(t*2*3.14159/150)+350)
    
for t in range(0,50):
    xs.append(t*1180/50+50)
    ys.append(50)

for t in range(0,50):
    xs.append(1230)
    ys.append(t*620/50+50)
    
for t in range(0,50):
    xs.append(1180-t*1180/50+50)
    ys.append(670)

for t in range(0,50):
    xs.append(50)
    ys.append(620-t*620/50+50)
    
    
for frame in range(0,350):
    with Image.open('blank.jpg') as background:
        try:
            background.paste(foreground, (int(xs[frame]), int(ys[frame])))
            background.save('thumb'+str(frame)+'.jpg')
        except:
            print('exception at frame')