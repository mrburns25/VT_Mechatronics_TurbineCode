#!/bin/bash
# This script will set up all directories and files needed to run the turbine on a new
# beaglebone running Ubuntu 14.04 with kernel 3.8.13-bone78

# Display intro message to user
cat << EOM
---------------------------------------------------
Welcome to the Turbine System set up!
This script will set up all the directories
needed to run the code and place all the right
code files where they need to be to work.
THIS MEANS THAT THE SCRIPT WILL MAKE MODIFICATIONS
TO YOUR SYSTEM!! By saying "Yes" to the question 
below, you agree that you are aware of the changes
that will be made and accept any good or bad 
result that could result from this operation (Only
good hopefully)
---------------------------------------------------
EOM

# Read in user input
read -p "Start Turbine System set up? [Y/N] " usr_ans

# End script if user says no
if [[ $usr_ans != "Y" && $usr_ans != "y" ]]; then
	echo "Terminating Set Up"
	exit
fi

# Collect system information
# Get OS name
OS=$(lsb_release -a | grep "Distributor" | awk {'print $3'})
# Get OS version
Ver=$(lsb_release -a| grep "Release" | awk {'print $2'})
# Get kernel info
kernel=$(uname -r)

# Check to make sure that all system requirements are met
# Check OS
echo -n "Checking OS Name.........[]"
if [[ $OS == "Ubuntu"]]; then
	echo "Checking OS Name.........[True]"
else
	echo "Checking OS Name.........[False]"
	echo "Please install Ubuntu to continue"
	exit
fi

# Check OS Version
echo -n "Checking OS Version......[]"
if [[ $Ver == "14.04"]]; then
	echo "Checking OS Version......[True]"
else
	echo "Checking OS Version......[False]"
	echo "Ubuntu 14.04 is required to continue"
	exit
fi

# Check kernel version
echo -n "Checking Kernel Version..[]"
if [[ $kernel == ""]]; then
	echo
else
	echo 
	echo 
	exit
fi
