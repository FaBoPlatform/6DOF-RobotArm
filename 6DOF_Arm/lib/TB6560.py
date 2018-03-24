# coding: UTF-8

import RPi.GPIO as GPIO
import time
import Param as prm
import threading 

#モータードライバーTB6560用のクラス
class TB6560:

	#コンストラクタ
	def __init__(self,pwm_pin,cw_pin):
		GPIO.setmode(GPIO.BCM)
		self.pwm_pin = pwm_pin
		self.cw_pin = cw_pin
		self.state = prm.Waiting
		self.time = 0
		self.start_time = 0
		GPIO.setup(self.pwm_pin,GPIO.OUT)
		GPIO.setup(self.cw_pin,GPIO.OUT)
		self.clk = GPIO.PWM(self.pwm_pin,500) 

	#pulse : 1秒間に送るパルス数
	#pos : 回転方向
	#ti : 回転時間
	def Pulse_Time(self,pulse,pos,ti):
		GPIO.output(self.cw_pin,GPIO.HIGH) if pos == prm.FORWARD else GPIO.output(self.cw_pin,GPIO.LOW)
		self.clk.ChangeFrequency(pulse)
		self.clk.start(50)
		self.time = ti
		self.start_time = time.time()
		self.state = prm.Running

	#Stateの変更
	def Change_State(self,state):
		self.state = state
		
	def Pulse(self,pulse,pos):
		GPIO.output(self.cw_pin,GPIO.HIGH) if pos == prm.FORWARD else GPIO.output(self.cw_pin,GPIO.LOW)
		self.clk.ChangeFrequency(pulse)
		self.clk.start(50)
		self.state = prm.Waiting

	#PWM出力の停止
	def stop(self):
		self.start_time = 0
		self.clk.stop()
