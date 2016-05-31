#!/bin/bash

#This script will set a new default gateway for this beaglebone

if ! ping -c 2 8.8.8.8 &> /dev/null; then
	/sbin/route add default gw 192.168.7.1
	echo "Default gateway is now 192.168.7.1"
else
	echo "Default gateway is already set to 192.168.7.1"
fi