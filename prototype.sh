pingAndLog()
{
    pingResult=$(ping $1 -n 1 | grep Reply)
    pingResultWithTimestamp="${pingResult} time=\"$(date -R)\""
    echo ${pingResultWithTimestamp} | tee -a $2
}


loopIntervalInSeconds=10
logFilename=latency.log

echo "Press <Enter> anytime to stop"

doLoop=true
while ${doLoop}
do
    pingAndLog 8.8.8.8 ${logFilename}
    pingAndLog 192.168.1.1 ${logFilename}

    # Press enter to escape loop
    read -p "" -t ${loopIntervalInSeconds}
    if [ $? -le 128 ]; then # did not timeout
        doLoop=false
    fi
done
