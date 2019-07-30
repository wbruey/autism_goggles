from PIL import Image
import csv
import logging
import pandas as pd
import numpy as np
import time
import math

total_frames=300
video_dict='C:\\ffmpeg\\bin\\'

foreground = Image.open("dot.jpg")
xs=[]
ys=[]

with open('video_gazed.csv','r') as csvfile:
    gaze_reader=csv.reader(csvfile)
    for row in gaze_reader:
        xs.append(float(row[1]))
        ys.append(float(row[2]))
    
for frame in range(1,total_frames):
    print(frame)
    with Image.open(video_dict+'thumb'+str(frame)+'.jpg') as background:
        try:
            background.paste(foreground, (int(xs[frame-1]), int(ys[frame-1])))
            background.save(video_dict+'thumb'+str(frame)+'.jpg')
        except:
            print('exception at frame')

