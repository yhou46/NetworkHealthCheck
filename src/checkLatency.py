import codecs
import argparse
import sys
import os
import subprocess
import logging

from datetime import timedelta

class PingResult:
    def __init__(self, ip = "", numOfBytes = 0, ttl = 0, milliseconds = 0):
        self.ip = ip
        self.numOfBytes = numOfBytes
        self.ttl = ttl
        self.time = timedelta(microseconds = milliseconds*1000)

    def prettyPrint(self):
        return "From " + self.ip + "; bytes=" + str(self.numOfBytes) + "; ttl=" + str(self.ttl) + "; time=" + str(self.time.total_seconds() * 1000) + " ms\n"

    def __str__(self):
        return ";".join([self.ip, str(self.numOfBytes), str(self.ttl), str(self.time.total_seconds() * 1000)])


def createPingCommand():
    platformStr = sys.platform

    if platformStr.startswith("win32"):
        return "ping -n 1 "
    elif platformStr.startswith("linux") or platformStr.startswith("darwin"):
        return "ping -c 1 "
    else:
        raise Exception("Unsupported OS: " + platformStr)


def parsePingResultStr_win32(response):
    
    # ping result in windows is like:
    # " Approximate round trip times in milli-seconds:
    #      Minimum = 8ms, Maximum = 8ms, Average = 8ms "
    # We only need to get average time, which is 8 in this case
    key = "Average = "
    begin = response.find(key)
    end = response.find("ms", begin)

    return int( response[begin+len(key) : end] )

def parsePingResultStr_linux(response):
    pass

# Ping the ip and return the result object
def pingServer(ip):
    command = createPingCommand()

    response = subprocess.check_output(command + ip).decode('ASCII') 

    time = parsePingResultStr_win32(response)

    # TODO: add args to control bytes and ttl?
    return PingResult(ip = ip, numOfBytes = 32, ttl = 51, milliseconds = time)

def run():
    logging.basicConfig(filename='latency.log', level=logging.DEBUG)
    
    logging.debug('This message should go to the log file')

if __name__ == "__main__":
    # print(createPingCommand())
    # print(timedelta(seconds = 1, microseconds= 13).total_seconds())

    # pingResult = PingResult("8.8.8.8", 32, 5, 45)
    # print(pingResult)

    print( pingServer("8.8.8.8") )
    run()
