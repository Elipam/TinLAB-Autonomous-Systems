# MoveRight(0.67)


# def MoveRight(duration):
#     print(f"Turning right for {duration} seconds")
#     pwmL.duty_u16(5300)
#     pwmR.duty_u16(5300)
#     time.sleep(duration)
#     pwmL.duty_u16(5000)
#     pwmR.duty_u16(5000)  

# # 90 graden

import random

# Functie om een lange lijst met bewegingen te genereren
def generate_long_movement_sequence(length):
    movements = []
    directions = ["MOVE_RIGHT", "MOVE_LEFT"]
    
    # Loop om de gewenste lengte te bereiken
    while len(movements) < length:
        # Kies willekeurig een richting
        direction = random.choice(directions)
        movements.append(direction)
        movements.append("MOVE_FORWARD")  # Altijd na elke richting vooruit bewegen
        
    return movements

# Voorbeeld van het genereren van een langere sequentie van bewegingen
long_movement_sequence = generate_long_movement_sequence(20)  # Verander de lengte naar wens
print("Generated Long Movement Sequence:", long_movement_sequence)