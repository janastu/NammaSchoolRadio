#!/usr/bin/python
# *** Libraries *** #
import RPi.GPIO as GPIO
import time
import os
import socket
from datetime import datetime
from subprocess import check_output

# *** Global Functions *** #
# to check if Pi is connected to internet or local server
def is_connected(network):
    try:
        if "." in network:
            network = socket.gethostbyname(network)
        s = socket.create_connection((network, 80), 2)
        return True
    except:
        return False

# to check if wifi is local network
def is_onradio():
    try:
        test = "NammaSchoolRadio" in check_output("iwgetid", universal_newlines=True)
	return test
    except:
	return False

# macro for playing audio instructions - to keep the code simple
def aplay(filename):
    os.system("aplay -D plughw:CARD=1,DEV=0 "+audioguidepath+"/"+filename)

# *** Global Variables *** #
# if button i is pressed, then button[i] is False
button1 = True 
button2 = True 
# gpio pins used 
pin1 = 21  # play, record, etc
pin2 = 20  # network related - radio, upload, etc
# flag to monitor if recorded audio is playing or not
playpause = True
# flag to check if button is pressed and held for long time
longpress = False 
# flag to monitor if radio is on or off
nammaschoolradio = True
# network verification variables
remote_server = "www.google.com"
local_server = "192.168.1.50"

# *** Setting up GPIO of Pi *** #
GPIO.setmode(GPIO.BCM)
# sets Pi's internal resistors to pull-up
GPIO.setup(20, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(21,  GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# setting folder paths
projectpath =  os.path.split(os.path.realpath(__file__))[0]
audioguidepath = projectpath + "/audio-alert"
recordingpath = projectpath + "/recordings"

aplay("lappiready.wav")

while True:
	# scan for button press
	button1 = GPIO.input(pin1) 
	button2 = GPIO.input(pin2)  
	# if button1 is pressed
	if not button1:
		previousTime = time.time()
		while not button1 and not longpress:
			button1 = GPIO.input(pin1)
			button2 = GPIO.input(pin2)
			if time.time() - previousTime > 2.0: # if the button is pressed for more than two seconds, then longpress is True
				if not button2: # if button2 is also pressed and held, then shutdown the Pi
                                    aplay("shutdown.wav")
                                    os.system("sleep 3s; shutdown now ")                                
                                    exit(0)
				longpress = True
		# if longpress is True, record audio after a 'beep'
		if longpress: 
			os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
			aplay("beep.wav")
			# records with 48000 quality
			os.system("arecord "+projectpath+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
			# scan for button press to stop recording
			button1 = True
			while button1:
				button1 = GPIO.input(pin1)
			os.system("pkill -9 arecord") 
			# converting recorded audio to mp3 and rename with date and time of recording
			os.system("lame -b 320 "+projectpath+"/recorded_audio.wav "+recordingpath+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
			longpress = False
		else:
			os.system("pkill -9 aplay")
			if playpause:
				os.system("aplay -D plughw:CARD=1,DEV=0 "+projectpath+"/recorded_audio.wav &")
				playpause = False
			else:
				playpause = True
	# if button2 is pressed		
	if not button2:
		previousTime = time.time()
		while not button2 and not longpress:
			button2 = GPIO.input(pin2)
			if time.time() - previousTime > 2.0: #if the button is pressed for more than a second, then longpress is True
		 		longpress = True
		googledrive = is_connected(remote_server)
		if (is_onradio() and is_connected(local_server)) or googledrive:
			if longpress:
				os.system("pkill -9 aplay")
				upfiles=os.listdir(recordingpath)
				if upfiles: # if there are files to upload
					os.system("echo uploading to local server ...")
												
					for i in upfiles:
						if googledrive:
                                                        aplay("gUploading.wav")
							os.system(projectpath+"/gdrive-linux-rpi upload --delete --parent 1SpDAklZ7Pu-zlWMF_a8zbZpUjvBH7zby "+recordingpath+"/"+i)
						else:							
							aplay("sUploading.wav")
							os.system("sshpass -p 'raspberry' scp "+recordingpath+"/"+i+" pi@"+local_server+":/home/pi/Documents")
							os.system("rm "+recordingpath+"/"+i)
					os.system("echo upload success !!!")
                                        aplay("Uploaded.wav")
				else:
					os.system("echo no new file to upload !!!")
					aplay("NothingToUpload.wav")
				longpress = False
			elif nammaschoolradio:
				os.system("pkill -9 aplay")
				print "echo starting namma school radio...."
				if googledrive:
                                    os.system("chromium-browser --kiosk --app=http://www.nammaschoolradio.com &")
                                else:
                                    os.system("chromium-browser --kiosk --app=http://nammahalli.radio &")
				aplay("radiostart.wav")
				nammaschoolradio = False
                        else:
                            nammaschoolradio = True
                            print "echo closing radio !!!"
                            os.system("killall chromium-browser")
		
		else:
		    print "No internet"
		    aplay("Nointernet.wav")