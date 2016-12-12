#!/bin/bash

#This code will run the System Test python code
#First, CheckLog.py will be terminated
#After the test is complete, CheckLog.py will be started again

#Kill CheckLog.py
kill $(ps aux | grep "[C]heckLog.py" | awk '{print $2}')

#Start the system test code
python /usr/PythonCode/SystemTest.py
echo 'System Test Complete'

#Start CheckLog.py
python /usr/PythonCode/CheckLog.py &

sleep 1

#Check to make sure start up was complete
if ps aux | grep -q '[C]heckLog.py'; then
	echo 'CheckLog.py Start Successful'
else
	echo 'CheckLog.py Failed to Start'
fi
