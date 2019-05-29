#!/bin/bash
mac="b8:27:eb:d9:2e:91"
echo "looking for RaspberryPi ip ..."
ip=$(arp | grep $mac | head -c12)

echo "raspberry pi IP address found : "$ip 

scp -r ./* pi@$ip:Vision-Sensor

