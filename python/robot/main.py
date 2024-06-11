'''
Useful starting point to setup the work environment
https://randomnerdtutorials.com/getting-started-raspberry-pi-pico-w/

This code exposes a small webpage allowing to tunr on or off the front (Red) and back (Green) leds and allowing to move
the two wheels forward (supposedly) for 1 second at moderate speed. To be fully tested.

Upload both this file and main.html on the picoW
To test in your own house, change the ssid and password accordingly
'''


import socket
import network
import time
from machine import Pin, PWM, ADC

import urequests as requests

SERVER_URL = "192.168.0.69"
BUILT_IN_LED=25 # Built in led
FLED=20 # Front led Red
BLED=21 # Back led Green
PWM_LM=6 # Left Continuous Servo
PWM_RM=7 # Right Continuous Servo
PWM_SC=10 # Panning Servo
SDA=4
SCL=5
MISO=16
MOSI=19
SCK=18
CS=17

# insert here your network parameters
ssid=b'tesla iot'
pwd=b'fsL6HgjN'

# initial state definition
built_in_led = machine.Pin("LED", machine.Pin.OUT)
fled = Pin(FLED, Pin.OUT)
bled = Pin(BLED, Pin.OUT)
fled.value(True)
bled.value(False)
built_in_led.value(True)
time.sleep(1)
built_in_led.value(False)
time.sleep(1)
fled.value(False)

#setus up servos
LeftMotor = PWM(Pin(PWM_LM))
LeftMotor.freq(50)
RightMotor = PWM(Pin(PWM_RM))
RightMotor.freq(50)
PanMotor = PWM(Pin(PWM_SC))
PanMotor.freq(50)

# loads the local page content
page = open("main1.html", "r")
html = page.read()
page.close()

# function controlling servos
def MoveForward(power,Stime):
    # power is not used here, values should be btw 1000 and 9000 (from full forward to full reverse)
    # 5000 should be motor stopped. To be tested.
    # https://microcontrollerslab.com/servo-motor-raspberry-pi-pico-micropython/
    LeftMotor.duty_u16(7000)
    RightMotor.duty_u16(7000)
    time.sleep(Stime)
    LeftMotor.duty_u16(5000)
    RightMotor.duty_u16(5000)

def moveLeft(power, Stime):
    LeftMotor.duty_u16(9000)
    RightMotor.duty_u16(1000)
    time.sleep(Stime)
    LeftMotor.duty_u16(5000)
    RightMotor.duty_u16(5000)  

def moveRight(power, Stime):
    LeftMotor.duty_u16(1000)
    RightMotor.duty_u16(9000)
    time.sleep(Stime)
    LeftMotor.duty_u16(5000)
    RightMotor.duty_u16(5000)

# activate the Pico Lan
network.hostname("mypicow") #wlan.config(hostname="mypico")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print("Hostname set to: "+str(network.hostname()))

time0=time.time()
wlan.connect(ssid, pwd)
while 1:
    if(wlan.isconnected()):
        print("\nConnected!\n")
        built_in_led.value(True)
        break
    else:
        print(".")
        time.sleep(1)
        if(time.time()-time0>10):
            print("Connection could not be established")
            break

sta_if = network.WLAN(network.STA_IF)

print(sta_if.ifconfig()[0]) # prints the IP on the serial
jsonData = {'ip':sta_if.ifconfig()[0]}

try:
    response = requests.post(SERVER_URL + "/robot_signup", json=jsonData)
    print(response.text)
except Exception as e:
    print("Failed to send POST request:", e)

# listen on port 80
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
print("Listening to port 80\n")
s.listen(1)

while True:
    cl, addr = s.accept()
    print("Incoming connection request from: "+str(addr)+"\n")
    # here is the place where we get the request body...
    cl_file = cl.makefile('rwb', 0)
    found=False
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
           break
        if not found: 
            if str(line).find("/?PRESS=FRONT_LED_ON") !=-1:
                #print("Command_1 ON received")
                fled.value(True)
                found=True
            if str(line).find("/?PRESS_1=FRONT_LED_OFF") !=-1:
                #print("Command_1 OFF received")
                fled.value(False)
                found=True
            if str(line).find("/?PRESS_2=BACK_LED_ON") !=-1:
                #print("Command_2 ON received")
                bled.value(True)
                found=True
            if str(line).find("/?PRESS_3=BACK_LED_OFF") !=-1:
                #print("Command_2 OFF received")
                bled.value(False)
                found=True
            if str(line).find("/?PRESS_4=MOVE") !=-1:
                #print("Command MOVE received")
                MoveForward(50,1)
                found=True
            if str(line).find("/get_right") !=-1:
                print("Moving right")
                moveRight(50, 1)
                found=True   
       
    # we process the response file, We can add placeholders to turn change the page aspect
    response=html # default page, placeholders needs to be replaced before submitting
    # send the page
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(response)
    cl.close()
    
