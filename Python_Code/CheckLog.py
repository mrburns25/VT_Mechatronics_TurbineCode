#!/usr/bin/env python

#Creation Date: 02/08/2016
#Last Edited: 12/12/2016
#Author: Clinton Burns

#This code is in charge of checking to make sure everything is where is should be.
#It is also incharge of handling errors and informing users of the current status of the system.
#Finally, it also updates the system log
#Based on what is in the file, the RGB LED will be 
#changed to one of the following states:
#   BLUE = Fan program is running.
#   GREEN = Fans not running. No errors.
#   RED = Error found. Check LCD.

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_CharLCD as LCD
from collections import Counter
import os.path
import time
import sys
import yaml

#Function to write to system log
def write_systemlog(log_message, path):
    #Get current time in readable form
    stamp_time = time.asctime(time.localtime(time.time()))
    
    #Build message
    log = stamp_time + ' ' + log_message
    
    #Write to file
    txt_file = open(path,'a')
    txt_file.write(log)
    txt_file.close()

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

######################################################################################
#Check for yaml files and import needed files
#Error Codes
if(os.path.isfile('/usr/local/Turbine/YAML_Files/Error_Codes.yaml') != 1):
    #Display message on LCD
    lcd.clear()
    lcd.message("FATAL ERROR\nError_Codes.yaml\nNot Found")
    
    #Turn off LED 
    GPIO.output("P8_29",GPIO.LOW)
    GPIO.output("P8_39",GPIO.LOW)
    GPIO.output("P8_27",GPIO.LOW)
    #Make LED RED
    GPIO.output("P8_27",GPIO.HIGH) #RED
    
    #Exit
    sys.exit()
else:
    error_codes_file = open('/usr/local/Turbine/YAML_Files/Error_Codes.yaml')
    error_codes = yaml.safe_load(error_codes_file)
    error_codes_file.close()
    
#Status Info
if(os.path.isfile('/usr/local/Turbine/YAML_Files/Status_Info.yaml') != 1):
    #Display message on LCD
    lcd.clear()
    lcd.message("FATAL ERROR\nStatus_Info.yaml\nNot Found")
    
    #Turn off LED 
    GPIO.output("P8_29",GPIO.LOW)
    GPIO.output("P8_39",GPIO.LOW)
    GPIO.output("P8_27",GPIO.LOW)
    #Make LED RED
    GPIO.output("P8_27",GPIO.HIGH) #RED
    
    #Exit
    sys.exit()
else:
    status_info_file = open('/usr/local/Turbine/YAML_Files/Status_Info.yaml')
    status_info = yaml.safe_load(status_info_file)
    status_info_file.close()

#Log Paths
if(os.path.isfile('/usr/local/Turbine/YAML_Files/Log_Paths.yaml') != 1):
    #Display message on LCD
    lcd.clear()
    lcd.message("FATAL ERROR\nLog_Paths.yaml\nNot Found")
    
    #Turn off LED 
    GPIO.output("P8_29",GPIO.LOW)
    GPIO.output("P8_39",GPIO.LOW)
    GPIO.output("P8_27",GPIO.LOW)
    #Make LED RED
    GPIO.output("P8_27",GPIO.HIGH) #RED
    
    #Exit
    sys.exit()
else:
    #Set log path file from yaml
    log_paths_file = open('/usr/local/Turbine/YAML_Files/Log_Paths.yaml')
    log_paths = yaml.safe_load(log_paths_file)
    log_paths_file.close()
    runlog_path = log_paths['RunLog']
    systemlog_path = log_paths['SystemLog']
    
    #Check to make sure that the log files are there
    if(os.path.isfile(runlog_path) != 1):
        #Display message on LCD
        lcd.clear()
        lcd.message("FATAL ERROR\nRunLog.txt\nNot Found")
        
        #Turn off LED 
        GPIO.output("P8_29",GPIO.LOW)
        GPIO.output("P8_39",GPIO.LOW)
        GPIO.output("P8_27",GPIO.LOW)
        #Make LED RED
        GPIO.output("P8_27",GPIO.HIGH) #RED
        
        #Exit
        sys.exit()
    elif(os.path.isfile(systemlog_path) != 1):
        #Display message on LCD
        lcd.clear()
        lcd.message("FATAL ERROR\nSystemLog.txt\nNot Found")
        
        #Turn off LED 
        GPIO.output("P8_29",GPIO.LOW)
        GPIO.output("P8_39",GPIO.LOW)
        GPIO.output("P8_27",GPIO.LOW)
        #Make LED RED
        GPIO.output("P8_27",GPIO.HIGH) #RED
        
        #Exit
        sys.exit()
    
#Funnel Setup
if(os.path.isfile('/usr/local/Turbine/YAML_Files/Funnel_Setup.yaml') != 1):
#Display message on LCD
    lcd.clear()
    lcd.message("FATAL ERROR\nFunnel_Setup.yaml\nNot Found")
    
    #Turn off LED 
    GPIO.output("P8_29",GPIO.LOW)
    GPIO.output("P8_39",GPIO.LOW)
    GPIO.output("P8_27",GPIO.LOW)
    #Make LED RED
    GPIO.output("P8_27",GPIO.HIGH) #RED
    
    #Exit
    sys.exit()
######################################################################################

#Write to system log saying start up was succesfull
write_systemlog(status_info['System_Ready'], systemlog_path)

#See when the last runlog modification was
OldModTime = os.path.getmtime(runlog_path)

#Open file and read status
txt = open(runlog_path) 
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
    NewModTime = os.path.getmtime(runlog_path)

    #Check mod time against old mod time
    #If they do not equal, read the file to see new status
    #If they do equal, do nothing
    if(NewModTime != OldModTime):
        #Set old mod time to the new one
        OldModTime = NewModTime
        
        #Open file and read status
        del status[:]
        txt = open(runlog_path) 
        status = txt.readlines()
        txt.close()
        
        #Check to make sure list is not empty
        #If empty try to read the file again
        #If list is empty after 20 tries, exit with error 13
        #and exit code manual restart
        tries = 0
        while len(status) == 0:
            txt = open(runlog_path) 
            status = txt.readlines()
            txt.close()
            
            tries = tries + 1
            
            if (tries >= 20):
                #Turn off LED 
                GPIO.output("P8_29",GPIO.LOW)
                GPIO.output("P8_39",GPIO.LOW)
                GPIO.output("P8_27",GPIO.LOW)
                #Make LED RED
                GPIO.output("P8_27",GPIO.HIGH) #RED
                #Clear LCD and display error
                lcd.clear()
                lcd.message(error_codes[Err_13])
                #Write to system log
                write_systemlog(error_codes[Err_13], systemlog_path)
                while(1):
                    #Exit code
                    sys.exit()
        
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
            
            #Write to system log
            write_systemlog(status_info[status[1]], systemlog_path)
        elif status[0] == 'Blue':
            #Recreate the LCD object because it makes the code work
            lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
            
            #Display correct info message based on info number
            lcd.message(status_info[status[1]])
            GPIO.output("P8_39",GPIO.HIGH) #BLUE
            
            #Write to system log
            write_systemlog(status_info[status[1]], systemlog_path)
        elif status[0] == 'Red':
            #Recreate the LCD object because it makes the code work
            lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
            
            #Display correct error message based on error code
            lcd.message(error_codes[status[1]])
            GPIO.output("P8_27",GPIO.HIGH) #RED
            
            #Write to system log
            write_systemlog(error_codes[status[1]], systemlog_path)
