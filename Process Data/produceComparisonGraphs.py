import itertools
import numpy as np
import matplotlib.pyplot as plt

#import matplotlib.mlab as mlab
from sklearn.metrics import confusion_matrix

#Plotting confusion Matrix
def direction_confusion_matrix(matchIdx,gt_mat,cd_mat,dirIdx):
	#   L R
	# L
	# R
	entryConfusion = [[0,0],[0,0]] 
	for match in matchIdx:
		gt_entry = gt_mat[match[0], dirIdx]
		cd_entry = cd_mat[match[1], dirIdx]
		if gt_entry == cd_entry and gt_entry == 'left':
			entryConfusion[0][0] = entryConfusion[0][0] + 1
		elif gt_entry is not cd_entry and gt_entry == 'right':
			entryConfusion[1][0] = entryConfusion[1][0] + 1		
		elif gt_entry is not cd_entry and gt_entry == 'left':
			entryConfusion[0][1] = entryConfusion[0][1] + 1
		elif gt_entry == cd_entry and gt_entry == 'right':
			entryConfusion[1][1] = entryConfusion[1][1] + 1

	entryConfusion = np.array(entryConfusion)

	plt.matshow(entryConfusion)
	plt.colorbar()
	plt.show()
	#plt.savefig('confusionMatrix')
	plt.close()


#Producing Histogram of Heights
def height_histogram(matched_heights):
	# the histogram of the data
	#n, bins, patches = plt.hist(matched_heights, 40, normed=1, facecolor='green', alpha=0.75)
	plt.hist(matched_heights)
	plt.xlabel('Height Measurments')
	plt.ylabel('Count')
	plt.title(r'mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
	plt.axis([10, 80, 0, 10])
	plt.grid(True)

	plt.show()
	#plt.savefig('histogram')
	plt.close()
	#This is being added to collect height values over time
	heightFile = open('allHeights.txt', 'a')

	for s in matched_heights:
	    heightFile.write(str(s) + ' ')

	heightFile.write('\n')
	heightFile.close()

#Opening files and processing data
groundTruth = open("groundTruthResults.csv")
collectedData = open("collectedDataResults.csv")

#Array of all the lines in Ground Truth
gt_lines = groundTruth.readlines()
#Array of all the lines in Collected Data
cd_lines = collectedData.readlines()

#Ground Truth Matrix
gt_mat = []
for gt in gt_lines:
	gt_split = gt.strip().split(",")
	gt_mat.append(gt_split)
gt_mat = np.array(gt_mat)

#Collected Data Matrix
cd_mat = []
for cd in cd_lines:
	cd_split = cd.strip().split(",")
	cd_mat.append(cd_split)
cd_mat = np.array(cd_mat)

matchIdx = [];

for i in range(0,len(gt_lines)):
	#get info on GT
	#print ("GT")
	#print (gt_mat[i,:])
	gt_st = gt_mat[i,0]
	gt_et = gt_mat[i,1]
	#print ("Ground Truth: " + gt_st +" "+ gt_et)
	#find a matching event in cd
	for j in range(0,len(cd_lines)):
		#get infor on CD
		#print ("CD")
		#print (cd_mat[j,:])
		cd_st = cd_mat[j,0]
		cd_et = cd_mat[j,1]
		#print ("Collected Data: " + cd_st + "," + cd_et)
		#check if within GT timestamps
		if cd_st > gt_st and cd_et < gt_et:
			#print ("Matched Events")
			#print gt
			#print cd
			matchIdx.append([i,j])
			#print i
			#print j

matchIdx = np.array(matchIdx)

#Cycling throught the ground truth matrix and check for false negatives/positives
for index in range(len(gt_mat)):
	#If the index is not found in the ground truth array then it's a false negative
	if index not in matchIdx[:,0]:
		print ('False Negative Found On: ', index)
	#If the index is not found in the collected data array then it's a false positive
	if index not in matchIdx[:,1]:
		print ('False Positive Found On: ', index)


#histogram of all matching heights
matched_heights = cd_mat[matchIdx[:,1],2].astype(float)
height_histogram(matched_heights)

#Confusion Matrix of Entry and Exit
#direction_confusion_matrix(matchIdx,gt_mat,cd_mat,3)
#direction_confusion_matrix(matchIdx,gt_mat,cd_mat,4)
