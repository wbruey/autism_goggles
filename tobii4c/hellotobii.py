import tobii_research as tr

import time
import os

import csv


found_eyetrackers = tr.find_all_eyetrackers()

for i in range(0,len(found_eyetrackers)):
    my_eyetracker = found_eyetrackers[i]
    print("Address: " + my_eyetracker.address)
    print("Model: " + my_eyetracker.model)
    print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
    print("Serial number: " + my_eyetracker.serial_number)

left_xs=[]
left_ys=[]

def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    left_xs.append(gaze_data['left_gaze_point_on_display_area'][0])
    left_ys.append(gaze_data['left_gaze_point_on_display_area'][1])
    
    print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

        
        
    


my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

os.system("start C:\\ffmpeg\\bin\\ffplay C:\\Users\\willb\\git_repos\\autism_goggles\\man.avi -fs -autoexit")

time.sleep(5)

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

with open('output.csv', 'w') as csvfile:

    spamwriter=csv.writer(csvfile,lineterminator='\n')
    
    for i in range (0,len(left_xs)):
        spamwriter.writerow([left_xs[i],left_ys[i]])