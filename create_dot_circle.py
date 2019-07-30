from PIL import Image
import csv
import logging
import pandas as pd
import numpy as np
import time
import math

video_dict='C:\\ffmpeg\\bin\\'
foreground = Image.open("blue_dot.jpg")
xs=[]
ys=[]

for t in range(0,300):
    xs.append(350*math.cos(t*2*3.14159/300)+600)
    ys.append(250*math.sin(t*2*3.14159/300)+350)
    
for frame in range(0,300):
    with Image.open('blank.jpg') as background:
        try:
            background.paste(foreground, (int(xs[frame]), int(ys[frame])))
            background.save('dotframe'+str(frame)+'.jpg')
        except:
            print('exception at frame')