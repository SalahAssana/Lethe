import sys
from struct import unpack

def rotate(matrix, degree):
    if abs(degree) not in [0, 90, 180, 270, 360]:
	print ('Can\'t Make That Rotation')
	return matrix
    if degree == 0:
	return matrix
    elif degree > 0:
	return rotate(zip(*matrix[::-1]), degree-90)
    else:
	return rotate(zip(*matrix[::-1]), degree+90)

inputFile = sys.argv[1]
outputFile = sys.argv[2]

with open(inputFile, "rb") as f:

   humanHeatSignature = 8300
   height = 0
   hotPixelA = False;
   hotPixelB = False;
   humanDetected = False;
   newFrame = True;
   data_file = '/home/pi/Desktop/Doorfly/Process Data/'+outputFile
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

	imageBufferArray = []
	for x in range(60):
	    imageBufferArray.append([])
	count = 0
	column = 0

	for totalPixels in range(0, 4800): 	  #The for loop read through all the pixels in the array	
	   pixelByte = f.read(2)
	   pixel = unpack("h", pixelByte)[0]
	   imageBufferArray[column].append(pixel)
	   count += 1
	   if count == 80:
		column += 1
		count = 0

	rotatedImageBuffer = rotate(imageBufferArray, 270)
	
	for row in range(80):
	    for column in range(60):
   		pixel = rotatedImageBuffer[row][column]

		if pixel > 8300 and newFrame == True:
		    height = 80 - row
		    newFrame = False

		if column == 0:
		    #print pixel,
		    if pixel > humanHeatSignature:
			hotPixelA = True

		if column == 59:
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
