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
   leftmostPixel = 60
   rightmostPixel = 0
   humanDetected = False
   data_file = '/home/pi/Desktop/Doorfly/newDirectionAlgorithem/'+outputFile+'PixelValuesProcessedData.log'
   fob = open(data_file, 'w')
   #startOfSpke = False

	
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
	rowFromTop = 0

	for totalPixels in range(0, 4800): 	  #The for loop read through all the pixels in the array	
	   pixelByte = f.read(2)
	   pixel = unpack("h", pixelByte)[0]
	   imageBufferArray[rowFromTop].append(pixel)
	   count += 1
	   if count == 80:
		rowFromTop += 1
		count = 0

	rotatedImageBuffer = rotate(imageBufferArray, 270)
	
	for row in range(80):
	    for column in range(60):
   		pixel = rotatedImageBuffer[row][column]

		#If a human is detected
		if pixel > humanHeatSignature:
		    #If this is a person in the frame then set flag to true
		    humanDetected = True
		    #This will find the rightmost pixel in the frame that's above the threshold.
		    if column > rightmostPixel:
			rightmostPixel = column
		    #This will find the leftmost pixel in the frame that's above the threshold.
		    if column < leftmostPixel:
			leftmostPixel = column

	#if humanDetected and startOfSpike:
	#   print ('---------------------------\n')
	#   startOfSpike = False

	if humanDetected:
	   #print (leftmostPixel, rightmostPixel)
	   fob.write("True\n")
           humanDetected = False
  	else:
	   fob.write("False\n")
	   humanDetected = False
	   #startOfSpike = True

	fob.write(str(rightmostPixel))
	fob.write("\n")
	fob.write(str(leftmostPixel))
	fob.write("\n")

	rightmostPixel = 0
	leftmostPixel = 60

