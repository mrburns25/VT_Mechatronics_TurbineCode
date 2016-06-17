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
echo "Collecting System Info...[]"
# Get OS name
OS=$(lsb_release -i | awk {'print $3'})
# Get OS version
Ver=$(lsb_release -a | awk {'print $2'})
# Get kernel info
kernel=$(uname -r)
echo "Collecting System Info...[Done]"

# Check to make sure that all system requirements are met
# If a condition is not met, terminate script
# Check OS
echo "Checking OS Name.........[]"
if [[ $OS == "Ubuntu" ]]; then
	echo "Checking OS Name.........[True]"
else
	echo "Checking OS Name.........[False]"
	echo "Please install Ubuntu to continue"
	exit
fi

# Check OS Version
if [[ $Ver == "14.04" ]]; then
	echo "Checking OS Version......[True]"
else
	echo "Checking OS Version......[False]"
	echo "Ubuntu 14.04 is required to continue"
	exit
fi

# Check kernel version
if [[ $kernel == "3.8.13-bone78" ]]; then
	echo "Checking Kernel Version..[True]"
else
	echo "Checking Kernel Version..[False]"
	echo "Kernel 3.8.13-bone78 is required to continue"
	exit
fi

# Start to create needed directories
echo "Creating PythonCode Directory...[]"
# Make the python code directory if not already there
if [ ! -d /usr/PythonCodeTEST ]; then
	sudo mkdir /usr/PythonCodeTEST
fi

# Check to see if directory was made
# If not try 5 times. If still not there, end script
i=0
if [ -d /usr/PythonCodeTEST ]; then
	echo "Creating PythonCode Directory...[True]"
else
	while [ ! -d /usr/PythonCodeTEST ]; do
		sudo mkdir /usr/PythonCodeTEST
		(($i++))
		
		if [[ $i et 6 ]]; then 
			echo "Creating PythonCode Directory...[False]"
			echo "Could not Create /usr/PythonCode Directory"
			exit
		fi
	done
fi

# Add all the python code to PythonCode directory
echo "Copying Python Files...[]"
cp -r $(pwd)/Python_Code/. /usr/PythonCodeTEST

# Check to see if all files copied
if diff /usr/PythonCodeTEST /usr/PythonCodeTEST; then
	echo "Copying Python Files...[True]"
else
	echo "Copying Python Files...[False]"
	echo "Error Copying Files"
	exit
fi

# Create upstart files and start services
echo "Copying Conf Files...[]"
cp $(pwd)/Conf_Files/CheckLog.conf /etc/init
cp $(pwd)/Conf_Files/rtc-ds1307.conf /etc/init

# Check to make sure the files were copied
