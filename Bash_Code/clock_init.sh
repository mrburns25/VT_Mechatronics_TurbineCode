#!/bin/bash

#This script will set the system time to the RTC time
sleep 15
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
hwclock -s -f /dev/rtc1
hwclock -w