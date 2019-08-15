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
    print("didnt create user folder")
else:
    print("Caution folder didnt exist already")

try:
    copyfile('eye_gaze_data.csv',path+'\\'+user_name+'_eye_gaze_data.csv')
    print('successfully coppied eye gaze data')
    os.remove('eye_gaze_data.csv')
except:
    print('unable to copy eye_gaze_data')
    
try:
    copyfile('video_gazed.csv',path+'\\'+user_name+'_video_gazed.csv')
    print('successfully coppied video gazed data')
    os.remove('video_gazed.csv')
except:
    print('unable to print video gazed data')
    
  
try:    
    copyfile('cal_params.pkl',path+'\\'+user_name+'_cal_params.pkl')
    print('successfully coppied cal params')
    os.remove('cal_params.pkl')
except:
    print('unable to copy cal params pickle file')

try:
    copyfile('test_i_love_you_man.mp4',path+'\\'+user_name+'_test_i_love_you_man.mp4')
    print('successfully coppied i love you man test video')
    os.remove('test_i_love_you_man.mp4')
except:
    print('unable to copy test i love you man video')

try:    
    os.remove('man_soundless.mp4')
    print('deleted soundless version')
except:
    print('unable to delete soundless version')
    
try:
    copyfile('blink_profile.csv',path+'\\'+user_name+'_blink_profile.csv')
    print('copied blink profile')
    os.remove('blink_profile.csv')
except:
    print('unable to cal blink profile')