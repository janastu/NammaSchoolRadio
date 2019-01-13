#!/usr/bin/python
# *** Libraries *** #
import RPi.GPIO as GPIO
from gpiozero import LED, Button
import time
import os
import socket
import subprocess
import wave
import contextlib
from datetime import datetime
from subprocess import check_output

# *** Global Functions *** #
# to check if Pi is connected to internet or local server
def is_connected(network):
    try:
        #if ".com" in network:
        #    network = socket.gethostbyname(network)
        s = socket.create_connection((network, 80))
        return True
    except:
        return False

# to check if wifi is local network
def is_onradio():
    try:
        test = "Namdu1Radio" in check_output("iwgetid", universal_newlines=True)
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
button3 = True 

# gpio pins used 
#pin1 = 21  # play, record, etc
#pin2 = 20  # network related - radio, upload, etc
pin3 = 26  # To start FM Transmitter
led1 = LED(16)
led2 = LED(12)
but1 = Button(21)
but2 = Button(20)

# flag to monitor if recorded audio is playing or not
playpause = True
# flag to check if button is pressed and held for long time
longpress = False 
longpress2 = False
# flag to monitor if radio is on or off
nammaschoolradio = True
# network verification variables
remote_server = "www.google.com"
local_server = "192.168.1.50"

# *** Setting up GPIO of Pi *** #
GPIO.setmode(GPIO.BCM)
# sets Pi's internal resistors to pull-up
#GPIO.setup(20, GPIO.IN, pull_up_down= GPIO.PUD_UP)
#GPIO.setup(21,  GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(26,  GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# setting folder paths
projectpath =  os.path.split(os.path.realpath(__file__))[0]
audioguidepath = projectpath + "/audio-alert"
recordingpath = projectpath + "/recordings"
fmpath = os.path.abspath("/home/pi/Desktop/fm_transmitter/stream.wav")

aplay("lappiready.wav")

radio = False
duration = 5

while True:
    # scan for button press
    #button1 = GPIO.input(pin1) 
    #button2 = GPIO.input(pin2)  
    button3 = GPIO.input(pin3)

    if not button3:
        print radio
	# previousTime = time.time()
	while not button3 and not longpress2:
            button3 = GPIO.input(pin3)
            print button3
			# if time.time() - previousTime > 2.0: # if the button is pressed for more than two seconds, then longpress2 is True
				# os.system("sudo pkill fm_transmitter")
				# os.system("echo Radio transmission stopped!")
				# os.system("arecord -D hw:1,0 -c1 -d 0 -r 48000 -f S16_LE | sudo ~/Desktop/fm_transmitter/fm_transmitter -f 88.0 - &")
				# records with 48000 quality
				# os.system("arecord "+projectpath+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ")
				# converting recorded audio to mp3 and rename with date and time of recording
				# os.system("lame -b 320 "+projectpath+"/recorded_audio.wav "+recordingpath+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
				# os.system("echo Radio transmission (microphone) started!")

            if not radio:
                lines = os.popen("lynx -dump -listonly http://"+local_server+"/.upload | grep http | grep \.mp3$ | awk '{print $2}'").read()
		lines = lines.split("\n")
		lines = lines[:-1]
		# print lines
		basecmd = "wget -O ~/Desktop/fm_transmitter/stream.mp3 "
		for x in reversed(lines):
                    print x
                    os.system(basecmd + x)
                    os.system("lame --decode ~/Desktop/fm_transmitter/stream.mp3 ~/Desktop/fm_transmitter/stream.wav")
                    # os.system("ffmpeg -y -i ~/Desktop/fm_transmitter/stream.mp3 -ar 22050 ~/Desktop/fm_transmitter/stream.wav")
                    os.system("echo Radio is now transmitting!")
                    os.system("sleep 1s")
                    fname = fmpath
                    with contextlib.closing(wave.open(fname,'r')) as f:
                        frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
		    os.system("sudo ~/Desktop/fm_transmitter/fm_transmitter -f 88.0 -r ~/Desktop/fm_transmitter/stream.wav &")
                    os.system("sleep " + str(duration) + "s")
                    os.system("sudo pkill fm_transmitter")
                    os.system("echo Radio transmission stopped!")				
		radio = True

	    else:
                os.system("sudo pkill fm_transmitter")
		os.system("echo Radio transmission stopped!")
		radio = False

    # if button1 is pressed
    if but1.is_pressed:
	previousTime = time.time()
        #but1.wait_for_release()
	while but1.is_pressed:
            if time.time() - previousTime > 2.0: # if the button is pressed for more than two seconds, then longpress is True
                if but2.is_pressed: # if button2 is also pressed and held, then shutdown the Pi
                    aplay("shutdown.wav")
                    os.system("sleep 3s; shutdown now ")                                
                    exit(0)
                longpress = True
                break
		# if longpress is True, record audio after a 'beep'
	if time.time() - previousTime < 0.1: continue
	time.sleep(0.5)
	if longpress:
            led1.on()
            os.system("pkill -9 aplay") # to stop playing recorded audio (if it was)
            aplay("beep.wav")
            # records with 48000 quality
            os.system("arecord "+projectpath+"/recorded_audio.wav -D sysdefault:CARD=1 -f dat & ") 
            # scan for button press to stop recording
            but1.wait_for_press()
            #button1 = True
            #while button1:
		#button1 = GPIO.input(pin1)
            os.system("pkill -9 arecord") 
            # converting recorded audio to mp3 and rename with date and time of recording
            os.system("lame -b 320 "+projectpath+"/recorded_audio.wav "+recordingpath+"/recorded@"+datetime.now().strftime('%d%b%Y_%H:%M')+".mp3 &")
            longpress = False
            led1.off()
	else:
            #led1.on()
            os.system("pkill -9 aplay")
            if playpause:
                os.system("aplay -D plughw:CARD=1,DEV=0 "+projectpath+"/recorded_audio.wav &")
		playpause = False
	    else:
		playpause = True
            #led1.off()
    # if button2 is pressed
    if but2.is_pressed:
	previousTime = time.time()
        #but1.wait_for_release()
	while but2.is_pressed:
            if time.time() - previousTime > 2.0: # if the button is pressed for more than two seconds, then longpress is True
                if but1.is_pressed: # if button2 is also pressed and held, then shutdown the Pi
                    aplay("shutdown.wav")
                    os.system("sleep 3s; shutdown now ")                                
                    exit(0)
                longpress = True
                break
   	# if longpress is True, record audio after a 'beep'
	if time.time() - previousTime < 0.1: continue
	time.sleep(0.5)
	nammaradio = is_onradio() and is_connected(local_server)
	if longpress:
            led2.on()
            os.system("pkill -9 aplay")
            upfiles=os.listdir(recordingpath)
            if not upfiles:
                print "no new file to upload !!!"
                aplay("NothingToUpload.wav")
            else:
                if is_onradio() and is_connected(local_server):
                    print "uploading to local server"
                    for i in upfiles:
                        aplay("sUploading.wav")
                        #os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+recordingpath+"/"+i+" pi@"+local_server+":/home/pi/Documents")
                        os.system("sshpass -p 'raspberry' rsync "+recordingpath+"/"+i+" pi@"+local_server+":/home/pi/Documents/pock1/")
                        os.system("rm "+recordingpath+"/"+i)
                    print "upload success !!!"
                    aplay("Uploaded.wav")
                elif is_connected(remote_server):
                    for i in upfiles:
                        aplay("gUploading.wav")
                        os.system(projectpath+"/gdrive-linux-rpi upload --delete --parent 142rfPJUXY_X2gHt0RYXENQEPgHN72hi_ "+recordingpath+"/"+i)
                    print "upload success !!!"
                    aplay("Uploaded.wav")
                else:
                    print "No internet"
                    aplay("Nointernet.wav")
            led2.off()
            longpress = False
        else:
            led2.on()
            if nammaschoolradio:
                os.system("pkill -9 aplay")
                nammaschoolradio = False
                if is_onradio() and is_connected(local_server):
                    os.system("chromium-browser --app=http://"+local_server+" &")
                    print "starting namma school radio...."
                    aplay("radiostart.wav")
                elif is_connected(remote_server):
                    os.system("chromium-browser --app=http://www.nammaschoolradio.com/home &")
                    print "starting namma school radio...."
                    aplay("radiostart.wav")
                else:
                    print "No internet"
                    aplay("Nointernet.wav")
            else:
                nammaschoolradio = True
                print "echo closing radio !!!"
                os.system("killall chromium-browser")
            led2.off()
        """    
        if (is_connected(remote_server)) or nammaradio:
            if longpress:
                led2.on()
                os.system("pkill -9 aplay")
		upfiles=os.listdir(recordingpath)
		if upfiles: # if there are files to upload
                    os.system("echo uploading to local server ...")
												
                    for i in upfiles:
                        if nammaradio:
                            aplay("sUploading.wav")
                            #os.system("sshpass -p 'raspberry' scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "+recordingpath+"/"+i+" pi@"+local_server+":/home/pi/Documents")
                            os.system("sshpass -p 'raspberry' rsync "+recordingpath+"/"+i+" pi@"+local_server+":/home/pi/Documents/pock1/")
                            os.system("rm "+recordingpath+"/"+i)
			else:
                            aplay("gUploading.wav")
                            os.system(projectpath+"/gdrive-linux-rpi upload --delete --parent 142rfPJUXY_X2gHt0RYXENQEPgHN72hi_ "+recordingpath+"/"+i)
							
		    os.system("echo upload success !!!")
                    aplay("Uploaded.wav")
                else:
                    os.system("echo no new file to upload !!!")
                    aplay("NothingToUpload.wav")
		longpress = False
		led2.off()
            elif nammaschoolradio:
                #led2.on()
                os.system("pkill -9 aplay")
                print "echo starting namma school radio...."
                if nammaradio:
                    os.system("chromium-browser --kiosk --app=http://"+local_server+" &")
                else:
                    os.system("chromium-browser --kiosk --app=http://www.nammaschoolradio.com/home &")
                aplay("radiostart.wav")
                nammaschoolradio = False
                
            else:
                nammaschoolradio = True
                print "echo closing radio !!!"
                os.system("killall chromium-browser")
        
		
        else:
            print "No internet"
            aplay("Nointernet.wav")
	led2.off()	    
	"""	    
