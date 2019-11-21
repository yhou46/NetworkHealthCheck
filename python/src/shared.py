
import time
import codecs
import datetime

from datetime import timedelta

# Global variables
g_logFormat = "%(asctime)s.%(msecs)03d|%(levelname)s|%(message)s"
g_dateFormat = "%Y-%m-%d %H:%M:%S"
g_datetimeFormat = g_dateFormat + ".%f"

# Global variables ends

class PingResult:
    def __init__(self, ip = "", numOfBytes = 0, ttl = 0, milliseconds = 0):
        self.ip = ip
        self.numOfBytes = numOfBytes
        self.ttl = ttl
        self.time = timedelta(microseconds = milliseconds*1000)

    def prettyPrint(self):
        return "From " + self.ip + "; bytes=" + str(self.numOfBytes) + "; ttl=" + str(self.ttl) + "; time=" + str(self.time.total_seconds() * 1000) + " ms\n"

    def __str__(self):
        return "|".join([self.ip, str(self.numOfBytes), str(self.ttl), str(self.time.total_seconds() * 1000)])

# Return a list of pairs (datetime, PingResult)
def parse(filename):
    pingResultList = []

    with codecs.open(filename, "r+", "utf-8") as file:

        for line in file:
            items = line.strip().split("|")

            timestamp = datetime.datetime.strptime(items[0], g_datetimeFormat)

            # item[1] is logging level (INFO, ERROR...)
            ip = items[2]
            numOfBytes = int(items[3])
            ttl = int(items[4])
            latency = float(items[5])
            pingResult = PingResult(ip, numOfBytes, ttl, latency)

            pingResultList.append( (timestamp, pingResult) )

    return pingResultList


if __name__ == "__main__":
    parse("/mnt/c/workspace/NetworkHealthCheck/python/src/network_latency.log")
    #print( test("2019-11-20 11:37:29.296") )
