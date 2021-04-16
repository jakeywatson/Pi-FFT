import serial
import numpy as np
import pygame
import time



pygame.init()
sw=1024
sh=800
screen = pygame.display.set_mode([sw, sh])
red = (255, 0 , 0)
white = (255 ,255 , 255)
black = (0, 0, 0)

rn = range(0, 1024)
fd =[0.0]*1024
ser=serial.Serial('/dev/ttyACM0' ,115200)
time.sleep(5)

while True:
	ser.flushInput()
	ser.write( '\x04\x02');
	data = ser.read(1024)
	
	for x in rn:
		fd[x] = ord(data[x])
	output = np.fft.rfft(fd)

	#high/low pass
	for i in range(0, len(output)):
		if (i < (8*len(output)/10)):
			output[i] = 0
		if (i >= (8*len(output)/10)):
			output[i]=output[i]

	invft = np.fft.irfft(output)
	maxout = np.amax(invft)
	maxin = np.amax(fd)

	screen.fill(black)

	for i in range (0, len(invft)):	
		endposout = sh -  0.75*((invft[i]/maxout)*(sh/2) )
		pygame.draw.line(screen, white, (i, sh) , (i, endposout) , 1)
	pygame.draw.rect(screen, black, (0, 0, sw, sh/2), 0)
	for i in rn:
		endposin = (sh/2)- (0.75)*((float(fd[i])/maxin)*(sh/2))
		pygame.draw.line(screen, red , (i, (sh/2)) , (i, endposin) , 1)
	
	pygame.display.flip()
	
	pygame.image.save(screen, "invft_square500_0.8highpass.png")

	
