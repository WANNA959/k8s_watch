#! /bin/bash
name=$1
count=$2

if [ ! $name ] ;then
 echo "please set name file path"
 exit 0
fi

sleepTime=5

apiServerFile=${name}-${count}.txt

cat /dev/null > $apiServerFile

echo "apiServerFile: "$apiServerFile
for i in $(seq 1 20)
do
  currentTime=`date +%y-%m-%d-%X-%Z`
  echo $i*$sleepTime"s后 -------------------------"  >> $apiServerFile
  ps -e -o 'pid,command,rsz,vsz,stime' --sort -rsz | grep apiserver  >>  $apiServerFile
  sleep $sleepTime
done