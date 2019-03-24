#!/bin/bash


date >> /home/pi/timer.log
#cd "/home/pi"
/usr/bin/python /home/pi/uploadImageFromRPI.py


echo "working"
