import numpy as np

inputFile = open("collectedDataWithGroupId.csv")

data = inputFile.readlines()

events = []
current_event = [];

def findDirection(eventArray):
	tmp = [0]*(len(eventArray)-1)
	
	for i in range(0,len(eventArray)-1):
		s1 = eventArray[i][2]
		e1 = eventArray[i][1]
		s2 = eventArray[i+1][2]
		e2 = eventArray[i+1][1]

	
		if (s1 < s2 and e1 < e2):
			if (e1 <= s2):
				tmp[i] = 2
			elif (e1 > s2):
				tmp[i] = 1
		elif (s1 > s2 and e1 > e2):
			if (e2 <= s1):
				tmp[i] = -2
			elif (e2 > s1):
				tmp[i] = -1
		elif (s1 == s2):
			if (e1 > e2):
				tmp[i] = -1
			if (e1 < e1):
				tmp[i] = 1
		elif (e1 == e2):
			if (s1 > s2):
				tmp[i]  = 1
			if (s1 < s2):
				tmp[i] = -1

		#print (s1, e1, s2, e2,tmp[i])

	arraySum = np.sum(tmp)

	if arraySum > 0:
	   return ('right', 'left')
	elif arraySum < 0:
	   return ('left', 'right')
	elif arraySum == 0:
	   print (tmp)
	   print (eventArray)
	   return ('?', '?')	

i = 0
for d in data:
	d_array = d.strip().split(",")
	ts = d_array[0]
	#ts_array = ts.split('.');
	#d_array[0] = float(ts_array[0]) + float(ts_array[1])/1000000000 
	h = int(d_array[1])
	state = d_array[2]
	presence = d_array[3]
	groupID = int(d_array[4])
	
	if(groupID is not 0):
		current_event.append(d_array)
	else:
		if(len(current_event)>0):
			events.append(current_event)
			current_event = []

outputFile = open("collectedDataResults.csv", "w")

for event in events:
	#print("EventID "+str(event[0][4])_
	event_np = np.array(event)
	#print(event)
	#print(event_np)
	#print(event_np[0,0])
	#print(event_np[len(event)-1,0])
	#print(np.max(event_np[:,1].astype(int))
	
	directionTuple = findDirection(event_np)
	#directionTuple = ('right', 'left')

	#Go through the array and find a list of unique state changes
	#Based on the pattern of state changes you can decide entry and exit

	t_s = event_np[0, 0]
	t_e = event_np[len(event)-1, 0]
	h = np.max(event_np[:,1].astype(int))
	d_in = directionTuple[0]
	d_out = directionTuple[1]
	id = event_np[0, 4]
	outputFile.write(t_s + "," + t_e + "," + str(h) + "," + d_in + "," + d_out + "," + str(id) + "\n")
