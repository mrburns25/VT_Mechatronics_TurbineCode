#!/usr/bin/env python

#Creation Date: 05/31/2016
#Last Edited: 06/01/2016
#Author: Clinton Burns

#This code will control the fans and check for
#any errors during fan operation

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time
import sys

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

######################################################################################

#Open file and write status
#Makes LED go blue indicating fans are starting
#Also indicate in Demo Mode so info #5 
txt = open('/usr/PythonCode/RunLog.txt','w') 
txt.write("Blue")
txt.write("5")
txt.close()

######################################################################################

#Stager start funnels
GPIO.output("P8_41",GPIO.LOW)
time.sleep(1)
GPIO.output("P8_42",GPIO.LOW)
time.sleep(1)
GPIO.output("P8_43",GPIO.LOW)
time.sleep(1)
GPIO.output("P8_44",GPIO.LOW)
time.sleep(1)

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
