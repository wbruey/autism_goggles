import tobii_research as tr
import time
import os
import csv

eye_tracker_serial_number='IS404-100108640431'

found_eyetrackers = tr.find_all_eyetrackers()

for i in range(0,len(found_eyetrackers)):
    found_eyetracker=found_eyetrackers[i]

    print("Address: " + found_eyetracker.address)
    print("Model: " + found_eyetracker.model)
    print("Name (It's OK if this is empty): " + found_eyetracker.device_name)
    print("Serial number: " + found_eyetracker.serial_number)
    if found_eyetracker.serial_number == eye_tracker_serial_number:
        my_eyetracker=found_eyetracker

combined_xs=[]
combined_ys=[]
times=[] # this is relative time
time_stamps=[]  # this is absolute time


def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    combined_xs.append(gaze_data['left_gaze_point_on_display_area'][0])
    combined_ys.append(gaze_data['left_gaze_point_on_display_area'][1])
    time_stamp=int(round(time.time() * 1000))
    time_stamps.append(time_stamp)
    times.append(time_stamp-start_time)
    
    print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

        
        


#start video
os.system("start C:\\ffmpeg\\bin\\ffplay C:\\Users\\willb\\git_repos\\autism_goggles\\man.avi -fs -autoexit")

#wait for the video to start
time.sleep(0.102)

#define start time     
start_time = int(round(time.time() * 1000))

#start subscribing to data
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

#sleep while gathering data and video is playing
time.sleep(111)

#unsubscribe from eye tracker
my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

#write data to file
with open('eye_gaze_data_tobii.csv', 'w') as csvfile:

    spamwriter=csv.writer(csvfile,lineterminator='\n')
    
    for i in range (0,len(combined_xs)):
        spamwriter.writerow(['eye_gaze',time_stamps[i],0,0,0,0,0,0,0,0,combined_xs[i],combined_ys[i],0,times[i]])