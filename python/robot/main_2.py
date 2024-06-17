from machine import Pin, PWM
import network
import usocket as socket
import ujson as json
import time
import urequests

# Setup lokale netwerk en wifi-verbinding
ssid = 'TP-Link_5114'
password = '44908034'
serverAddr = "192.168.0.25"
serverPort = 5000

# Setup hardware
led = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)
pwmR = PWM(Pin(6))
pwmR.freq(50)
pwmL = PWM(Pin(7))
pwmL.freq(50)

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
    try:
        url = f"http://{serverAddr}:{serverPort}/get_state"
        response = urequests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Ontvangen gegevens:", data)
            current_state = data.get('state')
            print(f"Huidige state is: {current_state}")
            execute_command(current_state)
        else:
            print("Mislukt om gegevens op te halen:", response.status_code)
    except Exception as e:
        print("Fout bij ophalen van gegevens:", e)

# Functie om commando's uit te voeren
def execute_command(command):
    if command == 'MOVE_FORWARD':
        MoveForward(1)
    elif command == 'MOVE_BACKWARD':
        MoveBackward(1)
    elif command == 'MOVE_LEFT':
        MoveLeft(1)
    elif command == 'MOVE_RIGHT':
        MoveRight(1)
    else:
        print("Onbekend commando:", command)

# Definieer functies voor bewegingen
def MoveForward(duration):
    print(f"Moving forward for {duration} seconds")
    pwmL.duty_u16(6000)
    pwmR.duty_u16(4000)
    time.sleep(duration)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveBackward(duration):
    print(f"Moving backward for {duration} seconds")
    pwmL.duty_u16(4000)
    pwmR.duty_u16(6000)
    time.sleep(duration)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveLeft(duration):
    print(f"Turning left for {duration} seconds")
    pwmL.duty_u16(4000)
    pwmR.duty_u16(4000)
    time.sleep(duration)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveRight(duration):
    print(f"Turning right for {duration} seconds")
    pwmL.duty_u16(6000)
    pwmR.duty_u16(6000)
    time.sleep(duration)
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

while True:
    # Behandel GET-verzoeken op gespecificeerd interval
    if time.time() >= next_get_request_time:
        handle_get_request()
        next_get_request_time = time.time() + get_request_interval
