#!/usr/bin/env python

#Creation Date: 08/15/2016
#Last Edited: 12/16/2016
#Author: Clinton Burns

#Class for funnel

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM_Lib
import time

class Funnel:
    #Sets up all needed pins for the funnel
    #PWM = Relay = Relay ctrl pin, PWM Pin, TAC1 and TAC2 = TAC pins
    def __init__(self, Relay, PWM, TAC1, TAC2):
        #Instance variables for other functions to use
        self.Relay_Pin = Relay
        self.PWM_Pin = PWM
        self.TAC1_Pin = TAC1
        self.TAC2_Pin = TAC2
        
        #Set Relay pin
        #GPIO.setup(PIN, IN/OUT)
        GPIO.setup(Relay, GPIO.OUT)
        
        #Set PWM pin
        #PWM.start(PIN, duty cycle, frequency)
        PWM_Lib.start(PWM,0,25000)
        
        #Set TAC pins
        GPIO.setup(TAC1, GPIO.IN)
        GPIO.setup(TAC2, GPIO.IN)
        
    #Reads the TACs for some number of samples
    def Take_Sample(self, sample_num):
        #List to hold samples
        TAC1_Samples = list()
        TAC2_Samples = list()
        
        #Sample TAC1
        for i in range(0,sample_num):
            #Read in TAC value and read TAC till its LOW
            prev_TAC_value = GPIO.input(self.TAC1_Pin)
            sample_start_time = time.time()
            while prev_TAC_value != 0:
                prev_TAC_value = GPIO.input(self.TAC1_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in TAC value and read TAC till value its HIGH
            TAC_Val = GPIO.input(self.TAC1_Pin)
            sample_start_time = time.time()
            while TAC_Val != 1:
                TAC_Val = GPIO.input(self.TAC1_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in time at LOW to HIGH point
            Time1 = time.time()
            
            #Read in TAC value and read TAC till its LOW
            sample_start_time = time.time()
            while prev_TAC_value != 0:
                prev_TAC_value = GPIO.input(self.TAC1_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in TAC value and read TAC till value its HIGH
            sample_start_time = time.time()
            while TAC_Val != 1:
                TAC_Val = GPIO.input(self.TAC1_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in time at LOW to HIGH point
            Time2 = time.time()
            
            #Add time difference to list
            TAC1_Samples.append(Time2 - Time1)
            
        #Sample TAC2
        for i in range(0,sample_num):
            #Read in TAC value and read TAC till its LOW
            prev_TAC_value = GPIO.input(self.TAC2_Pin)
            sample_start_time = time.time()
            while prev_TAC_value != 0:
                prev_TAC_value = GPIO.input(self.TAC2_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in TAC value and read TAC till value its HIGH
            TAC_Val = GPIO.input(self.TAC2_Pin)
            sample_start_time = time.time()
            while TAC_Val != 1:
                TAC_Val = GPIO.input(self.TAC2_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in time at LOW to HIGH point
            Time1 = time.time()
            
            #Read in TAC value and read TAC till its LOW
            sample_start_time = time.time()
            while prev_TAC_value != 0:
                prev_TAC_value = GPIO.input(self.TAC2_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in TAC value and read TAC till value its HIGH
            sample_start_time = time.time()
            while TAC_Val != 1:
                TAC_Val = GPIO.input(self.TAC2_Pin)
                
                #Count how long in this loop. If over 5 seconds,
                #throw an error
                current_time = time.time()
                diff_time = current_time - sample_start_time
                if diff_time > 5:
                    #Could not detect signal edge
                    TAC1_Samples.append(0)
                    TAC2_Samples.append(0)
                    return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
                
            #Read in time at LOW to HIGH point
            Time2 = time.time()
            
            #Add time difference to list
            TAC2_Samples.append(Time2 - Time1)
        
        #Return the sample lists as a dict
        return {'TAC1_Samp':TAC1_Samples , 'TAC2_Samp':TAC2_Samples}
        
    #Set the speed of the fans
    def Set_Speed(self, speed):
        PWM_Lib.set_duty_cycle(self.PWM_Pin, speed)

    #Turn the funnel on
    def Turn_On(self):
        GPIO.output(self.Relay_Pin, GPIO.HIGH)

    #Turn the funnel off
    def Turn_Off(self):
        GPIO.output(self.Relay_Pin, GPIO.LOW)
