#!/usr/bin/env python

""" vgrow a python region growing program
"""

import sys
from numpy  import *
from v4 import vx

of=' '
vxif=' '
clist = vx.vxparse(sys.argv,  "if= of= r= -p -v  - ")
exec (clist )

if 'OPT' in locals():
   print ("vgrow program")
   print ("if= input file")
   print ("of= output file")
   print ("r=  region pixel range")
   print ("-p  flag to select labeling scheme")
   print ("[-v] verbose mode")
   exit(0)

optp = 'OPTp' in locals()
optv = 'OPTv' in locals()

pixel_range = 0 # Initialize range variable
if 'r' in locals(): 
  print(r)
  r_in = int(r)
  if r_in < 0 or r_in > 255: # If r is not within range
      print("r= must be between 0 and 255", file=sys.stderr)
      pixel_range = 10 # Default range
  else: # If range input is suitable, use it
	  pixel_range = r_in

inimage = vx.Vx( vxif )
im = inimage.i
tmimage = vx.Vx( inimage ) 
tmimage.embedim((1,1,1,1))
tm = tmimage.i

# Clear image for output
for y in range(im.shape[0]):
    for x in range(im.shape[1]):
        im[y,x] = 0

first_pixel = 0 # Initialize variable to store value of first pixel

def setlabel (x, y, n): # n is current label
    global im, tm, first_pixel, r
    im[y,x] = n
    # 4 connected foreground 8 connected background
    if tm[y+2,x+1] > 0 and im[y+1,x] == 0 and (abs(int(tm[y+2,x+1]) - first_pixel) < pixel_range): # If pixel above current tm is foreground and not labeled in im
        setlabel(x, y+1, n)
    if tm[y,x+1] > 0 and im[y-1,x] == 0 and (abs(int(tm[y,x+1]) - first_pixel) < pixel_range): # If pixel below current tm is foreground and not labeled in im
        setlabel(x, y-1, n)
    if tm[y+1,x] > 0 and im[y,x-1] == 0 and (abs(int(tm[y+1,x]) - first_pixel) < pixel_range): # If pixel left of current tm is foreground and not labeled in im
        setlabel(x-1, y, n)
    if tm[y+1,x+2] > 0 and im[y,x+1] == 0 and (abs(int(tm[y+1,x+2]) - first_pixel) < pixel_range): # If pixel right current tm is foreground and not labeled in im
        setlabel(x+1, y, n)

l = 1 # Set initial label l to be 1
sys.setrecursionlimit(100000)
if optp:
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            if tm[y+1,x+1] > 0 and im[y,x] == 0:
                first_pixel = int(tm[y+1,x+1]) # Set first pixel value
                setlabel(x, y, first_pixel)	# Use first pixel as label
else:
    for y in range(im.shape[0]):
        for x in range(im.shape[1]):
            if tm[y+1,x+1] > 0 and im[y,x] == 0:
                first_pixel = int(tm[y+1,x+1]) # Set first pixel value
                setlabel(x, y, l)
                l = l + 1 # Increment l for next label
                if l == 255: # If at max l value
                    l = 1 # Reset l to 1


if optv:
   print (im)

inimage.write(of)
