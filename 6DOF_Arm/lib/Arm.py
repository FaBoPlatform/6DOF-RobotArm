from TB6560 import TB6560
import Param as prm
from Check_Pwm import Check_Pwm
import Adafruit_PCA9685
from pygame.locals import *
import pygame

class Arm:
	def __init__(self,TB):
		self.x = "0.0"
		self.y = "0.0"
		self.arm = self.pre_arm = 0
		self.button = ""
		self.TB = TB
		self.pre_pos = self.pos = prm.STOP
		self.cp = Check_Pwm(self.TB)
		self.duty = 325
		self.Arm_open = True
		self.Pwm_Init()
		self.joys = self.Joy_Init()
		self.c = 0
		
	def Joy_Init(self):
		pygame.joystick.init()
		joys = pygame.joystick.Joystick(0)
		joys.init()
		pygame.init()
		return joys
		
	def Pwm_Init(self):
		self.pwm = Adafruit_PCA9685.PCA9685()
		self.pwm.set_pwm_freq(60)
		self.pwm.set_pwm(0, 0, self.duty)
		
	def Decide_Move(self):
		if self.arm == 0 or self.arm == 3:
			if self.x == "0.0": self.Stop()
			else:
				if self.arm == 0: self.pos = prm.BACKWARD if ("-" in self.x) else prm.FORWARD
				else: self.pos = prm.FORWARD if ("-" in self.x) else prm.BACKWARD
				if self.arm != self.pre_arm: self.Move()
				elif self.pre_pos != self.pos: self.Move()
		
		elif self.arm == 1 or self.arm == 2 or self.arm == 4:
			if self.y == "0.0": self.Stop()
			else :
				if self.arm == 4: self.pos = prm.FORWARD if ("-" in self.y) else prm.BACKWARD
				else: self.pos = prm.BACKWARD if ("-" in self.y) else prm.FORWARD
				if self.arm != self.pre_arm:self.Move()
				elif self.pre_pos != self.pos:self.Move()

		elif self.arm == 5:
			if self.button == "5": self.Finger()         
			self.pos = prm.STOP
			self.c = 0
		self.pre_pos = self.pos
		
		if self.pre_arm == 5 and self.arm != 5 and self.c == 0:
			self.Arm_open = not(self.Arm_open)
			self.c = 1
		self.pre_arm = self.arm
		
	def Move(self):
		if self.arm == 0:self.TB[0].Pulse(3000,self.pos)
		elif self.arm == 1:	
			self.TB[1].Pulse(1000,self.pos)
			self.TB[2].Pulse(1000,self.pos)
		elif self.arm == 2: self.TB[3].Pulse(3000,self.pos)
		elif self.arm == 3: self.TB[4].Pulse(2000,self.pos)
		else: self.TB[5].Pulse(1000,self.pos)
	
	def Finger(self):
		self.duty += 10 if self.Arm_open else -10
		if self.duty > 600 : self.duty = 600
		elif self.duty < 325: self.duty = 325
		print "f = " + str(self.duty)
		self.pwm.set_pwm(0, 0, self.duty)
	
	def Stop(self):
		for i in range(len(self.TB)): self.TB[i].stop()
		self.pos = prm.STOP
	
	def Get_Button(self):
		return self.button
	
	def Get_Data(self):
		for i in pygame.event.get():
			if i.type == pygame.locals.JOYBUTTONDOWN: self.button = str(i.button)
			elif i.type == pygame.locals.JOYBUTTONUP: self.button = ""
			elif i.type == pygame.locals.JOYAXISMOTION:
				self.x , self.y = str(round(self.joys.get_axis(0),1)), str(round(self.joys.get_axis(1),1))
				self.x = self.x if self.x != '-0.0' else '0.0'
				self.y = self.y if self.y != '-0.0' else '0.0'
		
		self.arm = int(self.button) if len(self.button) != 0 else self.arm
		print "x = " + self.x
		print "y = " + self.y
		print "button = " + self.button
		print "arm = " + str(self.arm)
		print 
 
