#!/usr/bin/env python

"""
vits:  Iterative threshold selection algorithm
"""

import sys
import numpy as np
from numpy import *
from v4 import vx
import math

of=' '
vxif=' '
clist = vx.vxparse(sys.argv, "if= of= t= -v -")
exec (clist)

if 'OPT' in locals():
   print ("vits: iterative threshold selection algorithm")
   print ("if= input file")
   print ("of= output file")
   print ("t=  initial threshold (default is average gray value)")
   print ("-v  (verbose) print threshold information")
   exit(0)

optv = 'OPTv' in locals()

inimage = vx.Vx(vxif)
im = inimage.i
if im.dtype != uint8 :
    print ("error: image not byte type", file=sys.stderr)
    exit(1)

# Initialize threshold value as average gray value of image
thresh = 0
total_pixel_value = 0
pixel_count = 0
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        total_pixel_value = total_pixel_value + im[y,x]
        pixel_count = pixel_count + 1
thresh = total_pixel_value / pixel_count

if 't' in locals(): 
  t_in = int(t)
  if t_in < 0 or t_in > 255:
      print("t= must be between 0 and 255", file=sys.stderr)
  else: # If threshold input is suitable, use it
	  thresh = t_in

# Create a blank histogram of 256 bins
hist = np.zeros(256)

# Compute the histogram
for y in range(im.shape[0]):
  for x in range(im.shape[1]):
    hist[im[y,x]]+=1
    
# Function to calculate average gray values between hist range
def average (low, high):
    ave = 0
    total_mult = 0
    total_pix = 0

    for i in range(low, high):
        total_mult = total_mult + (hist[i] * i)
        total_pix = total_pix + hist[i]

    ave = total_mult / total_pix
    return ave

avg1 = 0
avg2 = 0 
old1 = 1 # Differentiate to avg values to enter loop
old2 = 1

# Loop to determine threshold
while avg1 != old1 and avg2 != old2: # stop if avg1 and 2 is already equal
	# Update old average values
	old1 = avg1
	old2 = avg2
	
	# Determine the splitting value for histogram regions
	midpoint = math.ceil(thresh) # Round up
	
	# Calculate average gray values of the two regions
	avg1 = average(0, midpoint)
	avg2 = average(midpoint, 256)
	print(midpoint, avg1, avg2, thresh)
	# New thresh value
	thresh = (avg1 + avg2) / 2
  
# Print output for verbose mode
if (optv):
  print("thresh=",thresh, file=sys.stderr) 
  
# Apply threshold
for y in range(im.shape[0]):
  for x in range(im.shape[1]):
    if (im[y,x] >= thresh): 
      im[y,x] = 255
    else:
      im[y,x] = 0

vx.vfwrite(of, im)
