import RPi.GPIO as GPIO
import time
import os
import socket

#TCP_IP = '192.168.1.12'
#TCP_PORT = 9001
#BUFFER_SIZE = 1024
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#variables:

butPressed1 = True #if button i is pressed, then butPressed[i] is False
butPressed2 = True 
pin1 = 21
pin2 = 20  #GPIO pins of each button
recordBool = False #True if a record is in progress
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(21,  GPIO.IN, pull_up_down=GPIO.PUD_UP) #sets Pi's internal resistors to pull-up

while butPressed2 == True:
	butPressed1 = GPIO.input(pin1) #checks if a button is pressed
	butPressed2 = GPIO.input(pin2)  
	
	#if butPressed1 == False: #if a button is pressed
	#	previousTime = time.time()
	#	while butPressed1  == False and recordBool == False:
	#		butPressed1 = GPIO.input(pin1)
	#		if time.time() - previousTime > 1.0: #if the button is pressed for more than a second, then recordBool is True
	#			recordBool = True
	#	if recordBool == True: #if recordBool is True, it plays a beep sound and then records
	#		os.system("aplay -D plughw:CARD=1,DEV=0 beep.wav")
	#		os.system("arecord recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") #records for maximum 20 seconds in file i.wav, with cd quality
			
			#butPressed1 = False
			#while butPressed1 == False:
			#	butPressed1 = GPIO.input(pin1)
			#os.system("pkill -9 arecord") #the record is stopped when the button is let go, or after 20 seconds
	#		recordBool = False
	#	else: #if recordBool is False, it plays sound i.wav
	#		os.system("aplay -D plughw:CARD=1,DEV=0 recorded_audio.wav")
			
	if butPressed2 == False:
                while butPressed2 == False:
                    butPressed2 = GPIO.input(pin2)
                os.system("lxterminal -e /home/pi/Documents/python_script/testaudio2.py")
                butPressed2 = False
           #     os.system("echo uploading recorded_audio.wav ...")
            #    os.system("~/Documents/gdrive-linux-rpi upload recorded_audio.wav")
             #   os.system("echo upload success !!!")
                
                
	#if butPressed2 == False :
	#	s.connect((TCP_IP, TCP_PORT))
	#	with open('received_file', 'wb') as f:
    	#		print 'file opened'
    	#		while True:
        			#print('receiving data...')
        #			data = s.recv(BUFFER_SIZE)
        #			print('data=%s', (data))
        #			if not data:
         #   				f.close()
          #  				print 'file close()'
           # 				break
        #			# write data to a file
        #			f.write(data)
#
#		print('Successfully get the file')
#		s.close()
#		print('connection closed')
time.sleep(0.1)
