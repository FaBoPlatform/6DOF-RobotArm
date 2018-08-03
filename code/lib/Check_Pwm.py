# coding: UTF-8

import Param as prm
import threading 
import time

#送ったパルス数をCheck
#指定した時間でストップ
#動作は10kHz
class Check_Pwm(threading.Thread):
	tb =[]
	def __init__(self,tb):
		super(Check_Pwm,self).__init__()
		self.setDaemon(True)
		self.tb = tb
		
	def run():
		while True:
			for n,i in enumerate(self.tb):
				if i.state == prm.Running and time.time() - i.start_time >= i.time:
					i.Change_State(prm.Waiting)
					i.stop()
			time.sleep(0.0001)
			
