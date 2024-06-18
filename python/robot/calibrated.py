MoveRight(0.67)


def MoveRight(duration):
    print(f"Turning right for {duration} seconds")
    pwmL.duty_u16(5300)
    pwmR.duty_u16(5300)
    time.sleep(duration)
    pwmL.duty_u16(5000)
    pwmR.duty_u16(5000)  

# 90 graden