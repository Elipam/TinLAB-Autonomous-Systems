import requests
import time
from controller import Supervisor, LED

# Maak een instantie van de robot
robot = Supervisor()
supervisorNode = robot.getSelf()

# Haal de tijd stap op van de huidige wereld
timestep = int(robot.getBasicTimeStep())
# Hoe snel de robot stappen zet
duration = (900 // timestep) * timestep

# Link alle distance sensoren
ds0 = robot.getDevice("ds0")
ds0.enable(timestep)

ds1 = robot.getDevice("ds1")
ds1.enable(timestep)

ds2 = robot.getDevice("ds2")
ds2.enable(timestep)

ds3 = robot.getDevice("ds3")
ds3.enable(timestep)

trans = supervisorNode.getField("translation")

# Alle variabelen
hostname = 'http://127.0.0.1:5000'
stopCount = 0
name = robot.getName()
afwissel = 0
switch = False
obstakel = None
obstakel1 = None
firstDirection = 'iets'
nextDirection = 'iets'
difX = None
difY = None
tarX = 0.5
tarY = 0.5

# Maak een instanties van de LED
ledU = LED("led0")
ledR = LED("led0(1)")
ledD = LED("led0(2)")
ledL = LED("led0(3)")

# Functie om de LEDS uit te zetten
def turnOff():
    ledU.set(0)
    ledR.set(0)
    ledD.set(0)
    ledL.set(0)

# Functie om de LEDS aan te zetten afhankelijk van de richting
def turnOn(direction):
    if direction == 'right':
        ledR.set(1)
    elif direction == 'left':
        ledL.set(1)
    elif direction == 'up':
        ledU.set(1)
    elif direction == 'down':
        ledD.set(1)
        
# Functie om de robot te verplaatsen
def stepTo(direction):
    global pos
    if direction == 'right':
        pos[0] += 0.1
    elif direction == 'left':
        pos[0] -= 0.1
    elif direction == 'up':
        pos[1] += 0.1
    elif direction == 'down':
        pos[1] -= 0.1
    else:
        return
    trans.setSFVec3f(pos)

# Functies om obstakels te vinden
def zoekObstakels(dis0, dis1, dis2, dis3):
    if dis0 < 500:
        obstakels.append('right')
    if dis1 < 500:
        obstakels.append('up')
    if dis2 < 500:
        obstakels.append('down')
    if dis3 < 500:
        obstakels.append('left')
    return obstakels    

# Functie om te controleren of een getal even is
def checkNumber(number):
    return number % 2
    
# Functie om horizontale richting te bepalen
def dirHori(xDiff):
    if xDiff > 0:
        return 'right'
    elif xDiff < 0:
        return 'left'
    else:
        return
        
# Functie om verticale richting te bepalen
def dirVerti(yDiff):
    if yDiff < 0:
        return 'down'
    elif yDiff > 0:
        return 'up'
    else:
        return

# Functie om van richting te veranderen
# zodat blok niet vast blijft zitten achter balk
def reset(nextDir, blokkade):
    global afwissel, switch
    if nextDir not in blokkade:
        afwissel += 1
        switch = True
        
# Functie om het delta te berekenen
def calcDiff(tar, pos):
    return tar - pos

def stopTime():
    response2 = requests.get(f'{hostname}/get_stop')
    stopper = float(response2.json()['stop_count'])
    if checkNumber(stopper) == 1:
        time.sleep(1)
        stopTime()

start_time = time.time()

def send_data_to_server(data):
    response = requests.post(f'{hostname}/data', json=data)

while robot.step(duration) != -1:
    # Verstuur een GET-verzoek naar de /get_target route om de doellocatie te ontvangen
    response = requests.get(f'{hostname}/get_target')
    target = response.json()

    if 'tarX' in target and 'tarY' in target:
        tarX = float(target['tarX'])
        tarY = float(target['tarY'])

    stopTime()

    obstakels = []
    turnOff()
    switch = False
    # Haal de positie op
    pos = supervisorNode.getPosition()
    # Rond de posities af naar het dichtstbijzijnde roosterpunt
    posX = round(pos[0] * 10) / 10  # keer 10 omdat roostergrootte 0,1 x 0,1 m is
    posY = round(pos[1] * 10) / 10
    
    # Haal de waarden van de afstandsensoren op
    distanceR = ds0.getValue()
    distanceL = ds1.getValue()
    distanceD = ds2.getValue()
    distanceU = ds3.getValue()

    zoekObstakels(distanceR, distanceU, distanceD, distanceL)
    difX = calcDiff(tarX, posX)
    difY = calcDiff(tarY, posY)
    
    reset(nextDirection, obstakels)

    if switch == True:
        firstDirection = nextDirection
        if checkNumber(afwissel) == 1:
            nextDirection = dirHori(difX)
        elif checkNumber(afwissel) == 0:
            nextDirection = dirVerti(difY)
            
    # Verstuur de JSON-gegevens naar de server
    send_data_to_server({"name": name, "firstDirection": firstDirection, "posX": posX, "posY": posY})

    turnOn(firstDirection)
    stepTo(firstDirection)
    if tarX == posX and tarY == posY:
        break