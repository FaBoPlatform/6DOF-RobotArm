from TB6560 import TB6560
import RPi.GPIO as GPIO
from Arm import Arm
import time

"""
Button list:
A :   Motor 0	: 0
B :   Motor 1	: 1
X :   Motor 2	: 2	
Y :   Motor 3	: 3	
LB :  Motor 4	: 4
RB :Servo Motor	: 5
START : 7
BACK  : 6

Servo moter 
Threashould Duty cycle 345 ~ 525
"""

t1 = TB6560(9,11) #Bottom
t2 = TB6560(14,15) #Second1
t3 = TB6560(17,27) #Second2
t4 = TB6560(25,8) #Thread
t5 = TB6560(23,24)  #Forth
t6 = TB6560(16,20) #Arm

if __name__ == '__main__':
	Robo_Arm = Arm([t1,t2,t3,t4,t5,t6])
	flag = True
	while flag:	
		Robo_Arm.Get_Data()
		flag = False if Robo_Arm.Get_Button() == "6" else True
		Robo_Arm.Decide_Move()
		time.sleep(0.02)
	Robo_Arm.Stop()
	GPIO.cleanup()
	
