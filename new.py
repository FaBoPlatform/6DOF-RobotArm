import wiringpi
import time
import RPi.GPIO as GPIO

cw1 = 14
pwm1 = 15
cw2 = 17
pwm2 = 27
cw3 = 23 
pwm3 = 24
cw4 = 8
pwm4 = 25
cw5 = 11
pwm5 = 9
cw6 = 16
pwm6 = 20

cw_pin = [cw1,cw2,cw3,cw4,cw5,cw6]
pwm_pin = [pwm1,pwm2,pwm3,pwm4,pwm5,pwm6]
pwm = []

def setup():
	GPIO.setmode(GPIO.BCM)
	for c in cw_pin:
		GPIO.setup(c,GPIO.OUT)
	for p in pwm_pin:
		print(p)
		GPIO.setup(p,GPIO.OUT)
		pwm.append(GPIO.PWM(p,100))
		
def fin():
	for p in pwm:
		p.stop()
	GPIO.cleanup()
	
def stop(pre_l):
	if pre_l[0] == 1 or pre_l[0] == 2:
		pwm[1].stop()
		pwm[2].stop()
	else :
		pwm[pre_l[0]].stop()

def move(l):
	if l[0] == 1 or l[0] == 2:
		pwm[1].ChangeFrequency(l[1])
		pwm[2].ChangeFrequency(l[1])
		pwm[1].start(50)
		pwm[2].start(50)
		GPIO.output(cw_pin[2],l[2])
		GPIO.output(cw_pin[1],l[2])
	else :
		pwm[l[0]].ChangeFrequency(l[1])
		pwm[l[0]].start(50)
		GPIO.output(cw_pin[l[0]],l[2])
	
def change_freq():
	if l[0] == 1 or l[0] == 2:
		pwm[1].ChangeFrequency(l[1])
		pwm[2].ChangeFrequency(l[1])
	else :
		pwm[l[0]].ChangeFrequency(l[1])
	
def change_pos():
	if [0] == 1 or l[0] == 2:
		GPIO.output(cw_pin[1],l[2])
		GPIO.output(cw_pin[2],l[2])
	else :
		GPIO.output(cw_pin[l[0]],l[2])
		
def test():
	setup()
	pre_l = [0]
	while(1):
		l = map(int,raw_input().split())
		if l[0] > 5: break
		else if l[0] == pre_l[0]:
			if l[1] != pre_l[1]:
				change_freq()
			else :
				change_pos()
		else:
			stop(pre_l)
			move(l)
		pre_l = l
	fin()

if __name__ == '__main__':
    test()