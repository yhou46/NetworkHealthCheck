
import argparse
import sys
import os
import subprocess
import logging
import logging.handlers
import time

from datetime import timedelta

# local import
import shared
from shared import PingResult

# Global variables
g_loggerName = "GlobalLogger"

# Global variables ends

def createPingCommand():
    platformStr = sys.platform

    if platformStr.startswith("win32"):
        return "ping -n 1 "
    elif platformStr.startswith("linux") or platformStr.startswith("darwin"):
        return "ping -c 1 "
    else:
        raise Exception("Unsupported OS: " + platformStr)


def parsePingResultStr_win32(response):
    
    '''ping result in windows is like:
    Approximate round trip times in milli-seconds:
          Minimum = 8ms, Maximum = 8ms, Average = 8ms "

    We only need to get average time, which is 8 in this case 
    '''

    key = "Average = "
    begin = response.find(key)
    end = response.find("ms", begin)

    return float( response[begin+len(key) : end] )


def parsePingResultStr_mac(response):
    '''ping result in mac is like:
    --- 8.8.8.8 ping statistics ---
    1 packets transmitted, 1 packets received, 0.0% packet loss
    round-trip min/avg/max/stddev = 30.767/30.767/30.767/0.000 ms

    We only care about average value
    '''

    key = "stddev =" 
    begin = response.find(key)
    begin = response.find("/", begin+len(key)) # find first "/" after "stddev ="
    end = response.find("/", begin+1) # find next "/" after begin

    return float( response[begin+1 : end] )

# Tested in Ubuntu(WSL) only
def parsePingResultStr_linux(response):
    '''
    --- 8.8.8.8 ping statistics ---
    1 packets transmitted, 1 received, 0% packet loss, time 0ms
    rtt min/avg/max/mdev = 4.074/4.074/4.074/0.000 ms
    '''
    key = "mdev = "
    begin = response.find(key)
    begin = response.find("/", begin+len(key)) # find first "/" after "stddev ="
    end = response.find("/", begin+1) # find next "/" after begin

    return float( response[begin+1 : end] )

# Ping the ip and return the result object
def pingServer(ip):
    command = createPingCommand()

    time = 0

    platformStr = sys.platform
    if platformStr.startswith("win32"):
        response = subprocess.check_output(command + ip).decode('ASCII')
        time = parsePingResultStr_win32(response)
    elif platformStr.startswith("darwin"):
        response = subprocess.check_output(command + ip, shell=True).decode('ASCII')
        time = parsePingResultStr_mac(response)
    elif platformStr.startswith("linux"):
        response = subprocess.check_output(command + ip, shell=True).decode('ASCII')
        time = parsePingResultStr_linux(response)
    else:
        raise Exception("Unsupported OS: " + platformStr)
    

    # TODO: add args to control bytes and ttl?
    return PingResult(ip = ip, numOfBytes = 32, ttl = 51, milliseconds = time)

def initLogger():
    logHandler = logging.handlers.TimedRotatingFileHandler("network_latency.log", when="midnight")
    logFormatter = logging.Formatter(shared.g_sharedLogFormat)
    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger(g_loggerName)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    return logger

# Start service
def run(interval_seconds = 5):

    initLogger()
    logger = logging.getLogger(g_loggerName)

    while(True):
        result = pingServer("8.8.8.8")
        logger.info(result)
        print(result.prettyPrint())
        time.sleep(interval_seconds)
    
    return



if __name__ == "__main__":

    run()
