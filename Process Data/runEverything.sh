#INPUT: collectedData.log
#OUTPUT: collectedDataWithGroupId.csv
python addGroupIDs.py

#INPUT: collectedDataWithGroupId.csv
#OUTPUT: collectedDataResults.csv
python detectEvents.py

#INPUT: groundTruth.log
#OUTPUT: groundTruthResults.csv
python processGroundTruth.py

#INPUT: groundTruthResults.csv, collectedDataResults.csv
#OUTPUT: Height Histogram, Direction Confusion Matrix
python produceComparisonGraphs.py

