from struct import unpack

with open("pixelValues.txt", "rb") as f:

   humanHeatSignature = 8200
   height = 0
   hotPixelA = False;
   hotPixelB = False;
   humanDetected = False;
   newFrame = True;
   data_file = '/home/pi/Desktop/Doorfly/Process Data/collectedData.log'
   fob = open(data_file, 'w')

	
   while True: #Keep reading from file until loop is broken

	firstByte = f.read(4)
	if not firstByte:
		fob.close() 
		break                   #Breaks loop when there is no more data in the file
	secondByte = f.read(4)
	seconds = unpack("i", firstByte)[0]
	milliseconds = unpack("i", secondByte)[0]
	fob.write("%s.%s" % (seconds, milliseconds))
	fob.write('\n')
	#print seconds, milliseconds

	for totalPixels in range(0, 4800): 	  #The for loop read through all the pixels in the array	
	   pixelByte = f.read(2)
	   pixel = unpack("h", pixelByte)[0]
	   
	   if pixel > 8300 and newFrame == True and (totalPixels % 60) == 29:
	      height = 60 - (totalPixels/80)
	      newFrame = False

	   if totalPixels == 2400:
	      #print pixel,
	      if pixel > humanHeatSignature:
		hotPixelA = True

	   if totalPixels == 2479:
	      #print pixel
	      if pixel > humanHeatSignature:
		hotPixelB = True

	   if pixel > humanHeatSignature:
	   	humanDetected = True

	#print "The max height found is: " + str(height)
	fob.write(str(height))
	fob.write("\n")
	height = 0
	newFrame = True

	if not hotPixelA and not hotPixelB: fob.write("HO\n")
	elif hotPixelA and not hotPixelB: fob.write("HA\n")
	elif not hotPixelA and hotPixelB: fob.write("HB\n")
	elif hotPixelA and hotPixelB: fob.write("HAB\n")
	hotPixelA = False
	hotPixelB = False

	if humanDetected:
	  #print "A human heat signature was detected"
	  fob.write("True\n")
	  humanDetected = False
	else:
	  #print "No human heat signature was detected"
	  fob.write("False\n")
	  humanDetected = False
