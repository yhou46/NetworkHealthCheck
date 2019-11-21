
  

# Network Health Check

  

## Python

  

### Requirements

1. Python3 required (python 3.6.8 or above)

2. python packages required:
    matplotlib (3.1.1 or above)

  

### Quick start

1. Use checkLatency.py to get data; data will be saved into log files

2. Use createDiagram.py to create diagrams from the log files created by checkLatency.py

  

### TODO:

1. Add config files with a list of ips to ping

2. Add arg parser

  
  

## Shell script:

  

### Script1:

  

Periodically ping public ip address and local router gateway FOREVER.

  

Log ping latency result. Consider log rotation by hour.

  
  
  

*input:*

  

- ping destination(s)

  

- file containing ping destinations, each line is an ip addr

  
  
  

*output:*

  

- log file containing latency data. each line is an entry with destination and rtt

  
  

### Script2:

  

Aggregate log result and draw latency graph

  
  
  

*input:*

  

- startTime (default 1h)

  

- endTime (default now)

  

- log folder location (default .)

  

- thresholdInMiliSec

  
  
  

*output:*

  

- graph