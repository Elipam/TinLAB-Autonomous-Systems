from machine import Pin, PWM
import network
import usocket as socket
import ujson as json
import time
import urequests

# Setup lokale netwerk en wifi-verbinding
ssid = 'De Froststreet 74'
password = 'Paultje4Life'
serverAddr = "192.168.68.56"
serverPort = 5000

# Setup hardware
led = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)
pwmR = PWM(Pin(6))
pwmR.freq(50)
pwmL = PWM(Pin(7))
pwmL.freq(50)

steps = []

# Verbinding maken met WiFi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('Wachten op WiFi-verbinding...')
        time.sleep(1)
    print('Verbonden met WiFi')
    print(wlan.ifconfig())
    return wlan

# Functie om GET-verzoek te behandelen en gegevens te verwerken
def handle_get_request():
    global steps  # Gebruik een globale variabele voor de stappen
    url = f"http://{serverAddr}:{serverPort}/get_state"
    response = urequests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Ontvangen gegevens:", data)
        if 'robots' not in data:
            return
        for robot in data['robots']:
            if robot.get('name') == 'Robot1':
                steps = robot.get('next_steps', [])  # Sla de 'next_steps' op in de globale 'steps'
                print(f"Robot {robot['name']} heeft de volgende acties: {steps}")

# Functie om commando's uit te voeren
def execute_command(command):
    if command == 'MOVE_FORWARD':
        MoveForward()
    elif command == 'MOVE_BACKWARD':
        MoveBackward()
    elif command == 'TURN_LEFT':
        MoveLeft()
    elif command == 'TURN_RIGHT':
        MoveRight()
    else:
        print("Waiting")

# Definieer functies voor bewegingen
def MoveForward():
    print('moving forward')
    pwmL.duty_u16(5500)
    pwmR.duty_u16(4335)
    time.sleep(1.3)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveBackward():
    print('moving backward')
    pwmL.duty_u16(3700)
    pwmR.duty_u16(6000)
    time.sleep(0.15)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveLeft():
    print('turning left')
    pwmL.duty_u16(4500)
    pwmR.duty_u16(4500)
    time.sleep(0.68)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveRight():
    print('turning right')
    pwmL.duty_u16(5400)
    pwmR.duty_u16(5400)
    time.sleep(0.55)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

# Initialiseren van hardware
led.on()
led2.on()

# Verbinding maken met WiFi
wlan = connect_to_wifi()

while True:
    steps = []  # Reset 'steps' elke iteratie
    handle_get_request()
    print(steps)
    if steps:  # Controleer of 'steps' niet leeg is
        for command in steps:
            execute_command(command)
            time.sleep(1)
    time.sleep(0.5)  # Pauzeer na elke iteratie van de while loop
