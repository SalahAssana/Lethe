#!/usr/bin/python
import sys

inputFile = sys.argv[1]

outputFile = open("groundTruthResults.csv", "w")

with open(inputFile) as f:
    while True:
        enterFrom = f.readline().strip()
        if enterFrom == "grave": break
        startTime = f.readline().strip()
        exitFrom = f.readline().strip()
        endTime = f.readline().strip()
	
	startTime_array = startTime.split(".")
	endTime_array = endTime.split(".")
	print (startTime_array)
	while len(startTime_array[1]) < 9: startTime_array[1] = "0"+startTime_array[1]
	while len(endTime_array[1]) < 9: endTime_array[1] = "0"+endTime_array[1]

	startTime = startTime_array[0] + "." + startTime_array[1]
	endTime = endTime_array[0] +  "." + endTime_array[1]

	enterRight = False
	enterLeft = False
	exitLeft = False
	exitRight = False

        if enterFrom == "Page_Up":
          #print ("Enter From Right")
	  enterRight = True
	  enterFrom = 'left'

        elif enterFrom == "Next":
          #print ("Enter From Left")
	  enterLeft = True
	  enterFrom = 'right'

        if exitFrom == "Page_Up":
          #print ("Exit From Right")
	  exitRight = True
	  exitFrom = 'left'

        elif exitFrom == "Next":
          #print ("Exit From Left")
	  exitLeft = True
	  exitFrom = 'right'

        #if enterRight is True and exitLeft is True: print("The Person Went Left")
	#if enterLeft is True and exitRight is True: print("The Person Went Right")

	outputFile.write(startTime +"," + endTime +"," + "22" + ","  + enterFrom +","+ exitFrom + "\n")

outputFile.close()
