#!/usr/bin/env python

#Creation Date: 01/05/2017
#Last Edited: 01/05/2017
#Author: Clinton Burns

#This code is used to calibrate the TAC readings
from Funnel import Funnel
import yaml
import time

#Open yaml file and read in data
file = open('/usr/local/Turbine/YAML_Files/Funnel_Setup.yaml')
funnel_setup = yaml.safe_load(file)
file.close()

#Create list of funnels and populate with funnel objects
funnel_list = list()
for funnel in funnel_setup.values():
    funnel_list.append(Funnel(funnel['Relay'], funnel['PWM'], funnel['TAC1'], funnel['TAC2']))
    print('Funnel Created')

#Output message
print("This python script will take 100 TAC readings from each fan")
print("at 0 PWM and 100 PWM and record them to the specified file path:\n")
print("/usr/local/Turbine/TAC_Data/" + '\n')
print("Files are formated as Funnel_funnel#_PWMSpeed#_PWM_Test.txt")
raw_input("Press Enter to Start Auto TAC Readings")

for funnel_select in range(0,4):
    print("##########START TEST FUNNEL " + str(funnel_select + 1) + "##########\n")
    #Turn on funnel and wait till idle
    funnel_list[funnel_select].Turn_On()
    print("Funnel " + str(funnel_select + 1) + " Turned On\n")
    
    print("Waiting Till 0 PWM Steady State (10 sec)\n")
    #Wait 10 seconds
    time.sleep(10)
    
#############################################################################################
    #PWM Speed 
    test_speed = 0
    print("SPEED SET: 0\n")
    
    #PWM wires for F2 and F3 were flipped when wire harness was made
    #This will fix that mistake
    if funnel_select == 1:
        #Send signal through pwm pin for F3
        funnel_list[2].Set_Speed(test_speed)
    elif funnel_select == 2:
        #Send singnal through pwm pin for F2
        funnel_list[1].Set_Speed(test_speed)
    else:
        funnel_list[funnel_select].Set_Speed(test_speed)

    #Make file to write to
    file_name = "Funnel_" + str(funnel_select + 1) + "_" + str(test_speed) + "_PWM_Test.txt"
    file_path = "/usr/local/Turbine/TAC_Data/" + file_name
    
    print("START " + "Funnel_" + str(funnel_select + 1) + "_" + str(test_speed) + "_PWM_Test.txt\n")

    for i in range(0,100):
        #Take samples at defined PWM
        pwm_results = funnel_list[funnel_select].Take_Sample()
        
        #Write to file
        data_to_write = str(pwm_results["TAC1_Freq"]) + ',' + str(pwm_results["TAC2_Freq"])
        file = open(file_path,'a')
        file.write(data_to_write + '\n')
        file.close()
        
        #Print results
        print("Data Point: " + str(i))
        print("TAC1 Freq: " + str(pwm_results["TAC1_Freq"]))
        print("TAC2 Freq: " + str(pwm_results["TAC2_Freq"]) + "\n")
        
        #Clear dictionary
        pwm_results.clear()
        
        #Wait 1 sec then read again
        time.sleep(0.1)
        
    print("END " + "Funnel_" + str(funnel_select + 1) + "_" + str(test_speed) + "_PWM_Test.txt\n\n")
#############################################################################################
    #PWM Speed 
    test_speed = 100
    print("SPEED SET: 100\n")
    
    #PWM wires for F2 and F3 were flipped when wire harness was made
    #This will fix that mistake
    if funnel_select == 1:
        #Send signal through pwm pin for F3
        funnel_list[2].Set_Speed(test_speed)
    elif funnel_select == 2:
        #Send singnal through pwm pin for F2
        funnel_list[1].Set_Speed(test_speed)
    else:
        funnel_list[funnel_select].Set_Speed(test_speed)

    #Make file to write to
    file_name = "Funnel_" + str(funnel_select + 1) + "_" + str(test_speed) + "_PWM_Test.txt"
    file_path = "/usr/local/Turbine/TAC_Data/" + file_name
    
    print("Waiting Till 100 PWM Steady State (15 sec)\n")
    #Wait till at 100 PWM speed
    time.sleep(15)

    print("START " + "Funnel_" + str(funnel_select + 1) + "_" + str(test_speed) + "_PWM_Test.txt\n")
    
    for i in range(0,100):
        #Take samples at defined PWM
        pwm_results = funnel_list[funnel_select].Take_Sample()
        
        #Write to file
        data_to_write = str(pwm_results["TAC1_Freq"]) + ',' + str(pwm_results["TAC2_Freq"])
        file = open(file_path,'a')
        file.write(data_to_write + '\n')
        file.close()
        
        #Print results
        print("Data Point: " + str(i))
        print("TAC1 Freq: " + str(pwm_results["TAC1_Freq"]))
        print("TAC2 Freq: " + str(pwm_results["TAC2_Freq"]) + "\n")
        
        #Clear dictionary
        pwm_results.clear()
        
        #Wait 1 sec then read again
        time.sleep(0.1)
    
    print("END " + "Funnel_" + str(funnel_select + 1) + "_" + str(test_speed) + "_PWM_Test.txt\n\n")
    
    #Turn Funnel off
    funnel_list[funnel_select].Turn_Off()
    print("Funnel " + str(funnel_select + 1) + " Turned Off\n")
    print("##########END TEST FUNNEL " + str(funnel_select + 1) + "##########\n")
