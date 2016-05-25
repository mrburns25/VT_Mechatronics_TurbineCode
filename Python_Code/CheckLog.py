#!/usr/bin/env python

#Creation Date: 02/08/2016
#Last Edited: 05/25/2016
#Author: Clinton Burns

#This code will check the run log for the fan code.
#Based on what is in the file, the RGB LED will be 
#changed to one of the following states:
#	BLUE = Fan program is running.
#	GREEN = Fans not running. No errors.
#	RED = Error found. Check LCD.

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_CharLCD as LCD
from collections import Counter
import os.path
import time
import sys

#Set up LED control
GPIO.setup("P8_27",GPIO.OUT) #Red of RGB
GPIO.setup("P8_29",GPIO.OUT) #Green of RGB
GPIO.setup("P8_39",GPIO.OUT) #Blue of RGB

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

#Checks to see if file is there
#If true, continue code, if not, end code
if (os.path.isfile('/usr/PythonCode/RunLog.txt') != 1):
	lcd.clear()
	lcd.message("Run Log File Not Found")
	print("Run Log File Not Found")
	sys.exit()

#See when the last modification was
OldModTime = os.path.getmtime('/usr/PythonCode/RunLog.txt')

#Open file and read status
txt = open('/usr/PythonCode/RunLog.txt') 
Status = txt.read()
txt.close()

#Based on status, LED will change to a certain color
if Counter(Status) == Counter('Green'):
	GPIO.output("P8_29",GPIO.HIGH) #GREEN
	lcd.clear()
	lcd.message("System Green\nNo Errors")
elif Counter(Status) == Counter('Blue'):
	lcd.clear()
	GPIO.output("P8_39",GPIO.HIGH) #BLUE
else:
	GPIO.output("P8_27",GPIO.HIGH) #RED
	lcd.clear()
	lcd.message("Errors")

#Now the code will enter a forever while loop
while(1):
	#Get the mod time of the run log file
	NewModTime = os.path.getmtime('/usr/PythonCode/RunLog.txt')

	#Check mod time against old mod time
	#If they do not equal, read the file to see new status
	#If they do equal, do nothing
	if(NewModTime != OldModTime):
		OldModTime = NewModTime
		
		#Open file and read status
		txt = open('/usr/PythonCode/RunLog.txt') 
		Status = txt.read()
		txt.close()

		#Clear screen
		lcd.clear()
		time.sleep(0.5)

		#Turn off LED 
		GPIO.output("P8_29",GPIO.LOW)
		GPIO.output("P8_39",GPIO.LOW)
		GPIO.output("P8_27",GPIO.LOW)


		if Counter(Status) == Counter('Green'):
			#Recreate the LCD object because it makes the code work
			lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
			lcd.message("System Green\nNo Errors")
			GPIO.output("P8_29",GPIO.HIGH) #GREEN
		elif Counter(Status) == Counter('Blue'):
			#Recreate the LCD object because it makes the code work
			lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
			lcd.message("Turbine Spinning Up")
			GPIO.output("P8_39",GPIO.HIGH) #BLUE
		elif Counter(Status) == Counter('Red'):
			#Recreate the LCD object because it makes the code work
			lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
			lcd.message("Errors")
			GPIO.output("P8_27",GPIO.HIGH) #RED
			#Errors will be printed to LCD