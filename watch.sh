#! /bin/bash
name=$1
count=$2
sleepTime=$3
if [ ! $name ] ;then
 echo "please set name file path"
 exit 0
fi

if [ ! $sleepTime ] ; then
  sleepTime=10
fi

pidFile=${name}-${count}.txt

echo /dev/null > $pidFile

echo "pidFile: "$pidFile
for i in $(seq 1 18)
do
  currentTime=`date +%y-%m-%d-%X-%Z`
  echo $i*10"s后 -------------------------"  >> $pidFile
  ps -e -o 'pid,command,rsz,vsz,stime' --sort -rsz | grep kube  >>  $pidFile
  sleep $sleepTime
done