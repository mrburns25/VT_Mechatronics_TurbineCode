#!/usr/bin/env python

#Creation Date: 08/15/2016
#Last Edited: 012/20/2016
#Author: Clinton Burns

#This code is used to calibrate the TAC readings
from Funnel import Funnel
import yaml
import time

#Variable to make loop go forever till user says stop
again = True

#Open yaml file and read in data
file = open('/usr/local/Turbine/YAML_Files/Funnel_Setup.yaml')
funnel_setup = yaml.safe_load(file)
file.close()

#Create list of funnels and populate with funnel objects
funnel_list = list()
for funnel in funnel_setup.values():
    funnel_list.append(Funnel(funnel['Relay'], funnel['PWM'], funnel['TAC1'], funnel['TAC2']))
    print('Funnel Created')

while(again):
    #Ask user which funnel to test
    usr_ans = input('Funnel # (1-4): ')
    
    print('Funnel ' + str(usr_ans) + ' Selected\n')
    print('Turning on and waiting till idle...\n')
    #Turn on funnel and wait till idle
    funnel_list[usr_ans - 1].Turn_On()
    time.sleep(7)
    
    raw_input('Idle reached. Press Enter to take samples')
    print('Taking 0 PWM Samples...')
    #Take samples at 0 PWM
    pwm0_results = funnel_list[usr_ans - 1].Take_Sample()
    
    print("TAC1 Freq: " + str(pwm0_results["TAC1_Freq"]) + "\n")
    print("TAC2 Freq: " + str(pwm0_results["TAC2_Freq"]) + "\n")
    
    print('Changing to 100 PWM...')
    #Change to 100 PWM and wait till 100 PWM
    funnel_list[usr_ans - 1].Set_Speed(100)
    time.sleep(15)
    
    print('100 PWM idle reached')
    print('Taking 100 PWM Samples...')
    #Take samples at 100 PWM
    pwm100_results = funnel_list[usr_ans - 1].Take_Sample()
    
    print("TAC1 Freq: " + str(pwm0_results["TAC1_Freq"] + "\n")
    print("TAC2 Freq: " + str(pwm0_results["TAC2_Freq"] + "\n")
    
    #Ask user if want to test new funnel
    #If no, set again to False which will end program
    y_n_ans = input('Test new funnel?(y/n) ')
    if str(y_n_ans) == "n":
        again = False
