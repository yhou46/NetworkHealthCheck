pingAndLog()
{
    pingResult=$(ping $1 -n 1 | grep Reply)
    pingResultWithTimestamp="$pingResult time=\"$(date -R)\""
    echo $pingResultWithTimestamp | tee -a $2

    latency=$(echo $pingResult | cut -d: -f2 | cut -d' ' -f3 | cut -d= -f2 | tr -d ms)
    if [ $latency -gt $3 ]; then
        echo $pingResultWithTimestamp >> $4
    fi
}


loopIntervalInSeconds=10
logFilename=latency.log
warnThresholdInMiliseconds=20
warnLogFilename=badLatency.log

echo "Press <Enter> anytime to stop"
echo "Latency warning threshold is ${warnThresholdInMiliseconds}ms"

doLoop=true
while ${doLoop}
do
    pingAndLog 8.8.8.8 $logFilename $warnThresholdInMiliseconds $warnLogFilename
    pingAndLog 192.168.1.1 $logFilename $warnThresholdInMiliseconds $warnLogFilename

    # Press enter to escape loop
    read -p "" -t $loopIntervalInSeconds
    if [ $? -le 128 ]; then # did not timeout
        doLoop=false
    fi
done
