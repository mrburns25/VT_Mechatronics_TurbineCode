#!/usr/bin/env python

#Creation Date: 01/20/2016
#Last Edited: 05/25/2016
#Author: Clinton Burns

#This code is used to test the different systems
#It will test the RGB LED, the Fan Control Relay, PWM signals,
#and the TACs from the fans
#
#This code will not run during normal operation. This code will
#only be used by someone who is trying to debug an issue.
#MAKE SURE THE CHECK LOG CODE IS NOT RUNNING WHEN THIS IS EXECUTED

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import Adafruit_CharLCD as LCD
import time
import sys

######################################################################################

#Define variables
prev_time = 0 #Previous time holder
current_time = 0 #Current time holder
time_delta = 0 #Change in time holder
interval = 1 #Interval to sample TACs (in seconds)

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

#Set up TAC pins
GPIO.setup("P8_7",GPIO.IN,0) #Funnel 1 Fan 1 (F1_1)
GPIO.setup("P8_9",GPIO.IN,0) #Funnel 1 Fan 2 (F1_2)
GPIO.setup("P8_11",GPIO.IN,0) #Funnel 2 Fan 1 (F2_1)
GPIO.setup("P8_15",GPIO.IN,0) #Funnel 2 Fan 2 (F2_2)
GPIO.setup("P8_17",GPIO.IN,0) #Funnel 3 Fan 1 (F3_1)
GPIO.setup("P8_26",GPIO.IN,0) #Funnel 3 Fan 2 (F3_2)
GPIO.setup("P8_28",GPIO.IN,0) #Funnel 4 Fan 1 (F4_1)
GPIO.setup("P8_30",GPIO.IN,0) #Funnel 4 Fan 2 (F4_2)

#Set up LCD
#Name pins used
lcd_rs        = 'P8_8'
lcd_en        = 'P8_10'
lcd_d4        = 'P8_18'
lcd_d5        = 'P8_16'
lcd_d6        = 'P8_14'
lcd_d7        = 'P8_12'
lcd_backlight = 'P8_7'
lcd_columns = 20
lcd_rows    = 4

#Create LCD object
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#Setup relay control pins
GPIO.setup("P8_41",GPIO.OUT) #Funnel 1
GPIO.output("P8_41",GPIO.HIGH)
GPIO.setup("P8_42",GPIO.OUT) #Funnel 2
GPIO.output("P8_42",GPIO.HIGH)
GPIO.setup("P8_43",GPIO.OUT) #Funnel 3
GPIO.output("P8_43",GPIO.HIGH)
GPIO.setup("P8_44",GPIO.OUT) #Funnel 4
GPIO.output("P8_44",GPIO.HIGH)
#print("Realy Control Pin Setup Complete")

#Set up LED control
GPIO.setup("P8_27",GPIO.OUT) #Red of RGB
GPIO.setup("P8_29",GPIO.OUT) #Green of RGB
GPIO.setup("P8_39",GPIO.OUT) #Blue of RGB
#print("LED Control Pin Setup Complete")

#Start PWM pins
#PWM.start(Channel, duty cycle, frequency)
PWM.start("P8_13",0,25000) #Funnel 1 
PWM.start("P8_19",0,25000) #Funnel 2 
PWM.start("P9_14",0,25000) #Funnel 3 
PWM.start("P9_16",0,25000) #Funnel 4 
#print("PWM Fan Control Pin Setup Complete")

#Set up ADC
ADC.setup()

######################################################################################

lcd.clear()
lcd.message("Setup Complete\nPress Enter to\nStart Tests")
raw_input("Press Enter to start tests")


#Test LED
lcd.clear()
lcd.message("Testing\nRGB LED")
GPIO.output("P8_27",GPIO.HIGH)
time.sleep(1)
GPIO.output("P8_27",GPIO.LOW)
GPIO.output("P8_29",GPIO.HIGH)
time.sleep(1)
GPIO.output("P8_29",GPIO.LOW)
GPIO.output("P8_39",GPIO.HIGH)
time.sleep(1)
GPIO.output("P8_39",GPIO.LOW)
lcd.clear()
lcd.message("RGB LED\nTest Complete\nPress ENTER to\nContinue")
raw_input("LED Test Complete. Press Enter to Continue...")

#Turn fan on and off
#To turn fan off, put pin HIGH
#To turn fan on, put pin LOW
#Pins defualt to HIGH

######################################################################################

#Turn on each set of fans at once and test PWM control and TAC reading
#Testing of funnel 1
lcd.clear()
lcd.message("Testing:\nFunnel 1\nPress ENTER to Start")
raw_input("Testing Funnel 1 Press ENTER to Start")

#Turn on funnel 1
GPIO.output("P8_41",GPIO.LOW)

#Wait till fans are at 0 PWM RPM
lcd.clear()
lcd.message("Funnel 1 Start\nSpinning Up\nTesting 0 PWM RPM")
print("Funnel 1 Start Spinning Up Testing 0 PWM RPM")
time.sleep(7)

prev_time = time.time()
current_time = time.time()
time_delta = current_time - prev_time
#Read TAC to check speed for 1 second
while time_delta < interval:
	#Read TAC pin for F1.1 and F1.2
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

print(Count_F1_1/2)
print(Count_F1_2/2)

#Turn off funnel 1
GPIO.output("P8_41",GPIO.HIGH)

######################################################################################

#Testing of funnel 2
lcd.clear()
lcd.message("Testing:\nFunnel 2\nPress ENTER to Start")
raw_input("Testing Funnel 2 Press ENTER to Start")

#Turn on funnel 2
GPIO.output("P8_42",GPIO.LOW)

#Wait till fans are at 0 PWM RPM
lcd.clear()
lcd.message("Funnel 2 Start\nSpinning Up\nTesting 0 PWM RPM")
print("Funnel 2 Start Spinning Up Testing 0 PWM RPM")
time.sleep(7)

prev_time = time.time()
current_time = time.time()
time_delta = current_time - prev_time
#Read TAC to check speed for 1 second
while time_delta < interval:
	#Read TAC pin for F1.1 and F1.2
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

print(Count_F2_1/2)
print(Count_F2_2/2)

#Turn off funnel 2
GPIO.output("P8_42",GPIO.HIGH)

#Throw error if either fan does not spin between 50 and 53 Hz
#if Count_F2_1/2 < 50 or Count_F2_1/2 > 53:
#	lcd.clear()
#	lcd.message("ERROR:\nF2_1 Not Spinning Up")
#	print("ERROR: F2_1 Not Spinning Up")
#	sys.exit()

#if Count_F2_2/2 < 50 or Count_F2_2/2 > 53:
#	lcd.clear()
#	lcd.message("ERROR:\nF2_2 Not Spinning Up")
#	print("ERROR: F2_2 Not Spinning Up")
#	sys.exit()

######################################################################################

#Testing of funnel 3
lcd.clear()
lcd.message("Testing:\nFunnel 3\nPress ENTER to Start")
raw_input("Testing Funnel 3 Press ENTER to Start")

#Turn on funnel 3
GPIO.output("P8_43",GPIO.LOW)

#Wait till fans are at 0 PWM RPM
lcd.clear()
lcd.message("Funnel 3 Start\nSpinning Up\nTesting 0 PWM RPM")
print("Funnel 3 Start Spinning Up Testing 0 PWM RPM")
time.sleep(7)

prev_time = time.time()
current_time = time.time()
time_delta = current_time - prev_time
#Read TAC to check speed for 1 second
while time_delta < interval:
	#Read TAC pin for F1.1 and F1.2
	TAC_Val_F3_1 = GPIO.input("P8_17")
	TAC_Val_F3_2 = GPIO.input("P8_26")

	#See if the state of the pin has changed
	if TAC_Val_F3_1 != Prev_TAC_Val_F3_1:
		Prev_TAC_Val_F3_1 = TAC_Val_F3_1
		Count_F3_1 = Count_F3_1 + 1
	
	if TAC_Val_F3_2 != Prev_TAC_Val_F3_2:
		Prev_TAC_Val_F3_2 = TAC_Val_F3_2
		Count_F3_2 = Count_F3_2 + 1

	current_time = time.time()
	time_delta = current_time - prev_time

print(Count_F3_1/2)
print(Count_F3_2/2)

#Turn off funnel 3
GPIO.output("P8_43",GPIO.HIGH)

######################################################################################

#Testing of funnel 4
lcd.clear()
lcd.message("Testing:\nFunnel 4\nPress ENTER to Start")
raw_input("Testing Funnel 4 Press ENTER to Start")

#Turn on funnel 4
GPIO.output("P8_44",GPIO.LOW)

#Wait till fans are at 0 PWM RPM
lcd.clear()
lcd.message("Funnel 4 Start\nSpinning Up\nTesting 0 PWM RPM")
print("Funnel 4 Start Spinning Up Testing 0 PWM RPM")
time.sleep(7)

prev_time = time.time()
current_time = time.time()
time_delta = current_time - prev_time
#Read TAC to check speed for 1 second
while time_delta < interval:
	#Read TAC pin for F1.1 and F1.2
	TAC_Val_F4_1 = GPIO.input("P8_28")
	TAC_Val_F4_2 = GPIO.input("P8_30")

	#See if the state of the pin has changed
	if TAC_Val_F4_1 != Prev_TAC_Val_F4_1:
		Prev_TAC_Val_F4_1 = TAC_Val_F4_1
		Count_F4_1 = Count_F4_1 + 1
	
	if TAC_Val_F4_2 != Prev_TAC_Val_F4_2:
		Prev_TAC_Val_F4_2 = TAC_Val_F4_2
		Count_F4_2 = Count_F4_2 + 1

	current_time = time.time()
	time_delta = current_time - prev_time

print(Count_F4_1/2)
print(Count_F4_2/2)

#Turn off funnel 4
GPIO.output("P8_44",GPIO.HIGH)

######################################################################################

lcd.clear()
GPIO.cleanup()
PWM.cleanup()
