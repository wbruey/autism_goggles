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
with open('william_cal_params.pkl','rb') as f:  # Python 3: open(..., 'rb')
    params = pickle.load(f)
    
    
print(params)