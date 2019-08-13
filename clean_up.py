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
import os

user_name=input('Please type unique user name: ')
path = os.getcwd()
path = path + '\\'+user_name
print(path)

try:
    os.mkdir(path)
except OSError:
    print("Creation of user folder failed")
else:
    print("successfully made user folder")

try:
    copyfile('eye_gaze_data_cal.csv',path+'\\'+user_name+'_eye_gaze_data_cal.csv')
    os.remove('eye_gaze_data_cal.csv')
except:
    print('unable to copy eye gaze cal data')

try:
    copyfile('eye_gaze_data.csv',path+'\\'+user_name+'_eye_gaze_data.csv')
    os.remove('eye_gaze_data.csv')
except:
    print('unable to copy eye_gaze_data')
    
try:
    copyfile('video_gazed_cal.csv',path+'\\'+user_name+'_video_gazed_cal.csv')
    os.remove('video_gazed_cal.csv')
except:
    print('unable to copy video_gazed cal data')
    
try:
    copyfile('video_gazed.csv',path+'\\'+user_name+'_video_gazed.csv')
    os.remove('video_gazed.csv')
except:
    print('unable to print video gazed data')
    
try:
    copyfile('frame_angles_cal.csv',path+'\\'+user_name+'_frame_angles_cal.csv')
    os.remove('frame_angles_cal.csv')
except:
    print('unable to copy frame angles file')
    
try:
    copyfile('dotchase.mp4',path+'\\'+user_name+'_dotchase.mp4')
    os.remove('dotchase.mp4')
except:
    print('unabel to copy dot chase video')
    
try:    
    copyfile('cal_params.pkl',path+'\\'+user_name+'_cal_params.pkl')
    os.remove('cal_params.pkl')
except:
    print('unable to copy cal params pickle file')

try:
    copyfile('test_i_love_you_man.mp4',path+'\\'+user_name+'_test_i_love_you_man.mp4')
    os.remove('test_i_love_you_man.mp4')
except:
    print('unable to copy test i love you man video')

