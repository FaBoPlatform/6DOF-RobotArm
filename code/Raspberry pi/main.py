import time
import RPi.GPIO as GPIO
from TB6560 import TB6560
import threading
import Param as prm
from Check_Pwm import Check_Pwm
import socket
from contextlib import closing
import Adafruit_PCA9685
import ipget

t1 = TB6560(14,15) #Bottom
t2 = TB6560(17,27) #Second1
t3 = TB6560(23,24) #Second2
t4 = TB6560(10,11) #Thread
t5 = TB6560(25,8)  #Forth
t6 = TB6560(19,20) #Arm

port = 8885
buff_size = 4096
Arm_open = True

def Create_Socket(ip_addr):
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	server_socket.bind((ip_addr,port))
	print "It is Waiting Now"
	return server_socket
	
def Get_Ip_Addr():
	ip_class = ipget.ipget()
	ip_addr = ip_class.ipaddr("wlan0")[:ip_class.ipaddr("eth0").index('/')]
	print "IP address = " + ip_addr
	return ip_addr

def Arm_init():
	pwm = Adafruit_PCA9685.PCA9685()
	pwm.set_pwm_freq(60)
	pwm.set_pwm(0, 0, 300)
	return pwm

def Stop(TB):
	for i in range(len(TB)):
		TB[i].stop()
	
def Move(arm,TB):
	if arm == 0:
		TB[0].Pulse(3000,prm.FORWARD)
	elif arm == 1:	
		TB[1].Pulse(1000,prm.FORWARD)
		TB[2].Pulse(1000,prm.FORWARD)
	elif arm == 2:
		TB[3].Pulse(3000,prm.FORWARD)
	elif arm == 3:
		TB[4].Pulse(1000,prm.FORWARD)
	else:
		TB[5].Pulse(1000,prm.FORWARD)

if __name__ == '__main__':
	ip_addr = Get_Ip_Addr()
	server_socket = Create_Socket(ip_addr)
	TB = [t1,t2,t3,t4,t5,t6]
	arm = 0
	cp = Check_Pwm(TB)
	pwm = Arm_init()
	while True:	
		print "arm = "+str(arm)
		message = sock.recv(bufsize)
		x = message[0:message.find(':')] if ":" in message else message
		print "x = " + x
		if x == '1':
			arm = arm + 1 if arm < 4 else 0
			
		elif x == '2':
			Stop(TB)
			break
			
		elif x == '3':
			pwm.set_pwm(0,0,500) if Arm_open else pwm.set_pwm(0,0,300)
			Arm_open =not(Arm_open)
			
 		elif "-" in x:
			Move(arm,TB) if not("0.0" in x) else Stop(TB)
				
		elif not("0.0" in x):
			Move(arm,TB)
		else :
			Stop(TB)
		time.sleep(0.1)
		
	server_socket.close()
	GPIO.cleanup()