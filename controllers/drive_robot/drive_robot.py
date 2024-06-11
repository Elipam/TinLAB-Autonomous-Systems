from controller import Robot

# Create the robot instance
robot = Robot()

# Constants
TIME_STEP = 64
MAX_SPEED = 3
WHEEL_RADIUS = 0.05
LENGTH_SIDE = 1.0

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
    end_time = start_time + 3.5  # Duration to drive forward
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
    end_time = start_time + 3.5  # Duration to drive forward
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
    end_time = start_time + (2 - 0.032) # Duration to turn 45 degrees (calibrate as needed)
    print(start_time)
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
    end_time = start_time + (2 - 0.032)  # Duration to turn 45 degrees (calibrate as needed)
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

# Main loop
while robot.step(TIME_STEP) != -1:
    space_right()
    break  # Exit after completing the sequence

      
    
    