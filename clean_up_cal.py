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
    print('coppied eye gaze data cal')
    os.remove('eye_gaze_data_cal.csv')
except:
    print('unable to copy eye gaze cal data')


try:
    copyfile('video_gazed_cal.csv',path+'\\'+user_name+'_video_gazed_cal.csv')
    print('copied video gazed cal')
    os.remove('video_gazed_cal.csv')
except:
    print('unable to copy video_gazed cal data')
    
try:
    copyfile('frame_angles_cal.csv',path+'\\'+user_name+'_frame_angles_cal.csv')
    print('copied frame angles cal')
    os.remove('frame_angles_cal.csv')
except:
    print('unable to copy frame angles file')
    
try:
    copyfile('dotchase.mp4',path+'\\'+user_name+'_dotchase.mp4')
    print('copied dot chase')
    os.remove('dotchase.mp4')
except:
    print('unabel to copy dot chase video')
    
try:
    copyfile('cal_error_summary.csv',path+'\\'+user_name+'_cal_error_summary.csv')
    print('copied cal error summary')
    os.remove('cal_error_summary.csv')
except:
    print('unable to copy cal error summary')

try:
    copyfile('cal_error_data.csv',path+'\\'+user_name+'_cal_error_data.csv')
    print('copied cal error data')
    os.remove('cal_error_data.csv')
except:
    print('unable to copy cal error data')

try:
    copyfile('cal_params.pkl',path+'\\'+user_name+'_cal_params.pkl')
    print('copied cal params')
except:
    print('unable to copy cal params')
