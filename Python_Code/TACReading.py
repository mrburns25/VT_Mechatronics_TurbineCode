#!/usr/bin/env python

#Creation Date: 08/15/2016
#Last Edited: 08/30/2016
#Author: Clinton Burns

#This code is used to calibrate the TAC readings
from Funnel import Funnel
import yaml
import time

#Variable to make loop go forever till user says stop
again = True

#Function to average periods and find TAC frequency
def Average(sample_results):
    #Add up total in list
    total = 0
    for period in sample_results['TAC1_Samp']:
        total = total + period
        
    #Divide by list length to get average
    average = 1/(total/len(sample_results['TAC1_Samp']))
    
    #Print TAC 1 avearge frequency
    print('TAC1 Average Frequency: ', avearge)
    
    #Add up total in list
    total = 0
    for period in sample_results['TAC2_Samp']:
        total = total + period
        
    #Divide by list length to get average
    average = 1/(total/len(sample_results['TAC2_Samp']))
    
    #Print TAC 2 average frequency 
    print('TAC2 Average Frequency: ', average)

#Open yaml file and read in data
file = open('/usr/PythonCode/Funnel_Setup.yaml')
funnel_setup = yaml.safe_load(file)
file.close()

#Create list of funnels and populate with funnel objects
funnel_list = list()
for funnel in funnel_setup.values():
    funnel_list.append(Funnel(funnel['Relay'], funnel['PWM'], funnel['TAC1'], funnel['TAC2']))
    print('Funnel Created')

while(again)
    #Ask user which funnel to test
    usr_ans = input('Funnel # (1-4): ')
    num_of_samples = input('How many samples? ')
    
    print('Funnel ' + str(usr_ans) + 'Selected\n')
    print('Turning on and waiting till idle...\n')
    #Turn on funnel and wait till idle
    funnel_list[usr_ans - 1].Turn_On()
    time.sleep(7)
    
    raw_input('Idle reached. Press Enter to take samples')
    print('Taking 0 PWM Samples...')
    #Take samples at 0 PWM
    pwm0_sample_results = funnel_list[usr_ans - 1].Take_Sample(num_of_samples)
    
    #Find and print average
    Average(pwm0_sample_results)
    
    print('Changing to 100 PWM...')
    #Change to 100 PWM and wait till 100 PWM
    funnel_list[usr_ans - 1].Set_Speed(100)
    time.sleep(7)
    
    print('100 PWM idle reached')
    print('Taking 100 PWM Samples...')
    #Take samples at 100 PWM
    pwm100_sample_results = funnel_list[usr_ans - 1].Take_Sample(num_of_samples)
    
    #Find and print average
    Average(pwm100_sample_results)
    
    #Ask user if want to test new funnel
    #If no, set again to False which will end program
    y_n_ans = input('Test new funnel?(y/n) ')
    if y_n_ans == 'n':
        again = False