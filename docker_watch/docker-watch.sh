#! /bin/bash

sleepTime=1

memoryDataFile=memory-change.txt

cat /dev/null > $memoryDataFile

echo "memoryDataFile: "$memoryDataFile
for i in $(seq 1 60)
do
  currentTime=`date +%y-%m-%d-%X-%Z`
  echo $i*$sleepTime"s后 -------------------------"  >> $memoryDataFile
  free -h | grep Mem | awk '{print $3}'  >>  $memoryDataFile
  sleep $sleepTime
done