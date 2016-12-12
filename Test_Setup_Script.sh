#!/bin/bash
# This script will set up all directories and files needed to run the turbine on a new
# beaglebone running Ubuntu 14.04 with kernel 3.8.13-bone78

# Display intro message to user
cat << EOM
---------------------------------------------------
Welcome to the Turbine System set up!
This script will set up all the directories
needed to run the code and place all the right
files where they need to be to work.
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
# Make Turbine directory
echo "Creating Turbine Directory in /usr/local...[]"
if [[ ! -d /usr/local/Turbine ]]; then
    mkdir /usr/local/Turbine
    # Check to see if directory was made
    if [[ -d /usr/local/Turbine ]]; then
        echo "Creating Turbine Directory in /usr/local...[True]"
    else
        echo "Creating Turbine Directory in /usr/local...[False]"
    fi
fi

# Make the python code directory if not already there
echo "Creating PythonCode Directory in /usr/local/Turbine...[]"
if [[ ! -d /usr/local/Turbine/PythonCode ]]; then
    mkdir /usr/local/Turbine/PythonCode
    # Check to see if directory was made
    if [[ -d /usr/local/Turbine/PythonCode ]]; then
        echo "Creating PythonCode Directory in /usr/local/Turbine...[True]"
    else
        echo "Creating PythonCode Directory in /usr/local/Turbine...[False]"
    fi
fi

# Add all the python code to PythonCode directory if not already there 
echo "Copying Python Files to /usr/local/Turbine/PythonCode...[]"
if ! diff $(pwd)/Python_Code /usr/local/Turbine/PythonCode >/dev/null; then
    cp -r $(pwd)/Python_Code/. /usr/local/Turbine/PythonCode
fi

# Check to see if all files copied
if diff $(pwd)/Python_Code /usr/local/Turbine/PythonCode >/dev/null; then
    echo "Copying Python Files to /usr/local/Turbine/PythonCode...[True]"
else
    echo "Copying Python Files to /usr/local/Turbine/PythonCode...[False]"
    exit
fi

# Make YAML_Files directory if not already there
echo "Creating YAML_Files Directory in /usr/local/Turbine...[]"
if [[ ! -d /usr/local/Turbine/YAML_Files ]]; then
    mkdir /usr/local/Turbine/YAML_Files
    # Check to see if directory was made
    if [[ -d /usr/local/Turbine/YAML_Files ]]; then
        echo "Creating YAML_Files Directory in /usr/local/Turbine...[True]"
    else
        echo "Creating YAML_Files Directory in /usr/local/Turbine...[False]"
    fi
fi

# Add all the yaml files to YAML_Files directory if not already there 
echo "Copying yaml files to /usr/local/Turbine/YAML_Files...[]"
if ! diff $(pwd)/YAML_Files /usr/local/Turbine/YAML_Files >/dev/null; then
    cp -r $(pwd)/YAML_Files/. /usr/local/Turbine/YAML_Files
fi

# Check to see if all files copied
if diff $(pwd)/YAML_Files /usr/local/Turbine/YAML_Files >/dev/null; then
    echo "Copying yaml files to /usr/local/Turbine/YAML_Files...[True]"
else
    echo "Copying yaml files to /usr/local/Turbine/YAML_Files...[False]"
    exit
fi

# Make the Logs directory if not already there
echo "Creating Logs Directory in /usr/local/Turbine...[]"
if [[ ! -d /usr/local/Turbine/Logs ]]; then
    mkdir /usr/local/Turbine/Logs
    # Check to see if directory was made
    if [[ -d /usr/local/Turbine/Logs ]]; then
        echo "Creating Logs Directory in /usr/local/Turbine...[True]"
    else
        echo "Creating Logs Directory in /usr/local/Turbine...[False]"
    fi
fi

# Make RunLog.txt and SystemLog.txt
touch /usr/local/Turbine/Logs/RunLog.txt
echo "Green" > /usr/local/Turbine/Logs/RunLog.txt
touch /usr/local/Turbine/Logs/SystemLog.txt
echo $(date) > /usr/local/Turbine/Logs/SystemLog.txt

# Add all the shell scripts if not already added and then check to make sure it copied
echo "Copying shell scripts:"
# RunSystemTest.sh
echo "Copying RunSystemTest.sh to /bin...[]"
if [[ ! -e /bin/RunSystemTest.sh ]]; then
    cp $(pwd)/Bash_Code/RunSystemTest.sh /bin
    # Check that it copied
    if [[ -e /bin/RunSystemTest.sh ]]; then
        echo "Copying RunSystemTest.sh to /bin...[True]"
    else
        echo "Copying RunSystemTest.sh to /bin...[False]"
    fi
fi
# SetDefaultGW.sh
echo "Copying SetDefaultGW.sh to /bin...[]"
if [[ ! -e /bin/SetDefaultGW.sh ]]; then
    cp $(pwd)/Bash_Code/SetDefaultGW.sh /bin
    # Check that it copied
    if [[ -e /bin/SetDefaultGW.sh ]]; then
        echo "Copying SetDefaultGW.sh to /bin...[True]"
    else
        echo "Copying SetDefaultGW.sh to /bin...[False]"
    fi
fi
# RunCheckLog.sh
echo "Copying RunCheckLog.sh to /bin...[]"
if [[ ! -e /bin/RunCheckLog.sh ]]; then
    cp $(pwd)/Bash_Code/RunCheckLog.sh /bin
    # Check that it copied
    if [[ -e /bin/RunCheckLog.sh ]]; then
        echo "Copying RunCheckLog.sh to /bin...[True]"
    else
        echo "Copying RunCheckLog.sh to /bin...[False]"
    fi
fi
# clock_init.sh
# First make rtc-ds1307 directory
echo "Making rtc-ds1307 dir in /usr/share...[]"
if [[ ! -d /usr/share/rtc-ds1307 ]]; then
    sudo mkdir /usr/share/rtc-ds1307
    # Check to make sure directory made
    if [[ -e /usr/share/rtc-ds1307 ]]
        echo "Making rtc-ds1307 dir in /usr/share...[True]"
    else
        echo "Making rtc-ds1307 dir in /usr/share...[False]"
    fi
fi
# Copy file
echo "Copying clock_init.sh to /usr/share/rtc-ds1307...[]"
if [[ ! -e /usr/share/rtc-ds1307/clock_init.sh ]]; then
    cp $(pwd)/Bash_Code/clock_init.sh /usr/share/rtc-ds1307
    # Check to make sure file copied
    if [[ -e /usr/share/rtc-ds1307/clock_init.sh ]]; then
        echo "Copying clock_init.sh to /usr/share/rtc-ds1307...[True]"
    else
        echo "Copying clock_init.sh to /usr/share/rtc-ds1307...[False]"
    fi
fi

# Create upstart files if not already there
echo "Copying Conf Files:"
# CheckLog.conf
echo "Copying CheckLog.conf to /etc/init...[]"
if [[ ! -e /etc/init/CheckLog.conf ]]; then
    cp $(pwd)/Conf_Files/CheckLog.conf /etc/init
    # Check to make sure copied
    if [[ -e /etc/init/CheckLog ]]; then
        echo "Copying CheckLog.conf to /etc/init...[True]"
        service CheckLog start
    else
        echo "Copying CheckLog.conf to /etc/init...[False]"
    fi
fi
# rtc-ds1307.conf
echo "Copying rtc-ds1307.conf to /etc/init...[]"
if [[ ! -e /etc/init/rtc-ds1307.conf ]]; then
    cp $(pwd)/Conf_Files/rtc-ds1307.conf /etc/init
    # Check to make sure copied
    if [[ -e /etc/init/rtc-ds1307.conf ]]; then
        echo "Copying rtc-ds1307.conf to /etc/init...[True]"
        service rtc-ds1307 start
    else
        echo "Copying rtc-ds1307.conf to /etc/init...[False]"
    fi
fi

echo "Install Done. Please check started services."
echo "A RESTART IS REQUIRED TO FINISH INSTALL"


