from controller import Robot
import requests

# Create the robot instance
robot = Robot()

# Constants
TIME_STEP = 5
MAX_SPEED = 2
WHEEL_RADIUS = 0.1
LENGTH_SIDE = 1.0

# Robot variables
START_POS_X = 0
START_POS_Y = 9
CURRENT_POS = [START_POS_X, START_POS_Y]
COLOR = robot.getCustomData()
NAME = robot.getName()

# Websockets server URL
server_url = "http://192.168.0.69:5000/";

# Calculate linear velocity and movement duration
linear_velocity = WHEEL_RADIUS * MAX_SPEED
duration_side = LENGTH_SIDE / linear_velocity

# Get the motors
leftfront_motor = robot.getDevice('Wheel1')
leftback_motor = robot.getDevice('Wheel4')
rightfront_motor = robot.getDevice('Wheel2')
rightback_motor = robot.getDevice('Wheel3')

# Initialize motors to infinity position and 0 velocity
motors = [leftfront_motor, leftback_motor, rightfront_motor, rightback_motor]
for motor in motors:
    if motor is None:
        raise ValueError("Error: One or more motors could not be found. Please check the device names.")
    motor.setPosition(float('inf'))
    motor.setVelocity(0.0)

# Function to move a space forward
def one_space():
    start_time = robot.getTime()
    end_time = start_time + 5.01  # Duration to drive forward
    while robot.step(TIME_STEP) != -1:
        current_time = robot.getTime()
        if current_time < end_time:
            left_speed = MAX_SPEED
            right_speed = MAX_SPEED
        else:
            left_speed = 0
            right_speed = 0
        leftfront_motor.setVelocity(left_speed)
        leftback_motor.setVelocity(left_speed)
        rightfront_motor.setVelocity(right_speed)
        rightback_motor.setVelocity(right_speed)
        if current_time >= end_time:
            break

# function to move a space back
def space_back():
    start_time = robot.getTime()
    end_time = start_time + 5.01  # Duration to drive forward
    while robot.step(TIME_STEP) != -1:
        current_time = robot.getTime()
        if current_time < end_time:
            left_speed = -MAX_SPEED
            right_speed = -MAX_SPEED
        else:
            left_speed = 0
            right_speed = 0
        leftfront_motor.setVelocity(left_speed)
        leftback_motor.setVelocity(left_speed)
        rightfront_motor.setVelocity(right_speed)
        rightback_motor.setVelocity(right_speed)
        if current_time >= end_time:
            break

# Function to turn right by 45 degrees
def turn_right():
    start_time = robot.getTime()
    end_time = start_time + 2.95 # Duration to turn 45 degrees (calibrate as needed)
    while robot.step(TIME_STEP) != -1:
        current_time = robot.getTime()
        if current_time < end_time:
            left_speed = 0.5 * MAX_SPEED
            right_speed = -0.5 * MAX_SPEED
        else:
            left_speed = 0
            right_speed = 0
        leftfront_motor.setVelocity(left_speed)
        leftback_motor.setVelocity(left_speed)
        rightfront_motor.setVelocity(right_speed)
        rightback_motor.setVelocity(right_speed)
        if current_time >= end_time:
            break

# Function to turn left by 45 degrees
def turn_left():
    start_time = robot.getTime()
    end_time = start_time + 2.95  # Duration to turn 45 degrees (calibrate as needed)
    while robot.step(TIME_STEP) != -1:
        current_time = robot.getTime()
        if current_time < end_time:
            left_speed = -0.5 * MAX_SPEED
            right_speed = 0.5 * MAX_SPEED
        else:
            left_speed = 0
            right_speed = 0
        leftfront_motor.setVelocity(left_speed)
        leftback_motor.setVelocity(left_speed)
        rightfront_motor.setVelocity(right_speed)
        rightback_motor.setVelocity(right_speed)
        if current_time >= end_time:
            break

# function to move one space right
def space_right():
    turn_right()
    one_space()
    turn_left()

# function to move one space left
def space_left():
    turn_left()
    one_space()
    turn_right()


# Get the direction the robot has to go
def direction_fun(current_pos, next_pos):
    if next_pos[0] > current_pos[0]:
        return "right"
    elif next_pos[1] < current_pos[1]:
        return "up"
    elif next_pos[1] > current_pos[1]:
        return "down"
    elif next_pos[0] < current_pos[0]:
        return "left"
    return "wait"

def senddata():
    # Fill json with the current robot data
    jsonfile = {
        "robots": [
            {
                "name": NAME,
                "current_position": CURRENT_POS,
                "color" : COLOR,
                "direction": 12
            }
        ]
    }
    # Send robot data to the server
    senddata = requests.post(server_url + 'send_data', json = jsonfile)

def move_next_space():
    global CURRENT_POS
     # Get robot data from the server
    response = requests.get(server_url + 'get_data')
    data = response.json()
    if 'robots' in data:
      for robotReceived in data['robots']:
          if all(key in robotReceived for key in ('name', 'current_position', 'next_position')):
    # Check if this robot has to move
              if robotReceived['name'] == NAME:
    # Check if the server knows the current location of the robot
                  if robotReceived['current_position'] == CURRENT_POS:
    # Drive the robot
                      direction = direction_fun(robotReceived['current_position'], robotReceived['next_position'])
                      print(direction)
                      match direction:
                          case "up":
                              one_space()
                          case "down":
                              space_back()
                          case "right":
                              space_right()
                          case "left":
                              space_left()
                          case "wait":
                              continue
                      CURRENT_POS = robotReceived['next_position']
                      senddata()
          else:
              print({'message': 'Data received successfully but keys are weird'})
                     
senddata()       
# Main loop
while robot.step(TIME_STEP) != -1:
    if (robot.getTime()%1 < TIME_STEP/1000.0):
        move_next_space()
   
   
        
    