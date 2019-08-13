from PIL import Image
import csv
import logging
import pandas as pd
import numpy as np
import time
import math
import statistics

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



x1=1280/2-5
x2=0+300-5
x3=1280/2-5
x4=1280-300-5
x5=1280-300-5
x6=1280-300-5
x7=1280/2-5
x8=0+300-5
x9=0+300-5

y1=720/2-5
y2=0+200-5
y3=0+200-5
y4=0+200-5
y5=720/2-5
y6=720-200-5
y7=720-200-5
y8=720-200-5
y9=720/2-5

eye_dot_xs=[]
eye_dot_ys=[]
target_errors=[]     
error_frames=[]   
for frame in range(1,total_frames):
    print(frame)
      
    with Image.open('thumb'+str(frame)+'.jpg') as background:
        try:
        #    background.paste(left_foreground, (int(left_xs[frame-1])-int(width_of_dot/2), int(left_ys[frame-1])-int(width_of_dot/2)))
        #    background.paste(right_foreground, (int(right_xs[frame-1])-int(width_of_dot/2), int(right_ys[frame-1])-int(width_of_dot/2)))
            eye_dot_x=int(combined_xs[frame-1])-int(width_of_dot/2)
            eye_dot_xs.append(eye_dot_x)
            eye_dot_y=int(combined_ys[frame-1])-int(width_of_dot/2)
            eye_dot_ys.append(eye_dot_y)
            background.paste(combined_foreground, (eye_dot_x,eye_dot_y))
            background.save('thumb'+str(frame)+'.jpg')
       
            if frame>50 and frame <91:
                target_errors.append(math.sqrt((x1-eye_dot_x)**2+(y1-eye_dot_y)**2))
                error_frames.append(frame)
            if frame>127 and frame<148:
                target_errors.append(math.sqrt((x2-eye_dot_x)**2+(y2-eye_dot_y)**2))
                error_frames.append(frame)
            if frame>170 and frame<190:
                target_errors.append(math.sqrt((x3-eye_dot_x)**2+(y3-eye_dot_y)**2))
                error_frames.append(frame)
            if frame>225 and frame<246:
                target_errors.append(math.sqrt((x4-eye_dot_x)**2+(y4-eye_dot_y)**2))
                error_frames.append(frame)
            if frame>274 and frame<294:
                target_errors.append(math.sqrt((x5-eye_dot_x)**2+(y5-eye_dot_y)**2))                
                error_frames.append(frame)
            if frame>320 and frame<344:
                target_errors.append(math.sqrt((x6-eye_dot_x)**2+(y6-eye_dot_y)**2))
                error_frames.append(frame)
            if frame>372 and frame<393:
                target_errors.append(math.sqrt((x7-eye_dot_x)**2+(y7-eye_dot_y)**2))
                error_frames.append(frame)
            if frame>420 and frame<440:
                target_errors.append(math.sqrt((x8-eye_dot_x)**2+(y8-eye_dot_y)**2))
                error_frames.append(frame)
            if frame>470 and frame<490:
                target_errors.append(math.sqrt((x9-eye_dot_x)**2+(y9-eye_dot_y)**2))                
                error_frames.append(frame)
        
        except Exception as e:
            print('exception at frame')
            print(e)
        

with open('cal_error_data.csv', 'w') as csvfile:
    spamwriter=csv.writer(csvfile,lineterminator='\n')
    for i in range(0,len(error_frames)):
        spamwriter.writerow([error_frames[i],target_errors[i]])
    
with open('cal_error_summary.csv', 'w') as csvfile:
    spamwriter=csv.writer(csvfile,lineterminator='\n')
    spamwriter.writerow(['max error',max(target_errors)])
    spamwriter.writerow(['min error',min(target_errors)])
    spamwriter.writerow(['average error',statistics.mean(target_errors)])
    spamwriter.writerow(['median error',statistics.median(target_errors)])
    spamwriter.writerow(['stdev error',statistics.stdev(target_errors)])
    spamwriter.writerow(['Histogram Bins','Histogram Freq'])
    hist, bin_edges=np.histogram(target_errors)
    for i in range(0,len(hist)):
        spamwriter.writerow([bin_edges[i],hist[i]])

print(' ')
print('Calibration Error Metrics')
print('max error: '+ str(max(target_errors)))
print('min error: '+ str(min(target_errors)))
print('average error: '+ str(statistics.mean(target_errors)))
print('stdev error: '+ str(statistics.stdev(target_errors)))

wait=input('press enter after acknowledging these error stats.')