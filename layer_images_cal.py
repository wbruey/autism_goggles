from PIL import Image
import csv
import logging
import pandas as pd
import numpy as np
import time
import math

total_frames=550 #dot static
#total_frames=2626 #i love you man
#total_frames=350  #dot circle

width_of_dot=10

left_foreground = Image.open("red_dot.jpg")
right_foreground = Image.open("orange_dot.jpg")
combined_foreground = Image.open("yellow_dot.jpg")

left_xs=[]
left_ys=[]
right_xs=[]
right_ys=[]
combined_xs=[]
combined_ys=[]
with open('video_gazed_cal.csv','r') as csvfile:
    gaze_reader=csv.reader(csvfile)
    for row in gaze_reader:
        left_xs.append(float(row[1]))
        left_ys.append(float(row[2]))
        right_xs.append(float(row[3]))
        right_ys.append(float(row[4]))        
        combined_xs.append(float(row[5]))
        combined_ys.append(float(row[6]))
        
for frame in range(1,total_frames):
    print(frame)
    with Image.open('thumb'+str(frame)+'.jpg') as background:
        try:
        #    background.paste(left_foreground, (int(left_xs[frame-1])-int(width_of_dot/2), int(left_ys[frame-1])-int(width_of_dot/2)))
        #    background.paste(right_foreground, (int(right_xs[frame-1])-int(width_of_dot/2), int(right_ys[frame-1])-int(width_of_dot/2)))
            background.paste(combined_foreground, (int(combined_xs[frame-1])-int(width_of_dot/2), int(combined_ys[frame-1])-int(width_of_dot/2)))

            background.save('thumb'+str(frame)+'.jpg')
        except Exception as e:
            print('exception at frame')
            print(e)

