# Network Health Check

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
