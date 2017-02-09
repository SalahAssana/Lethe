import sys	
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

from struct import unpack

with open("pixelValues.txt", "rb") as f:

   humanHeatSignature = 8200
   height = 0
   data_file = '/home/pi/Desktop/Scatter Plots/collectedHeights.log'
   fob = open(data_file, 'w')
   newFrame = True
   totalFrames = 0
   frameArray = []
	
   while True: #Keep reading from file until loop is broken

	firstByte = f.read(4)
	if not firstByte:
		fob.close()
		break                   #Breaks loop when there is no more data in the file
	secondByte = f.read(4)
	seconds = unpack("i", firstByte)[0]
	milliseconds = unpack("i", secondByte)[0]
	#fob.write("%s.%s" % (seconds, milliseconds))
	#fob.write('\n')
	#print seconds, milliseconds

	for totalPixels in range(0, 4800): 	  #The for loop read through all the pixels in the array	
	   pixelByte = f.read(2)
	   pixel = unpack("h", pixelByte)[0]
	   #frameArray.append(pixel)

	   if pixel > humanHeatSignature and newFrame == True:
	      if (totalPixels % 80) >= 28 and (totalPixels % 80) <= 30: #This checks to see if the pixel is in the three middle columns
	      	height = 60 - (totalPixels/80)
	      	newFrame = False

	totalFrames += 1

	#if totalFrames >= 722:
	   #print (totalFrames)
	 #  a = np.array(frameArray)
	  # a.resize(60, 80)
	   #plt.imshow(a)
	   #plt.show()
	#frameArray = []

	fob.write(str(height))
	fob.write("\n")
	height = 0

	newFrame = True
