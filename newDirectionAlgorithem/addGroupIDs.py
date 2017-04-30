import sys

inputFile = sys.argv[1]

outputFile = open("collectedDataWithGroupId.csv", "w")
input = open(inputFile)
groupID = 0
startOfSpike = False

while True:
	timestamp = input.readline().strip()
	if not timestamp: break
	timestamp_array = timestamp.split(".")
	while len(timestamp_array[1]) < 9:
		timestamp_array[1] = "0"+timestamp_array[1]
	timestamp = timestamp_array[0]+"."+timestamp_array[1]
	#height = input.readline().strip()
	#state = input.readline().strip()
	presence = input.readline().strip()
	leftmost = input.readline().strip()
	rightmost = input.readline().strip()

	if(presence == "True"):
		if(not startOfSpike):
			groupID = groupID + 1
			startOfSpike = True
		outputFile.write(timestamp+","+leftmost+","+rightmost+","+presence+","+str(groupID)+"\n")

	else: #presence == False
		if(startOfSpike):
			startOfSpike = False
		outputFile.write(timestamp+","+leftmost+","+rightmost+","+presence+",0\n")

input.close()
outputFile.close()
