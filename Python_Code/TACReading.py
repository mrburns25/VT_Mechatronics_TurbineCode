#!/usr/bin/env python

#Creation Date: 08/15/2016
#Last Edited: 12/20/2016
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
    usr_ans = input("Funnel # (1-4): ")
    
    print('Funnel ' + str(usr_ans) + ' Selected')
    print('Turning on...\n')
    #Turn on funnel and wait till idle
    funnel_list[usr_ans - 1].Turn_On()
    
    test_speed = input("Enter Test PWM: ")
    print("Spinning to desired speed...\n")
    #PWM wires for F2 and F3 were flipped when wire harness was made
    #This will fix that mistake
    if usr_ans == 2:
        #Send signal through pwm pin for F3
        funnel_list[2].Set_Speed(test_speed)
    elif usr_ans == 3:
        #Send singnal through pwm pin for F2
        funnel_list[1].Set_Speed(test_speed)
    else:
        funnel_list[usr_ans - 1].Set_Speed(test_speed)
    
    raw_input('Press Enter to take samples\n')
    print('Taking ' + str(test_speed) + ' PWM Samples...\n')
    
    #Make file to write to
    file_name = "Funnel_" + str(usr_ans) + "_" + str(test_speed) + "_PWM_Test.txt"
    file_path = "/usr/local/Turbine/TAC_Data/" + file_name
    
    print("Writing results to:\n")
    print(file_path + '\n')
    
    for i in range(0,100):
        #Take samples at defined PWM
        pwm_results = funnel_list[usr_ans - 1].Take_Sample()
        
        #Write to file
        data_to_write = str(pwm_results["TAC1_Freq"]) + ',' + str(pwm_results["TAC2_Freq"])
        file = open(file_path,'a')
        file.write(data_to_write + '\n')
        file.close()
        
        #Print results
        print("TAC1 Freq: " + str(pwm_results["TAC1_Freq"]))
        print("TAC2 Freq: " + str(pwm_results["TAC2_Freq"]) + "\n")
        
        #Clear dictionary
        pwm_results.clear()
        
        #Wait 1 sec then read again
        time.sleep(0.1)
    
    #Turn Funnel off
    funnel_list[usr_ans - 1].Turn_Off()
    
    #Ask user if want to test new funnel
    #If no, set again to False which will end program
    y_n_ans = raw_input('Run Reading Again?(y/n) ')
    if y_n_ans == 'n':
        again = False
