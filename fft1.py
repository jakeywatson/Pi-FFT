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
	maxout = np.amax(output)
	maxin = np.amax(fd)

	screen.fill(black)

	for i in range (0, len(output)):	
		endposout = sh -  (15)*((output[i]/maxout)*(sh/2) )
		pygame.draw.line(screen, white, (i*1.5, sh) , (i*1.5, endposout) , 1)
	pygame.draw.rect(screen, black, (0, 0, sw, sh/2), 0)
	for i in rn:
		endposin = (sh/2)- (0.75)*((float(fd[i])/maxin)*(sh/2))
		pygame.draw.line(screen, red , (i, (sh/2)) , (i, endposin) , 1)
	
	pygame.display.flip()
	
	pygame.image.save(screen, "trumpettestg.png")

	
