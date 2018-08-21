#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
import socket

REMOTE_SERVER = "www.google.com"
def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
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
nammaschoolradio = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(21,  GPIO.IN, pull_up_down=GPIO.PUD_UP) #sets Pi's internal resistors to pull-up

while True:
	butPressed1 = GPIO.input(pin1) #checks if a button is pressed
	butPressed2 = GPIO.input(pin2)  
	if butPressed1 == False: #if a button is pressed
		previousTime = time.time()
		while butPressed1  == False and recordBool == False:
			butPressed1 = GPIO.input(pin1)
			if time.time() - previousTime > 1.0: #if the button is pressed for more than a second, then recordBool is True
				recordBool = True
		if recordBool == True: #if recordBool is True, it plays a beep sound and then records
			os.system("pkill -9 aplay")
			os.system("aplay -D plughw:CARD=1,DEV=0 /home/pi/Documents/python_script/beep.wav")
			os.system("arecord /home/pi/Documents/python_script/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") #records for maximum 20 seconds in file i.wav, with cd quality
			butPressed1 = True
			while butPressed1 == True:
				butPressed1 = GPIO.input(pin1)
			os.system("pkill -9 arecord") #the record is stopped when the button is let go, or after 20 seconds
			recordBool = False
		else: #if recordBool is False, it plays sound i.wav
			os.system("pkill -9 aplay")
			os.system("aplay -D plughw:CARD=1,DEV=0 /home/pi/Documents/python_script/recorded_audio.wav &")
			
	if butPressed2 == False:
                previousTime = time.time()
		while butPressed2  == False and recordBool == False:
			butPressed2 = GPIO.input(pin2)
			if time.time() - previousTime > 1.0: #if the button is pressed for more than a second, then recordBool is True
		 		recordBool = True
		if is_connected() == False:
			os.system("pkill -9 aplay")
                        os.system("echo No internet")
                        os.system("aplay -D plughw:CARD=1,DEV=0 /home/pi/Documents/python_script/Nointernet.wav")
                elif recordBool == True:
                        os.system("pkill -9 aplay")
                        os.system("echo connecting to google drive ...")
                        os.system("aplay -D plughw:CARD=1,DEV=0 /home/pi/Documents/python_script/Uploading.wav")
                        os.system("~/Documents/python_script/gdrive-linux-rpi upload --parent 1-1ubd7ccjGg6uqu5bKaAA4el5WL8TTNq /home/pi/Documents/python_script/recorded_audio.wav")
                        os.system("echo upload success !!!")
                        os.system("aplay -D plughw:CARD=1,DEV=0 /home/pi/Documents/python_script/Uploaded.wav")
                        recordBool = False
                elif nammaschoolradio == True:
                        os.system("pkill -9 aplay")
                        os.system("echo starting namma school radio....")
                        os.system("chromium-browser --kiosk --app=http://www.nammaschoolradio.com &")
                        os.system("aplay -D plughw:CARD=1,DEV=0 /home/pi/Documents/python_script/radiostart.wav")
                        nammaschoolradio = False
                else:
                        nammaschoolradio = True
                        os.system("echo closing radio !!!")
                        os.system("killall chromium-browser")
                        
                
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

