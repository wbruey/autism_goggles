from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import time
import calendar


#now = float(calendar.timegm(time.gmtime()))
now = int(round(time.time() * 1000))

time.sleep(2.2)

#later = float(calendar.timegm(time.gmtime()))
later = int(round(time.time() * 1000))

print(now)
print(later)
print(later-now)