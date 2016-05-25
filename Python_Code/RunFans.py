#!/usr/bin/env python

#Creation Date: 02/24/2016
#Last Edited: 05/25/2016
#Author: Clinton Burns

#This code will control the fans and check for
#any errors during fan operation

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import sys

######################################################################################

#Define variables
#Error related variables 
Autonomous = True
Error_list = list()
Error = 0

#TAC related variables
interval = 1 #Interval to sample TACs (in seconds)
prev_time = 0 #Previous time holder
current_time = 0 #Current time holder
time_delta = 0 #Change in time holder

Prev_TAC_Val_F1_1 = 0 #Previous TAC value for F1_1
TAC_Val_F1_1 = 0 #Current TAC value for F1_1
Count_F1_1 = 0 #Number of rises and falls in TAC signal for F1_1

Prev_TAC_Val_F1_2 = 0 #Previous TAC value for F1_2
TAC_Val_F1_2 = 0 #Current TAC value for F1_2
Count_F1_2 = 0 #Number of rises and falls in TAC signal for F1_2

Prev_TAC_Val_F2_1 = 0 #Previous TAC value for F2_1
TAC_Val_F2_1 = 0 #Current TAC value for F2_1
Count_F2_1 = 0 #Number of rises and falls in TAC signal for F2_1

Prev_TAC_Val_F2_2 = 0 #Previous TAC value for F2_2
TAC_Val_F2_2 = 0 #Current TAC value for F2_2
Count_F2_2 = 0 #Number of rises and falls in TAC signal for F2_2

Prev_TAC_Val_F3_1 = 0 #Previous TAC value for F3_1
TAC_Val_F3_1 = 0 #Current TAC value for F3_1
Count_F3_1 = 0 #Number of rises and falls in TAC signal for F3_1

Prev_TAC_Val_F3_2 = 0 #Previous TAC value for F3_2
TAC_Val_F3_2 = 0 #Current TAC value for F3_2
Count_F3_2 = 0 #Number of rises and falls in TAC signal for F3_2

Prev_TAC_Val_F4_1 = 0 #Previous TAC value for F4_1
TAC_Val_F4_1 = 0 #Current TAC value for F4_1
Count_F4_1 = 0 #Number of rises and falls in TAC signal for F4_1

Prev_TAC_Val_F4_2 = 0 #Previous TAC value for F4_2
TAC_Val_F4_2 = 0 #Current TAC value for F4_2
Count_F4_2 = 0 #Number of rises and falls in TAC signal for F4_2

######################################################################################

#Set up relay control pins
GPIO.setup("P8_41",GPIO.OUT) #Funnel 1
GPIO.output("P8_41",GPIO.HIGH)
GPIO.setup("P8_42",GPIO.OUT) #Funnel 2
GPIO.output("P8_42",GPIO.HIGH)
GPIO.setup("P8_43",GPIO.OUT) #Funnel 3
GPIO.output("P8_43",GPIO.HIGH)
GPIO.setup("P8_44",GPIO.OUT) #Funnel 4
GPIO.output("P8_44",GPIO.HIGH)

#Start PWM pins
#PWM.start(Channel, duty cycle, frequency)
PWM.start("P8_13",0,25000) #Funnel 1 
PWM.start("P8_19",0,25000) #Funnel 2 
PWM.start("P9_14",0,25000) #Funnel 3 
PWM.start("P9_16",0,25000) #Funnel 4 

#Set up TAC pins
GPIO.setup("P8_7",GPIO.IN,0) #Funnel 1 Fan 1 (F1_1)
GPIO.setup("P8_9",GPIO.IN,0) #Funnel 1 Fan 2 (F1_2)
GPIO.setup("P8_11",GPIO.IN,0) #Funnel 2 Fan 1 (F2_1)
GPIO.setup("P8_15",GPIO.IN,0) #Funnel 2 Fan 2 (F2_2)
GPIO.setup("P8_17",GPIO.IN,0) #Funnel 3 Fan 1 (F3_1)
GPIO.setup("P8_26",GPIO.IN,0) #Funnel 3 Fan 2 (F3_2)
GPIO.setup("P8_28",GPIO.IN,0) #Funnel 4 Fan 1 (F4_1)
GPIO.setup("P8_30",GPIO.IN,0) #Funnel 4 Fan 2 (F4_2)

######################################################################################

#Open file and write status
#Makes LED go blue indicating fans are starting 
txt = open('/usr/PythonCode/RunLog.txt','w') 
txt.write("Blue")
txt.close()

######################################################################################

#Turn on funnels in cascading order and check to make sure they are working
#If there is an error in any fan, the program will throw the correct error 
#code and then terminate.

#Turn on funnel 1
GPIO.output("P8_41",GPIO.LOW)

#Wait till fans are at 0 PWM RPM
time.sleep(7) #Seconds

prev_time = time.time()
current_time = time.time()
time_delta = current_time - prev_time
#Read TAC to check speed for 1 second
while time_delta < interval:
	#Read TAC pin for F1_1 and F1_2
	TAC_Val_F1_1 = GPIO.input("P8_7")
	TAC_Val_F1_2 = GPIO.input("P8_9")

	#See if the state of the pin has changed
	if TAC_Val_F1_1 != Prev_TAC_Val_F1_1:
		Prev_TAC_Val_F1_1 = TAC_Val_F1_1
		Count_F1_1 = Count_F1_1 + 1
	
	if TAC_Val_F1_2 != Prev_TAC_Val_F1_2:
		Prev_TAC_Val_F1_2 = TAC_Val_F1_2
		Count_F1_2 = Count_F1_2 + 1

	current_time = time.time()
	time_delta = current_time - prev_time

#Check to see if any errors with F1_1
if Count_F1_1/2 < 50 or Count_F1_1/2 > 53:
	#Add error code 1 to error list
	Error_list[Error] = 1
	#Add 1 to error counter
	Error = Error + 1
	
#Check to see if any errors with F1_2
if Count_F1_2/2 < 50 or Count_F1_2/2 > 53:
	#Add error code 2 to error list
	Error_list[Error] = 2
	#Add 1 to error counter
	Error = Error + 1

#If any errors, send correct error code to the log file
if len(Error_list) != 0:
	#First check to see if errors are in both fans. If not
	#see if either fan 1 or 2 had the error. Program will
	#terminate if there is any error.
	if Error_list.count(1) > 0 and Error_list.count(2) > 0:
		#Errors in both fans: Error Code 3
		txt = open('/usr/PythonCode/RunLog.txt','w') 
		txt.write("Red\n")
		txt.write("3")
		txt.close()
		sys.exit()
	elif Error_list.count(1) > 0:
		#Error in F1_1: Error Code 1
		txt = open('/usr/PythonCode/RunLog.txt','w') 
		txt.write("Red\n")
		txt.write("1")
		txt.close()
		sys.exit()
	elif Error_list.count(2) > 0:
		#Error in F1_2: Error Code 2
		txt = open('/usr/PythonCode/RunLog.txt','w') 
		txt.write("Red\n")
		txt.write("2")
		txt.close()
		sys.exit()
		
######################################################################################		
#Turn on Funnel 2
GPIO.output("P8_42",GPIO.LOW)

#Wait till fans are at 0 PWM RPM
time.sleep(7) #Seconds

prev_time = time.time()
current_time = time.time()
time_delta = current_time - prev_time
#Read TAC to check speed for 1 second
while time_delta < interval:
	#Read TAC pin for F2_1 and F2_2
	TAC_Val_F2_1 = GPIO.input("P8_11")
	TAC_Val_F2_2 = GPIO.input("P8_15")

	#See if the state of the pin has changed
	if TAC_Val_F2_1 != Prev_TAC_Val_F2_1:
		Prev_TAC_Val_F2_1 = TAC_Val_F2_1
		Count_F2_1 = Count_F2_1 + 1
	
	if TAC_Val_F2_2 != Prev_TAC_Val_F2_2:
		Prev_TAC_Val_F2_2 = TAC_Val_F2_2
		Count_F2_2 = Count_F2_2 + 1

	current_time = time.time()
	time_delta = current_time - prev_time

#Check to see if any errors with F2_1
if Count_F2_1/2 < 50 or Count_F2_1/2 > 53:
	#Add error code 4 to error list
	Error_list[Error] = 4
	#Add 1 to error counter
	Error = Error + 1
	
#Check to see if any errors with F2_2
if Count_F2_2/2 < 50 or Count_F2_2/2 > 53:
	#Add error code 5 to error list
	Error_list[Error] = 5
	#Add 1 to error counter
	Error = Error + 1

#If any errors, send correct error code to the log file
if len(Error_list) != 0:
	#First check to see if errors are in both fans. If not
	#see if either fan 1 or 2 had the error. Program will
	#terminate if there is any error.
	if Error_list.count(4) > 0 and Error_list.count(5) > 0:
		#Errors in both fans: Error Code 6
		txt = open('/usr/PythonCode/RunLog.txt','w') 
		txt.write("Red\n")
		txt.write("6")
		txt.close()
		sys.exit()
	elif Error_list.count(4) > 0:
		#Error in F2_1: Error Code 4
		txt = open('/usr/PythonCode/RunLog.txt','w') 
		txt.write("Red\n")
		txt.write("4")
		txt.close()
		sys.exit()
	elif Error_list.count(2) > 0:
		#Error in F2_2: Error Code 5
		txt = open('/usr/PythonCode/RunLog.txt','w') 
		txt.write("Red\n")
		txt.write("5")
		txt.close()
		sys.exit()
######################################################################################
raw_input("Press Enter to 25 Percent PWM...")

PWM.set_duty_cycle("P8_13",25)
PWM.set_duty_cycle("P8_19",25)
PWM.set_duty_cycle("P9_14",25)
PWM.set_duty_cycle("P9_16",25)

raw_input("PWM 25 Percent\nPress Enter to 50 Percent PWM...")

PWM.set_duty_cycle("P8_13",50)
PWM.set_duty_cycle("P8_19",50)
PWM.set_duty_cycle("P9_14",50)
PWM.set_duty_cycle("P9_16",50)

raw_input("PWM 50 Percent\nPress Enter to 75 Percent PWM...")

PWM.set_duty_cycle("P8_13",75)
PWM.set_duty_cycle("P8_19",75)
PWM.set_duty_cycle("P9_14",75)
PWM.set_duty_cycle("P9_16",75)

raw_input("PWM 75 Percent\nPress Enter to 100 Percent PWM...")

PWM.set_duty_cycle("P8_13",100)
PWM.set_duty_cycle("P8_19",100)
PWM.set_duty_cycle("P9_14",100)
PWM.set_duty_cycle("P9_16",100)

raw_input("PWM 100 Percent\nPress Enter to End")

txt = open('/usr/PythonCode/RunLog.txt','w') 
txt.write("Green")
txt.close()

#Clean up pins
GPIO.cleanup()
PWM.cleanup()
