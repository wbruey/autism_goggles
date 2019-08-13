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

input_raw_eye_data_filename='eye_gaze_data_cal.csv'
########################################################################

#copyfile(input_raw_eye_data_filename,user_name+'_'+input_raw_eye_data_filename)
output_angle_frame_filename='frame_angles.csv'

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
            if row[4]==0 or row[7]==0:
                
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


#now find the cal values
theta1=mean(combined_xs[50:91])
theta2=mean(combined_xs[127:148])
theta3=mean(combined_xs[170:190])
theta4=mean(combined_xs[225:246])
theta5=mean(combined_xs[274:294])
theta6=mean(combined_xs[320:344])
theta7=mean(combined_xs[372:393])
theta8=mean(combined_xs[420:440])
theta9=mean(combined_xs[470:490])

phi1=mean(combined_ys[50:91])
phi2=mean(combined_ys[127:148])
phi3=mean(combined_ys[170:190])
phi4=mean(combined_ys[225:246])
phi5=mean(combined_ys[274:294])
phi6=mean(combined_ys[320:344])
phi7=mean(combined_ys[372:393])
phi8=mean(combined_ys[420:440])
phi9=mean(combined_ys[470:490])

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

#A=np.array([[-0.010,0.000,1.000],[0.064,1.000,0.000],[0.326,0.000,1.000]])
#B=np.array([640.000, 360.000, 980.000])
#cal_params=np.linalg.solve(A,B)
#print(cal_params)
#inverse_A=np.linalg.inv(A)
#cal_params=inverse_A.dot(B)
#print(cal_params)

A=np.array([[-1*theta1,0.0,1.0],[-1*math.tan(phi1),1.0,0.0],[-1*theta2,0.0,1.0],[-1*math.tan(phi2),1.0,0.0],
[-1*theta3,0.0,1.0],[-1*math.tan(phi3),1.0,0.0],[-1*theta4,0.0,1.0],[-1*math.tan(phi4),1.0,0.0],
[-1*theta5,0.0,1.0],[-1*math.tan(phi5),1.0,0.0],[-1*theta6,0.0,1.0],[-1*math.tan(phi6),1.0,0.0],
[-1*theta7,0.0,1.0],[-1*math.tan(phi7),1.0,0.0],[-1*theta8,0.0,1.0],[-1*math.tan(phi8),1.0,0.0]
])
B=np.array([x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7,x8,y8])

trans_A=A.transpose()
builder=trans_A.dot(A)
builder=np.linalg.inv(builder)
builder=builder.dot(trans_A)
cal_params=builder.dot(B)
print(cal_params)

with open('cal_params.pkl', 'wb') as f:
    pickle.dump(cal_params,f)



# write to file
with open(output_angle_frame_filename, 'w') as csvfile:
    spamwriter=csv.writer(csvfile,lineterminator='\n')
    for frame in range(0,len(frame_nums)):

        spamwriter.writerow([frame,left_xs[frame],left_ys[frame],right_xs[frame],right_ys[frame],combined_xs[frame],combined_ys[frame]])