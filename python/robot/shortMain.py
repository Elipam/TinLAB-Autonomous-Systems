from machine import Pin, PWM
import network
import usocket as socket
import ujson as json
import time
import urequests

# Setup lokale netwerk en wifi-verbinding
ssid = 'TP-Link_5114'
password = '44908034'
serverAddr = "192.168.0.69"
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
    global steps
    try:
        url = f"http://{serverAddr}:{serverPort}/get_state"
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Ontvangen gegevens:", data)
            for robot in data:
                if robot.get('name') == 'Robot10':
                    steps = robot.get('next_steps', [])
                    print(f"Robot {robot['name']} heeft de volgende acties: {steps}")
        else:
            print("Mislukt om gegevens op te halen:", response.status_code)
    except Exception as e:
        print("Fout bij ophalen van gegevens:", e)

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
    pwmL.duty_u16(6000)
    pwmR.duty_u16(3780)
    time.sleep(0.73)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveBackward():
    pwmL.duty_u16(3700)
    pwmR.duty_u16(6000)
    time.sleep(0.15)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveLeft():
    pwmL.duty_u16(4300)
    pwmR.duty_u16(4300)
    time.sleep(0.51)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveRight():
    pwmL.duty_u16(5700)
    pwmR.duty_u16(5700)
    time.sleep(0.31)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

# Initialiseren van hardware
led.on()
led2.on()

# Verbinding maken met WiFi
wlan = connect_to_wifi()

# Hoofdloop voor periodieke GET-verzoeken
get_request_interval = 2  # Interval in seconden
next_get_request_time = time.time() + get_request_interval

while not steps:  # Loop blijft draaien totdat 'steps' lijst is gevuld
    # Behandel GET-verzoeken op gespecificeerd interval
    if time.time() >= next_get_request_time:
        handle_get_request()
        if steps:
            print("Stappen:", steps)
        else:
            print("waiting")
        next_get_request_time = time.time() + get_request_interval

for step in steps:
    execute_command(step)
    time.sleep(1)

MoveBackward()