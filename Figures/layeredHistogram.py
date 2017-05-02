import numpy
from matplotlib import pyplot

inputFile = open('allHeights.txt')
num_lines = sum(1 for line in open('allHeights.txt'))

stringsArray = []

bins = numpy.linspace(0, 90, 100)

for line in range(num_lines):
    inputedString = inputFile.readline().strip()
    stringsArray.append(inputedString)

i = 0
labels = ['5.56', '5.45', '5.75', '5.97']

for row in stringsArray:
    heightStrings = row.split()
    heights = map(float, heightStrings)
    heights = map(int, heights)
    pyplot.hist(heights, bins, alpha = 0.5, label = labels[i])
    i += 1

pyplot.legend(loc='upper right')
pyplot.show()
