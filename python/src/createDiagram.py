import codecs
import argparse
import os
import glob
import sys

# external packages
import matplotlib.pyplot as pyplot

# local import
import shared
from shared import PingResult


def initArgParser():
    parser = argparse.ArgumentParser(description = "Create network latency charts from log files")

    parser.add_argument( "-f", "--file", type=str, required=True, help="Log file names; regular expresseion accepted, like \"/usr/data/test*.log\"")
    return parser


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

# Entrance
def main(args):

    parser = initArgParser()
    parsedArgs = parser.parse_args(args)

    filePattern = ""
    if parsedArgs.file != None:
        filePattern = parsedArgs.file

    fileList = glob.glob(filePattern)

    pingResultList = []
    for filePath in fileList:
        pingResultList += shared.parse(filePath)

    pingResultList.sort()
    drawDiagram(pingResultList)
    return

if __name__ == "__main__":

    main(sys.argv[1:])
