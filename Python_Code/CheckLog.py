#!/usr/bin/env python

#Creation Date: 02/08/2016
#Last Edited: 05/31/2016
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

#Create update list
#This list will be used to inform user what stage the program is at 
info_msg_list = ['Funnel 1: Testing...\nFunnel 2: Standby\nFunnel 3: Standby\nFunnel 4: Standby',
'Funnel 1: Ready\nFunnel 2: Testing...\nFunnel 3: Standby\nFunnel 4: Standby',
'Funnel 1: Ready\nFunnel 2: Ready\nFunnel 3: Testing...\nFunnel 4: Standby',
'Funnel 1: Ready\nFunnel 2: Ready\nFunnel 3: Ready\nFunnel 4: Testing...',
'System Ready\nTurbine Spinning Up']

#Create error code list
#0 index is blank so error 1 lines up with index 1
err_msg_list = ['', 
"ERROR CODE: 1\nF1_1 Not Working",
"ERROR CODE: 2\nF1_2 Not Working",
"ERROR CODE: 3\nFunnel 1 Not \nWorking",
"ERROR CODE: 4\nF2_1 Not Working",
"ERROR CODE: 5\nF2_2 Not Working",
"ERROR CODE: 6\nFunnel 2 Not\nWorking",
"ERROR CODE: 7\nF3_1 Not Working",
"ERROR CODE: 8\nF3_2 Not Working",
"ERROR CODE: 9\nFunnel 3 Not\nWorking",
"ERROR CODE: 10\nF4_1 Not Working",
"ERROR CODE: 11\nF4_2 Not Working",
"ERROR CODE: 12\nFunnel 4 Not\nWorking"]

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
status = txt.readlines()
txt.close()

#Remove '\n' character
for i in range(0,len(status)):
	status[i] = status[i].strip('\n')

#Based on status, LED will change to a certain color
if status[0] == 'Green':
	GPIO.output("P8_29",GPIO.HIGH) #GREEN
	lcd.clear()
	lcd.message("System Green\nNo Errors")
elif status[0] == 'Blue':
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
		#Set old mod time to the new one
		OldModTime = NewModTime
		
		#Open file and read status
		del status[:]
		txt = open('/usr/PythonCode/RunLog.txt') 
		status = txt.readlines()
		txt.close()
		
		#Remove '\n' character
		for c in range(0,len(status)):
			status[c] = status[c].strip('\n')

		#Clear screen
		lcd.clear()
		time.sleep(0.5)

		#Turn off LED 
		GPIO.output("P8_29",GPIO.LOW)
		GPIO.output("P8_39",GPIO.LOW)
		GPIO.output("P8_27",GPIO.LOW)

		if status[0] == 'Green':
			#Recreate the LCD object because it makes the code work
			lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
			lcd.message("System Green\nNo Errors")
			GPIO.output("P8_29",GPIO.HIGH) #GREEN
		elif status[0] == 'Blue':
			#Recreate the LCD object because it makes the code work
			lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
			
			#Display correct info message based on info number
			info_msg = info_msg_list[int(status[1])]
			lcd.message(info_msg)
			GPIO.output("P8_39",GPIO.HIGH) #BLUE
		elif status[0] == 'Red':
			#Recreate the LCD object because it makes the code work
			lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
			
			#Display correct error message based on error code
			error_msg = err_msg_list[int(status[1])]
			lcd.message(error_msg)
			GPIO.output("P8_27",GPIO.HIGH) #RED