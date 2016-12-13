#!/usr/bin/env python

#Creation Date: 05/31/2016
#Last Edited: 12/13/2016
#Author: Clinton Burns

#This code will control the fans for a demo.
#There is no error checking

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from Funnel import Funnel
import time
import sys
import yaml

######################################################################################

#Set log path file from yaml
log_paths_file = open('/usr/local/Turbine/YAML_Files/Log_Paths.yaml')
log_paths = yaml.safe_load(log_paths_file)
log_paths_file.close()
runlog_path = log_paths['RunLog']

#Open yaml file and read in data
file = open('/usr/local/Turbine/YAML_Files/Funnel_Setup.yaml')
funnel_setup = yaml.safe_load(file)
file.close()

#Create list of funnels and populate with funnel objects
funnel_list = list()
for funnel in funnel_setup.values():
    funnel_list.append(Funnel(funnel['Relay'], funnel['PWM'], funnel['TAC1'], funnel['TAC2']))
    print('Funnel Created')


######################################################################################

#Open file and write status
#Makes LED go blue indicating fans are starting
#Also indicate in Demo Mode 
txt = open(runlog_path,'w') 
txt.write("Blue\n")
txt.write("Demo_Start")
txt.close()

######################################################################################

#Stager start funnels
for i in range(0,4):
    funnel_list[i].Turn_On()
    time.sleep(1)

######################################################################################
raw_input("Press Enter to 25 Percent PWM...")

for i in range(0,4):
    funnel_list[i].Set_Speed(25)

raw_input("PWM 25 Percent\nPress Enter to 50 Percent PWM...")

for i in range(0,4):
    funnel_list[i].Set_Speed(50)

raw_input("PWM 50 Percent\nPress Enter to 75 Percent PWM...")

for i in range(0,4):
    funnel_list[i].Set_Speed(75)

raw_input("PWM 75 Percent\nPress Enter to 100 Percent PWM...")

for i in range(0,4):
    funnel_list[i].Set_Speed(100)

raw_input("PWM 100 Percent\nPress Enter to End")

txt = open(runlog_path,'w')
txt.write("Green\n")
txt.write("Demo_Stop")
txt.close()

#Clean up pins
GPIO.cleanup()
PWM.cleanup()
