#!/usr/bin/python
# name: timelapse.py
# version: 1.0
# date: May 2016
#
# as a pre-requisite the avconv utility needs installed to convert jpeg files into mpeg. Use the following command:
# sudo apt-get -y install libav-tools
#
#
# the following arguments are supported:
# timelapse.py process    --this merges all of the jpeg picture files in logdir and converts to mpeg
# timelapse.py clear      --this will remove all of the contents of the logdir directory
# timelapse.py shutdown   --this will 
#
#

import sys
import time
from datetime import datetime
import subprocess
import os

logdir = '/var/log/timelapse'
logfilename = 'timelapse.log'
countfilename = 'countfile.txt'
videofilename = 'timelapse.mp4'
logfile = logdir + "/" + logfilename
countfile = logdir + "/" + countfilename
videoname = logdir + "/" + videofilename

photo_width = 1920 
photo_height = 1080
pct_quality = 100
shutdown_delay = 30

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

if len(sys.argv) == 2:

    if 'process' in sys.argv[1].lower():
       update_file("INFO: started to create video %s at %s \n" % (videoname,datestr), logfile)
       fname = logdir + "/%05d.jpeg"
       subprocess.call("avconv -i %s -r 25 %s" % (fname,videoname),shell=True) 
       datestr = get_date()
       update_file("INFO: complete creating video %s at %s \n" % (videoname,datestr), logfile)

    elif 'clear' in sys.argv[1].lower():
        print ("removing the contents of folder %s \n" % (logdir))
        for the_file in os.listdir(logdir):
            file_path = os.path.join(logdir, the_file)
            try:
                if os.path.isfile(file_path):
                    print ("removing file %s \n" % (file_path))
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    elif 'shutdown' in sys.argv[1].lower():
       datestr = get_date()
       update_file("INFO: system shutdown command being issues at %s \n" % (datestr), logfile)
       update_file("INFO: now sleeping for %d seconds at %s \n" % (shutdown_delay,datestr), logfile)
       time.sleep(shutdown_delay)
       subprocess.call("sudo shutdown -h now",shell=True) 

else:

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
