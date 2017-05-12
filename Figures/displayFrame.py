import sys	
import numpy as np

from struct import unpack

inputFile = sys.argv[1]

with open(inputFile, "rb") as f:

   humanHeatSignature = 8300
   height = 0
   #data_file = '/home/pi/Desktop/Scatter Plots/collectedHeights.log'
   #fob = open(data_file, 'w')
   newFrame = True
   totalFrames = 0
   frameArray = []
	
   for totalPixels in range(0, 4800): 	  #The for loop read through all the pixels in the array	
       pixelByte = f.read(2)
       pixel = unpack("h", pixelByte)[0]
       frameArray.append(pixel)

       if (totalPixels == (45 * 40)):
	  print ("Hallway Middle: " + str(pixel))

       if (totalPixels == (45 * 70)):
	  print ("Hallway Bottom: " + str(pixel))

       if (totalPixels == (15 * 40)):
	  print ("Cubical Middle: " + str(pixel))

       if (totalPixels == (15 * 70)):
	  print ("Cubical Bottom: " + str(pixel))


  #print (frameArray)

	
