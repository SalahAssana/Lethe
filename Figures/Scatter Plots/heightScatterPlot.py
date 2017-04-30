import matplotlib.pyplot
import pylab

fob = open('collectedHeights.log', 'r')
heightsCollected = []

frameCount = 0

for x in fob:
   heightsCollected.append(int(x))
   #if int(x) > 40 and int(x) < 50: print (x)
   #frameCount += 1

heightsRange = range(0, len(heightsCollected))

matplotlib.pyplot.scatter(heightsRange, heightsCollected)
matplotlib.pyplot.show()

matplotlib.pyplot.hist(heightsCollected)
matplotlib.pyplot.show()

#matplotlib.pyplot.savefig('8500')
#matplotlib.pyplot.close()
