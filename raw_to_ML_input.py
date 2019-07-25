# this script takes the raw gaze data outputted from the VR headset and puts it into a table
# that csv table has video frame number, x/y dot location, and that's it. 

import csv
import logging
import pandas as pd
import numpy as np
import time
import math

frame_rate=23.98
video_rez_x=1280
video_rez_y=720


left_max_angle=.535
right_max_angle=-.574
x_range=left_max_angle-right_max_angle

top_max_angle=.222
bottom_max_angle=-.392
y_range=top_max_angle-bottom_max_angle


times=[]
xs_raw=[]
ys_raw=[]
zs_raw=[]
frame_nums_raw=[]
blinking=[]
first_row=True

with open('eye_gaze_data.csv','r') as csvfile:

    gaze_reader=csv.reader(csvfile)
    
    #import the data from the csv
    for row in gaze_reader:
        if first_row:
            start_time=float(row[1])/1000.0
            times.append(float(0.0))
            xs_raw.append(float(row[4]))
            ys_raw.append(float(row[5]))
            zs_raw.append(float(row[6]))
            frame_nums_raw.append(1)
            first_row=False
        else:
            time_of_frame=float(row[1])/1000.0-start_time
            times.append(time_of_frame)
            
            #if there is a blink use the previous value
            if row[4]==0:
                xs_raw.append(xs_raw[-1])
                ys_raw.append(ys_raw[-1])
                zs_raw.append(zs_raw[-1])
                blinking.append(1)
            else:
                xs_raw.append(float(row[4]))
                ys_raw.append(float(row[5]))
                zs_raw.append(float(row[6]))
                blinking.append(0)
                
            frame_nums_raw.append(math.floor(time_of_frame*frame_rate)+1)

    
#go through each row and get average gaze location for each frame
total_video_frames=frame_nums_raw[-1]
current_frame=1
xs_sum=0
ys_sum=0
zs_sum=0
xs=[]
ys=[]
zs=[]
frame_nums=[]
aliaser=0
for row in range(0,len(frame_nums_raw)):
    # if this row has a new frame number, write all data from previous frame to array.

    if frame_nums_raw[row] != current_frame or row==len(frame_nums_raw)-1 :
        frame_nums.append(current_frame) #append the frame number to frame list
        xs.append(xs_sum/aliaser) #append the average to the xs list
        ys.append(ys_sum/aliaser) #append the average to the ys list
        zs.append(zs_sum/aliaser) #append the average to the zs list
        aliaser=1  #this counts how many gaze data points exist for a given frame
        current_frame=frame_nums_raw[row] #re-assign current_frame to the new frame from the csv file
        xs_sum=xs_raw[row] # reset/start summing x gaze
        ys_sum=ys_raw[row] # reset/start summing y gaze
        zs_sum=zs_raw[row] # reset/start summing z gaze
    #otherwise continue to sum gazes from that frame to collect the average
    else:
        aliaser=aliaser+1  # this is at least the 2nd gaze data point for this frame
        xs_sum=xs_sum+xs_raw[row] # adding gaze data
        ys_sum=ys_sum+ys_raw[row]
        zs_sum=zs_sum+zs_raw[row]
        

#now do the conversion from angle to pixel location

with open('video_gazed.csv', 'w') as csvfile:
    spamwriter=csv.writer(csvfile,lineterminator='\n')
    for frame in range(0,len(frame_nums)):

        xs[frame]=(left_max_angle-xs[frame])*video_rez_x/x_range
        if xs[frame]<0:
            xs[frame]=0
        if xs[frame]>video_rez_x:
            xs[frame]=video_rez_x
           
        ys[frame]=(top_max_angle-ys[frame])*video_rez_y/y_range  #### NEED TO ADD TANGENT HERE!!!!!!!!!!!!!!!!!!!!!
        if ys[frame]<0:
            ys[frame]=0
        if ys[frame]>video_rez_y:
            ys[frame]=video_rez_y
        spamwriter.writerow([frame,xs[frame],ys[frame]])
        
            

    
    
    

        
    
    