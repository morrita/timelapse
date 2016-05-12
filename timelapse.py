#!/usr/bin/python
# name: timelapse.py
# version: 1.0
# date: May 2016


import sys
import time
from datetime import datetime
import subprocess
import os

logdir = '/var/log/timelapse'
logfilename = 'timelapse.log'
logfile = logdir + "/" + logfilename

photo_width = 640
photo_height = 480
pct_quality = 100

def update_file(message,filename): # append filename with message
        with open(filename,'a') as f:
          f.write(message)


def get_date(): # return current date and time
        time = datetime.now()
        return "%02d-%02d-%04d_%02d%02d%02d" % (time.day, time.month, time.year, time.hour, time.minute, time.second)


datestr = get_date()
photofilename = datestr + ".jpg"
photoname = logdir + "/" + photofilename


subprocess.call("raspistill -mm matrix -w %d -h %d -e jpg -q %d -o %s" % (photo_width, photo_height, pct_quality, photoname), shell=True)


update_file("INFO: photograph %s created at %s \n" % (photoname,datestr), logfile)

