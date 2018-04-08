import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

cw0 = 21
cw1 = 12
cw2 = 6
cw3 = 5
cw4 = 4
pwm_ch0 = 0
pwm_ch1 = 1
pwm_ch2 = 2
pwm_ch3 = 3
pwm_ch4 = 4
duty = 50
DEF = 999

cw_pin = [cw0,cw1,cw2,cw3,cw4]
pwm_ch = [pwm_ch0,pwm_ch1,pwm_ch2,pwm_ch3,pwm_ch4]
pwm = Adafruit_PCA9685.PCA9685()

def setup():
	GPIO.setmode(GPIO.BCM)
	for c in cw_pin:
		GPIO.setup(c,GPIO.OUT)
		
def fin():
	for i in pwm_ch:
		pwm.set_pwm(i,0,0)
	GPIO.cleanup()
	
def stop(I,pre_I):
	if pre_I[0] == DEF: return 
	elif I[0] != pre_I[0]: pwm.set_pwm(pre_I[0],0,0)

def move(I):
	pwm.set_pwm_freq(I[1])
	GPIO.output(cw_pin[I[0]],I[2])
	pwm.set_pwm(I[0],0,duty)
	
def change_info(I,pre_I):
	if I[1] != pre_I[1]:	
		pwm.set_pwm_freq(I[1])
	GPIO.output(cw_pin[I[0]],I[2])
		
def test():
	setup()
	pre_I = [DEF,DEF,DEF]
	while(1):
		I = map(int,raw_input().split())
		if I[0] > 4: break
		elif I[0] == pre_I[0]:
			change_info(I,pre_I)
		else:
			stop(I,pre_I)
			move(I)
		pre_I = I
	fin()

if __name__ == '__main__':
    test()