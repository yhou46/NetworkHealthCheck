
import time
import codecs

from datetime import timedelta

# Global variables
g_sharedLogFormat = "%(asctime)s-%(levelname)s;%(message)s"

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
        return ";".join([self.ip, str(self.numOfBytes), str(self.ttl), str(self.time.total_seconds() * 1000)])

# Return a list of pairs (datetime, PingResult)
def parse(filename):
    pingResultList = []

    with codecs.open(filename, "r+", "utf-8") as file:

        for line in file:
            items = line.strip().split(";")
            
            ip = items[1]
            numOfBytes = int(items[2])
            ttl = int(items[3])
            time = float(items[4])

            # TODO: should also read datetime
            pingResultList.append(PingResult(ip, numOfBytes, ttl, time))

    for result in pingResultList:
        print(result)
    return pingResultList

        

if __name__ == "__main__":
    parse("/mnt/c/workspace/NetworkHealthCheck/python/src/network_latency.log")
