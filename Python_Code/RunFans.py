#!/usr/bin/env python

#Creation Date: 02/24/2016
#Last Edited: 01/10/2017
#Author: Clinton Burns

#This code will control the fans and check for
#any errors during fan operation

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from Funnel import Funnel
import time
import sys
import yaml
import os.path

######################################################################################

#Set log path file from yaml
log_paths_file = open('/usr/local/Turbine/YAML_Files/Log_Paths.yaml')
log_paths = yaml.safe_load(log_paths_file)
log_paths_file.close()
runlog_path = log_paths['RunLog']

#Open funnel yaml file and read in data
funnel_file = open('/usr/local/Turbine/YAML_Files/Funnel_Setup.yaml')
funnel_setup = yaml.safe_load(funnel_file)
funnel_file.close()

#Create list of funnels and populate with funnel objects
funnel_list = list()
for funnel in funnel_setup.values():
    funnel_list.append(Funnel(funnel['Relay'], funnel['PWM'], funnel['TAC1'], funnel['TAC2']))
    print('Funnel Created')

#Define variables
#Error related variables 
Error_list = list()
Error = 0

######################################################################################

#Open file and write status
#Makes LED go blue and set to info to Test_F1
txt = open(runlog_path,'w') 
txt.write("Blue\n")
txt.write("Test_F1")
txt.close()

#Turn on funnels in cascading order and check to make sure they are working
#If there is an error in any fan, the program will throw the correct error 
#code and then terminate.

#Turn on funnel 1
funnel_list[0].Turn_On()

#Wait till fans are at 0 PWM RPM
time.sleep(7) #Seconds

#Take samples of TACs
funnel_1_TAC = funnel_list[0].Take_Sample() 

#Check to see if any error (Take_Sample returns just 1 0)
if funnel_1_TAC["TAC1_Freq"] == 0 or funnel_1_TAC["TAC2_Freq"] == 0:
    txt = open(runlog_path,'w') 
    txt.write("Red\n")
    txt.write("Err_14")
    txt.close()
    sys.exit()

#Check to see if any errors with F1_1
if funnel_1_freq['TAC1_Avg'] < 50 or funnel_1_freq['TAC1_Avg'] > 62:
    #Add error code 1 to error list
    Error_list.append(1)

#Check to see if any errors with F1_2
if funnel_1_freq['TAC2_Avg'] < 48 or funnel_1_freq['TAC2_Avg'] > 60:
    #Add error code 2 to error list
    Error_list.append(2)

#If any errors, send correct error code to the log file
if len(Error_list) != 0:
    #First check to see if errors are in both fans. If not
    #see if either fan 1 or 2 had the error. Program will
    #terminate if there is any error.
    if Error_list.count(1) > 0 and Error_list.count(2) > 0:
        #Errors in both fans: Error Code 3
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_3")
        txt.close()
        sys.exit()
    elif Error_list.count(1) > 0:
        #Error in F1_1: Error Code 1
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_1")
        txt.close()
        sys.exit()
    elif Error_list.count(2) > 0:
        #Error in F1_2: Error Code 2
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_2")
        txt.close()
        sys.exit()
        
######################################################################################
#Open file and write status
#Makes LED go blue and set to info to Test_F2 
txt = open(runlog_path,'w') 
txt.write("Blue\n")
txt.write("Test_F2")
txt.close()

#Turn on Funnel 2
funnel_list[1].Turn_On()

#Wait till fans are at 0 PWM RPM
time.sleep(7) #Seconds

#Take samples of TACs
funnel_2_TAC = funnel_list[1].Take_Sample()

#Check to see if any error (Take_Sample returns just 1 0)
if funnel_2_TAC["TAC1_Freq"] == 0 or funnel_2_TAC["TAC2_Freq"] == 0:
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_14")
        txt.close()
        sys.exit() 

#Get avearge. Average frequency is returned
funnel_2_freq = Average(funnel_2_TAC)

#Check to see if any errors with F2_1
if funnel_2_freq['TAC1_Avg'] < 48 or funnel_2_freq['TAC1_Avg'] > 60:
    #Add error code 4 to error list
    Error_list.append(4)

#Check to see if any errors with F2_2
if funnel_2_freq['TAC2_Avg'] < 50 or funnel_2_freq['TAC2_Avg'] > 60:
    #Add error code 5 to error list
    Error_list.append(5)

#If any errors, send correct error code to the log file
if len(Error_list) != 0:
    #First check to see if errors are in both fans. If not
    #see if either fan 1 or 2 had the error. Program will
    #terminate if there is any error.
    if Error_list.count(4) > 0 and Error_list.count(5) > 0:
        #Errors in both fans: Error Code 6
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_6")
        txt.close()
        sys.exit()
    elif Error_list.count(4) > 0:
        #Error in F2_1: Error Code 4
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_4")
        txt.close()
        sys.exit()
    elif Error_list.count(5) > 0:
        #Error in F2_2: Error Code 5
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_5")
        txt.close()
        sys.exit()
######################################################################################
#Open file and write status
#Makes LED go blue and set to info to Test_F3 
txt = open(runlog_path,'w') 
txt.write("Blue\n")
txt.write("Test_F3")
txt.close()

#Turn on Funnel 3
funnel_list[2].Turn_On()

#Wait till fans are at 0 PWM RPM
time.sleep(7) #Seconds

#Take samples of TACs
funnel_3_TAC = funnel_list[2].Take_Sample() 

#Check to see if any error (Take_Sample returns just 1 0)
if funnel_3_TAC["TAC1_Freq"] == 0 or funnel_3_TAC["TAC2_Freq"] == 0:
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_14")
        txt.close()
        sys.exit()

#Get avearge. Average frequency is returned
funnel_3_freq = Average(funnel_3_TAC)

#Check to see if any errors with F3_1
if funnel_3_freq['TAC1_Avg'] < 48 or funnel_3_freq['TAC1_Avg'] > 59:
    #Add error code 7 to error list
    Error_list.append(7)

#Check to see if any errors with F3_2
if funnel_3_freq['TAC2_Avg'] < 48 or funnel_3_freq['TAC2_Avg'] > 60:
    #Add error code 8 to error list
    Error_list.append(8)

#If any errors, send correct error code to the log file
if len(Error_list) != 0:
    #First check to see if errors are in both fans. If not
    #see if either fan 1 or 2 had the error. Program will
    #terminate if there is any error.
    if Error_list.count(7) > 0 and Error_list.count(8) > 0:
        #Errors in both fans: Error Code 9
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_9")
        txt.close()
        sys.exit()
    elif Error_list.count(7) > 0:
        #Error in F3_1: Error Code 7
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_7")
        txt.close()
        sys.exit()
    elif Error_list.count(8) > 0:
        #Error in F3_2: Error Code 8
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_8")
        txt.close()
        sys.exit()
######################################################################################
#Open file and write status
#Makes LED go blue and set to info to Test_F4 
txt = open(runlog_path,'w') 
txt.write("Blue\n")
txt.write("Test_F4")
txt.close()

#Turn on Funnel 4
funnel_list[3].Turn_On()

#Wait till fans are at 0 PWM RPM
time.sleep(7) #Seconds

#Take samples of TACs
funnel_4_TAC = funnel_list[3].Take_Sample() 

#Check to see if any error (Take_Sample returns just 1 0)
if funnel_4_TAC["TAC1_Freq"] == 0 or funnel_4_TAC["TAC2_Freq"] == 0:
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_14")
        txt.close()
        sys.exit()

#Get avearge. Average frequency is returned
funnel_4_freq = Average(funnel_4_TAC)

#Check to see if any errors with F4_1
if funnel_4_freq['TAC1_Avg'] < 48 or funnel_4_freq['TAC1_Avg'] > 60:
    #Add error code 10 to error list
    Error_list.append(10)

#Check to see if any errors with F4_2
if funnel_4_freq['TAC2_Avg'] < 48 or funnel_4_freq['TAC2_Avg'] > 60:
    #Add error code 11 to error list
    Error_list.append(11)

#If any errors, send correct error code to the log file
if len(Error_list) != 0:
    #First check to see if errors are in both fans. If not
    #see if either fan 1 or 2 had the error. Program will
    #terminate if there is any error.
    if Error_list.count(10) > 0 and Error_list.count(11) > 0:
        #Errors in both fans: Error Code 12
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_12")
        txt.close()
        sys.exit()
    elif Error_list.count(10) > 0:
        #Error in F4_1: Error Code 10
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_10")
        txt.close()
        sys.exit()
    elif Error_list.count(11) > 0:
        #Error in F4_2: Error Code 11
        txt = open(runlog_path,'w') 
        txt.write("Red\n")
        txt.write("Err_11")
        txt.close()
        sys.exit()
######################################################################################
#Open file and write status
#Makes LED go blue and set to info to 4 
txt = open(runlog_path,'w')  
txt.write("Blue\n")
txt.write("Turbine_Ready")
txt.close()

#If no errors on any funnel, all the fans will be set to 100 PWM
for i in range(0,4):
    funnel_list[i].Set_Speed(100)

#Run for some time
time.sleep(60)

#If no errors, set everything green
txt = open(runlog_path,'w') 
txt.write("Green\n")
txt.write("Stop")
txt.close()

#Clean up pins
GPIO.cleanup()
PWM.cleanup()
