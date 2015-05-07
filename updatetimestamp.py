"""Copyright 2014 Aaron Briel"""
#JUnitXML writes to file with 9 minute lag, causing Jenkins xUnit plugin reporter to fail jobs.
#This script is run as a build step to update the file

import os
import time
from stat import *

#returns a list of all the files on the current directory
files = os.listdir('.')

for f in files:
  if f.lower().endswith('xml'):
    st = os.stat(f)
    atime = st[ST_ATIME] #access time
    mtime = st[ST_MTIME] #modification time

    new_mtime = mtime + (4*3600) #new modification time

    #modify the file timestamp
    os.utime(f,(atime,new_mtime))