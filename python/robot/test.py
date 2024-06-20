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
while True:
    MoveRight(0.3)
    time.sleep(1)
