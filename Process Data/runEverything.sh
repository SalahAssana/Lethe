#INPUT: collectedData.log
#OUTPUT: collectedDataWithGroupId.csv
python addGroupIDs.py $1

#INPUT: collectedDataWithGroupId.csv
#OUTPUT: collectedDataResults.csv
python detectEvents.py

#INPUT: groundTruth.log
#OUTPUT: groundTruthResults.csv
python processGroundTruth.py $2

#INPUT: groundTruthResults.csv, collectedDataResults.csv
#OUTPUT: Height Histogram, Direction Confusion Matrix
python produceComparisonGraphs.py
