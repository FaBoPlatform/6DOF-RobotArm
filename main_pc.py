from __future__ import print_function
import socket
import time
from contextlib import closing
import sys
import pygame
from pygame.locals import *


host = '192.168.13.41'
port = 4000
 
if __name__ == '__main__':
	pygame.joystick.init()
	joys = pygame.joystick.Joystick(0)
	joys.init()
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	pygame.init()
	pre_message = ""
	flag = True
	while flag:
		message = ""
		for i in pygame.event.get():
			if i.type == pygame.locals.JOYBUTTONDOWN:
				message = str(i.button)
				flag = False if i.button == 2 else True
				
			elif i.type == pygame.locals.JOYAXISMOTION:
				x , y = joys.get_axis(0), joys.get_axis(1)
				message = str(round(x,1)) +':'+ str(round(y,1))
				
		if message != "": print("message = " + message)
		if message == "" and ":" in pre_message: message = pre_message
		pre_message = message
		message = message.encode('utf-8')
		print(message)
		sock.sendto(message, (host, port))
		if message == '2': break
	sock.close()