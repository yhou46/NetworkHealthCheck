import codecs
import argparse
import matplotlib.pyplot as pyplot

# local import
import shared
from shared import PingResult

# pingResultList = [ (timestamp, PingResult), ... ]
def drawDiagram(pingResultList):
    datetimeList = []
    latencyList = []

    for resultPair in pingResultList:
        datetimeList.append(resultPair[0])
        latencyList.append(resultPair[1].time.total_seconds() * 1000)
    pyplot.plot_date(x=datetimeList, y=latencyList, fmt="r-")
    pyplot.ylabel("Latency-milliseconds")
    pyplot.xlabel("time")
    pyplot.show()

    return

def run(filePath):
    pingResultList = shared.parse(filePath)

    drawDiagram(pingResultList)
    return

if __name__ == "__main__":

    filePath = "C:\\workspace\\NetworkHealthCheck\\python\src\\network_latency.log"
    run(filePath)