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
countfilename = 'countfile.txt'
logfile = logdir + "/" + logfilename
countfile = logdir + "/" + countfilename

photo_width = 640
photo_height = 480
pct_quality = 100

def update_file(message,filename): # append filename with message
    with open(filename,'a') as f:
        f.write(message)


def get_date(): # return current date and time
    time = datetime.now()
    return "%02d-%02d-%04d_%02d%02d%02d" % (time.day, time.month, time.year, time.hour, time.minute, time.second)


def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


datestr = get_date()

if os.path.isfile(countfile): 
    with open(countfile, 'r') as f:
        firstLine = f.readline()

    firstList = firstLine.split()
    firstNum = firstList[0]

    if representsInt(firstNum):
        firstInt = int(firstNum)
        update_file("Temp file %s  contains number  %s \n" % (countfile, str(firstInt)), logfile)
        firstInt += 1

        os.remove (countfile)
        update_file(str(firstInt),countfile)

        update_file("INFO: Updated countfile %s  with number  %s \n" % (countfile, str(firstInt)), logfile)


else:

    firstInt = 1
    update_file("Creating countfile %s at %s \n" % (countfile, datestr), logfile)
    update_file(str(firstInt),countfile)

datestr = get_date()
photofilename = str(firstInt).zfill(5) + ".jpeg"
photoname = logdir + "/" + photofilename

subprocess.call("raspistill -mm matrix -w %d -h %d -e jpg -q %d -o %s" % (photo_width, photo_height, pct_quality, photoname), shell=True)

update_file("INFO: photograph %s created at %s \n" % (photoname,datestr), logfile)
