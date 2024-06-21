from machine import Pin, PWM
import time

# Setup hardware
led = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)
pwmR = PWM(Pin(6))
pwmR.freq(50)
pwmL = PWM(Pin(7))
pwmL.freq(50)

# Definieer functies voor bewegingen
def MoveForward():
    pwmL.duty_u16(6000)
    pwmR.duty_u16(3700)
    time.sleep(1)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveBackward():
    pwmL.duty_u16(3700)
    pwmR.duty_u16(6000)
    time.sleep(2)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)

def MoveLeft():
    pwmL.duty_u16(4300)
    pwmR.duty_u16(4300)
    time.sleep(0.4)
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
while True:
    MoveForward()
    time.sleep(1)
    MoveLeft()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveLeft()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveLeft()
    time.sleep(1)
    MoveRight()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveRight()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveLeft()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveRight()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveLeft()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveRight()
    time.sleep(1)
    MoveForward()
    time.sleep(1)
    MoveRight()
    time.sleep(1)