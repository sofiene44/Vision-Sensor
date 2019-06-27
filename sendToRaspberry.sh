#!/bin/bash
#mac="b8:27:eb:d9:2e:91"    #3A+ mac
mac="b8:27:eb:f8:a6:56"     #3B+ mac
echo "looking for RaspberryPi ip ..."
ip=$(arp -n| grep $mac | head -c13)

echo "raspberry pi IP address found : ."$ip 

scp -r ./* pi@$ip:/home/pi/Vision-Sensor

echo "sending done"
