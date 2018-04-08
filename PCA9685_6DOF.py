import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685

'''
INPUT Data
data1 data2 data3 
data1 : motor
data2 : speed
data3 : position

~motor~
0 : Bottom Stepper
1 : First Joint Stepper
2 : Second Joint Stepper
3 : Third Joint Stepper
4 : Rotate Stepper
5 : Servo Motor(data2 ->0:open ->1:close)
6 : Finish
'''

#CW/CCW GPIO PIN
cw0 = 21
cw1 = 12
cw2 = 6
cw3 = 5
cw4 = 4

#PCA9685 PWM Channel
pwm_ch0 = 0
pwm_ch1 = 1
pwm_ch2 = 2
pwm_ch3 = 3
pwm_ch4 = 4

#Command
servo = 5
suspend = 6

#Parameter
servo_freq = 60
servo_open = 100
servo_close = 500
duty = 50
DEF = 999

cw_pin = [cw0,cw1,cw2,cw3,cw4]
pwm_ch = [pwm_ch0,pwm_ch1,pwm_ch2,pwm_ch3,pwm_ch4]
pwm = Adafruit_PCA9685.PCA9685()

def setup():
	#setup
	GPIO.setmode(GPIO.BCM)
	for c in cw_pin:
		GPIO.setup(c,GPIO.OUT)
	pwm.set_pwm_freq(servo_freq)
	pwm.set_pwm(servo,0,servo_open)
		
def fin():
	#Closing process
	for i in pwm_ch:
		pwm.set_pwm(i,0,0)
	GPIO.cleanup()
	
def stop(I,pre_I):
	#Stop motor
	if pre_I[0] == DEF: return 
	elif I[0] != pre_I[0]: pwm.set_pwm(pre_I[0],0,0)

def move(I,pre_I):
	#Move motor
	stop(I,pre_I)
	pwm.set_pwm_freq(I[1])
	GPIO.output(cw_pin[I[0]],I[2])
	pwm.set_pwm(I[0],0,duty)
	
def change_info(I,pre_I):
	#Change motor parameter
	if pre_I[0] == stop:
		pwm.set_pwm_freq(I[1])
	elif I[1] != pre_I[1]:	
		pwm.set_pwm_freq(I[1])
	GPIO.output(cw_pin[I[0]],I[2])
	
def servo_move(I):
	#Serve control
	pwm.set_pwm_freq(servo_freq)
	pwm.set_pwm(servo,0,servo_open + 500 * I[1])
		
def test():
	#test program
	setup()
	pre_I = [DEF,DEF,DEF]
	while(1):
		I = map(int,raw_input().split())
		print(I)
		print(I[0])
		print(I[0] == suspend)
		if I[0] > 6: break
		elif I[0] == servo: servo_move(I)
		elif I[0] == suspend: stop(I,pre_I)
		elif I[0] == pre_I[0]:change_info(I,pre_I)
		else: move(I,pre_I)
		pre_I = I
	fin()

if __name__ == '__main__':
    test()