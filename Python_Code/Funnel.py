#!/usr/bin/env python

#Creation Date: 08/15/2016
#Last Edited: 12/20/2016
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
    def Take_Sample(self):
        #Take TAC1 sample for 1 sec
        start_time = time.time()
        diff_time = 0
        GPIO.setup(TAC1, GPIO.IN)
        prev_pin_state = GPIO.input(self.TAC1_Pin)
        TAC1_count = 0
        while diff_time < 1:
            #Check state of pin
            GPIO.setup(TAC1, GPIO.IN)
            current_pin_state = GPIO.input(self.TAC1_Pin)
            
            if current_pin_state != prev_pin_state:
                #Add to counter
                TAC1_count = TAC1_count + 1
                #Make current state prev state
                prev_pin_state = current_pin_state
            
            current_time = time.time()
            diff_time = current_time - start_time
            
        #Take TAC2 sample for 1 sec
        start_time = time.time()
        diff_time = 0;
        prev_pin_state = GPIO.input(self.TAC2_Pin)
        TAC2_count = 0
        while diff_time < 1:
            #Check state of pin
            current_pin_state = GPIO.input(self.TAC2_Pin)
            
            if current_pin_state != prev_pin_state:
                #Add to counter
                TAC2_count = TAC2_count + 1
                #Make current state prev state
                prev_pin_state = current_pin_state
            
            current_time = time.time()
            diff_time = current_time - start_time
            
        #Take half of the TAC counts
        TAC1_Freq = TAC1_count/2
        TAC2_Freq = TAC2_count/2
        
        #return
        return {"TAC1_Freq" : TAC1_Freq, "TAC2_Freq" : TAC2_Freq}
        
    #Set the speed of the fans
    def Set_Speed(self, speed):
        PWM_Lib.set_duty_cycle(self.PWM_Pin, speed)

    #Turn the funnel on
    def Turn_On(self):
        GPIO.output(self.Relay_Pin, GPIO.HIGH)

    #Turn the funnel off
    def Turn_Off(self):
        GPIO.output(self.Relay_Pin, GPIO.LOW)
