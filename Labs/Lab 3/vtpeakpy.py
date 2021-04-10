#!/usr/bin/env python

"""
vtpeakpy:  Threshold image between two most sig. hgram peaks
"""

import sys
import numpy as np
from numpy import *
from v4 import vx

of=' '
vxif=' '
clist = vx.vxparse(sys.argv, "if= of= d= -v -")
exec (clist)

if 'OPT' in locals():
   print ("vtpeakpy: threshold between hgram peaks")
   print ("if= input file")
   print ("of= output file")
   print ("d=  min dist between hgram peaks (default 10)")
   print ("-v  (verbose) print threshold information")
   exit(0)

optv = 'OPTv' in locals()

inimage = vx.Vx(vxif)
im = inimage.i
if im.dtype != uint8 :
    print ("error: image not byte type", file=sys.stderr)
    exit(1)

dist = 10   # Default distance
if 'd' in locals(): 
  dist = int(d)
  if dist < 0 or dist > 255:
      print("d= must be between 0 and 355", file=sys.stderr)
      dist = 10

# Create a blank histogram of 256 bins
hist = np.zeros(256)

# Compute the histogram
for y in range(im.shape[0]):
  for x in range(im.shape[1]):
    hist[im[y,x]]+=1
    
# Compute the Threshold
    
# Find maximum bin for entire histogram
maxbin = 0
for i in range(256):
  if hist[i] > hist[maxbin]:
    maxbin = i
    
# Find next maximum bin at distance dist below maxbin
maxb = maxbin-dist
for i in range(maxbin-dist):
  if hist[i] > hist[maxb]:
    maxb = i

# Find next maximum bin at distance dist above maxbin
maxa = maxbin + dist
for i in range(maxbin+dist,256):
  if hist[i] > hist[maxa]:
    maxa = i

# If second max found above and below take maximum
if maxa <= 255 and maxb > 0:
  if hist[maxa] > hist[maxb]:
    nxtbin = maxa
  else:
    nxtbin = maxb
    
# If only second max above was found
elif maxa <= 255:
  nxtbin = maxa
# If only second max below was found
elif maxb >= 0:
  nxtbin = maxb


# Find minimum between peaks and use as threshold
if nxtbin < maxbin:
  minbin = nxtbin
  for i in range(nxtbin,maxbin+1):
    if hist[i] < hist[minbin]:
      minbin = i
else:
  minbin = maxbin
  for i in range(maxbin,nxtbin+1):
    if hist[i] < hist[minbin]:
      minbin = i
    
thresh = minbin

# Print output for verbose mode
if (optv):
  print("maxbin=",maxbin,"nxtbin=",nxtbin,"thresh=",thresh, file=sys.stderr)
  
# Apply threshold
for y in range(im.shape[0]):
  for x in range(im.shape[1]):
    if (im[y,x] >= thresh): 
      im[y,x] = 255
    else:
      im[y,x] = 0

vx.vfwrite(of, im)
