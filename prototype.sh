loopNum=5
loopIntervalInSeconds=2
doLoop=true

echo "Press <Enter> anytime to stop"

while ${doLoop}
do
    pingResult=$(ping 8.8.8.8 -n 1 | grep Reply)
    pingResultWithTimestamp="${pingResult} time=\"$(date -R)\""
    echo ${pingResultWithTimestamp} | tee -a latency.log

    # Press enter to escape loop
    read -p "" -t ${loopIntervalInSeconds}
    if [ $? -le 128 ]; then # did not timeout
        doLoop=false
    fi
done