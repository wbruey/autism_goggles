# this script takes the raw gaze data outputted from the VR headset and puts it into a table
# that csv table has video frame number, x/y dot location, and that's it. 

import csv
import logging
import pandas as pd
import numpy as np
import time
import math
from shutil import copyfile
from statistics import mean
import numpy as np
import pickle

##CONSTANTS THAT DEFINE THE VIDE0 AND EYE GAZE PARAMS##################
frame_rate=23.975
video_rez_x=1280
video_rez_y=720

theta_max_angle=0.6  #0.544907   #.535  (left side of screen)
theta_min_angle=-0.616058  #-.574  (right side of screen)
theta_zero_angle=-0.00848389

phi_max_angle=0.3#0.269867 #.222    (top of screen)
phi_min_angle=-0.405853  #-.392  (bottom of screen)
phi_zero_angle=-0.0565491

input_raw_eye_data_filename='eye_gaze_data.csv'
output_pixel_coordinate_data_filename='video_gazed.csv'

########################################################################
with open('cal_params.pkl','rb') as f:  # Python 3: open(..., 'rb')
    cal_params = pickle.load(f)
    
rho_picture=cal_params[0]#1034#1078.591 
height_picture=cal_params[1]#302#283.642
rho_pic_theta_pic=cal_params[2]#646#648.095



theta_range=theta_max_angle-theta_min_angle  
phi_range=phi_max_angle-phi_min_angle
times=[]
left_xs_raw=[]
left_ys_raw=[]
left_zs_raw=[]
right_xs_raw=[]
right_ys_raw=[]
right_zs_raw=[]
combined_xs_raw=[]
combined_ys_raw=[]
combined_zs_raw=[]

frame_nums_raw=[]
blinking=[]
first_row=True
   
with open(input_raw_eye_data_filename,'r') as csvfile:

    gaze_reader=csv.reader(csvfile)
    
    #import the data from the csv
    for row in gaze_reader:
        if first_row:
            start_time=float(row[1])/1000.0
            times.append(float(0.0))

            left_xs_raw.append(float(row[4]))
            left_ys_raw.append(float(row[5]))
            left_zs_raw.append(float(row[6]))
            
            right_xs_raw.append(float(row[7]))
            right_ys_raw.append(float(row[8]))
            right_zs_raw.append(float(row[9]))            

            combined_xs_raw.append(float(row[10]))
            combined_ys_raw.append(float(row[11]))
            combined_zs_raw.append(float(row[12]))    

            frame_nums_raw.append(1)
            first_row=False
        else:
            time_of_frame=float(row[1])/1000.0-start_time
            times.append(time_of_frame)
            
            #if there is a blink use the previous value
            if float(row[4])==0 or float(row[7])==0 or float(row[10])==-1:
                
                left_xs_raw.append(left_xs_raw[-1])
                left_ys_raw.append(left_ys_raw[-1])
                left_zs_raw.append(left_zs_raw[-1])

                right_xs_raw.append(right_xs_raw[-1])
                right_ys_raw.append(right_ys_raw[-1])
                right_zs_raw.append(right_zs_raw[-1])                
                
                combined_xs_raw.append(combined_xs_raw[-1])
                combined_ys_raw.append(combined_ys_raw[-1])
                combined_zs_raw.append(combined_zs_raw[-1])
                
                
                
                blinking.append(1)
            else:
                
                left_xs_raw.append(float(row[4]))
                left_ys_raw.append(float(row[5]))
                left_zs_raw.append(float(row[6]))
                
                right_xs_raw.append(float(row[7]))
                right_ys_raw.append(float(row[8]))
                right_zs_raw.append(float(row[9]))            

                combined_xs_raw.append(float(row[10]))
                combined_ys_raw.append(float(row[11]))
                combined_zs_raw.append(float(row[12]))                    
                
                blinking.append(0)
                
            frame_nums_raw.append(math.floor(time_of_frame*frame_rate)+1)

    
#go through each row and get average gaze location for each frame
total_video_frames=frame_nums_raw[-1]
current_frame=1


left_xs_sum=0
left_ys_sum=0
left_zs_sum=0
left_xs=[]
left_ys=[]
left_zs=[]

right_xs_sum=0
right_ys_sum=0
right_zs_sum=0
right_xs=[]
right_ys=[]
right_zs=[]

combined_xs_sum=0
combined_ys_sum=0
combined_zs_sum=0
combined_xs=[]
combined_ys=[]
combined_zs=[]

frame_nums=[]
aliaser=0
for row in range(0,len(frame_nums_raw)):
    # if this row has a new frame number, write all data from previous frame to array.

    if frame_nums_raw[row] != current_frame or row==len(frame_nums_raw)-1 :
        frame_nums.append(current_frame) #append the frame number to frame list
        
        left_xs.append(left_xs_sum/aliaser) #append the average to the xs list
        left_ys.append(left_ys_sum/aliaser) #append the average to the ys list
        left_zs.append(left_zs_sum/aliaser) #append the average to the zs list
        right_xs.append(right_xs_sum/aliaser) #append the average to the xs list
        right_ys.append(right_ys_sum/aliaser) #append the average to the ys list
        right_zs.append(right_zs_sum/aliaser) #append the average to the zs list
        combined_xs.append(combined_xs_sum/aliaser) #append the average to the xs list
        combined_ys.append(combined_ys_sum/aliaser) #append the average to the ys list
        combined_zs.append(combined_zs_sum/aliaser) #append the average to the zs list
        
        aliaser=1  #this counts how many gaze data points exist for a given frame
        current_frame=frame_nums_raw[row] #re-assign current_frame to the new frame from the csv file

        left_xs_sum=left_xs_raw[row] # reset/start summing x gaze
        left_ys_sum=left_ys_raw[row] # reset/start summing y gaze
        left_zs_sum=left_zs_raw[row] # reset/start summing z gaze
        right_xs_sum=right_xs_raw[row] # reset/start summing x gaze
        right_ys_sum=right_ys_raw[row] # reset/start summing y gaze
        right_zs_sum=right_zs_raw[row] # reset/start summing z gaze
        combined_xs_sum=combined_xs_raw[row] # reset/start summing x gaze
        combined_ys_sum=combined_ys_raw[row] # reset/start summing y gaze
        combined_zs_sum=combined_zs_raw[row] # reset/start summing z gaze
        
    #otherwise continue to sum gazes from that frame to collect the average
    else:
        aliaser=aliaser+1  # this is at least the 2nd gaze data point for this frame
        left_xs_sum=left_xs_sum+left_xs_raw[row] # adding gaze data
        left_ys_sum=left_ys_sum+left_ys_raw[row]
        left_zs_sum=left_zs_sum+left_zs_raw[row]
        right_xs_sum=right_xs_sum+right_xs_raw[row] # adding gaze data
        right_ys_sum=right_ys_sum+right_ys_raw[row]
        right_zs_sum=right_zs_sum+right_zs_raw[row]        
        combined_xs_sum=combined_xs_sum+combined_xs_raw[row] # adding gaze data
        combined_ys_sum=combined_ys_sum+combined_ys_raw[row]
        combined_zs_sum=combined_zs_sum+combined_zs_raw[row]        

#now do the conversion from angle to pixel location


with open(output_pixel_coordinate_data_filename, 'w') as csvfile:
    spamwriter=csv.writer(csvfile,lineterminator='\n')
    for frame in range(0,len(frame_nums)):

        #left_xs[frame]=(theta_max_angle-left_xs[frame])*video_rez_x/theta_range
        left_xs[frame]=rho_pic_theta_pic-rho_picture*left_xs[frame]
        if left_xs[frame]<0:
            left_xs[frame]=0
        if left_xs[frame]>video_rez_x:
            left_xs[frame]=video_rez_x
           
        #left_ys[frame]=(phi_max_angle-left_ys[frame])*video_rez_y/phi_range  #### NEED TO ADD TANGENT HERE!!!!!!!!!!!!!!!!!!!!!
        left_ys[frame]=height_picture-rho_picture*math.tan(left_ys[frame])
        if left_ys[frame]<0:
            left_ys[frame]=0
        if left_ys[frame]>video_rez_y:
            left_ys[frame]=video_rez_y
        
        
        #right_xs[frame]=(theta_max_angle-right_xs[frame])*video_rez_x/theta_range
        right_xs[frame]=rho_pic_theta_pic-rho_picture*right_xs[frame]
        if right_xs[frame]<0:
            right_xs[frame]=0
        if right_xs[frame]>video_rez_x:
            right_xs[frame]=video_rez_x
           
        #right_ys[frame]=(phi_max_angle-right_ys[frame])*video_rez_y/phi_range  #### NEED TO ADD TANGENT HERE!!!!!!!!!!!!!!!!!!!!!
        right_ys[frame]=height_picture-rho_picture*math.tan(right_ys[frame])
        if right_ys[frame]<0:
            right_ys[frame]=0
        if right_ys[frame]>video_rez_y:
            right_ys[frame]=video_rez_y

        #combined_xs[frame]=(theta_max_angle-combined_xs[frame])*video_rez_x/theta_range
        combined_xs[frame]=rho_pic_theta_pic-rho_picture*combined_xs[frame]
        if combined_xs[frame]<0:
            combined_xs[frame]=0
        if combined_xs[frame]>video_rez_x:
            combined_xs[frame]=video_rez_x
           
        #combined_ys[frame]=(phi_max_angle-combined_ys[frame])*video_rez_y/phi_range  #### NEED TO ADD TANGENT HERE!!!!!!!!!!!!!!!!!!!!!
        combined_ys[frame]=height_picture-rho_picture*math.tan(combined_ys[frame])
        if combined_ys[frame]<0:
            combined_ys[frame]=0
        if combined_ys[frame]>video_rez_y:
            combined_ys[frame]=video_rez_y            

        
        spamwriter.writerow([frame,left_xs[frame],left_ys[frame],right_xs[frame],right_ys[frame],combined_xs[frame],combined_ys[frame]])
        
            

    
    
    

        
    
    