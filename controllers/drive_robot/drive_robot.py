from controller import Robot
from controller import Motor

# Create the robot instance
robot = Robot()

# Get the timestep of the current world
timestep = 64
max_speed = 6.28

#Created motor instances
leftfront_motor = robot.getDevice('Wheel1')
leftback_motor = robot.getDevice('Wheel4')
rightfront_motor = robot.getDevice('Wheel2')
rightback_motor = robot.getDevice('Wheel3')
leftfront_motor.setPosition(float('inf'))
leftback_motor.setPosition(float('inf'))
rightfront_motor.setPosition(float('inf'))
rightback_motor.setPosition(float('inf'))
leftfront_motor.setVelocity(0.0)
leftback_motor.setVelocity(0.0)
rightfront_motor.setVelocity(0.0)
rightback_motor.setVelocity(0.0)

# main loop
while robot.step(timestep) != -1:
# driving the robot in a straight line  
    # left_speed = 0.5 * max_speed
    # right_speed = 0.5 * max_speed
    # leftfront_motor.setVelocity(left_speed)
    # leftback_motor.setVelocity(left_speed)
    # rightfront_motor.setVelocity(right_speed)
    # rightback_motor.setVelocity(right_speed)
# driving the robot the right on the same place
    # left_speed = -0.5 * max_speed
    # right_speed = 0.5 * max_speed
    # leftfront_motor.setVelocity(left_speed)
    # leftback_motor.setVelocity(left_speed)
    # rightfront_motor.setVelocity(right_speed)
    # rightback_motor.setVelocity(right_speed)
# driving the robot to right with a bend
    left_speed = 0.5 * max_speed
    right_speed = 0.25 * max_speed
    leftfront_motor.setVelocity(left_speed)
    leftback_motor.setVelocity(left_speed)
    rightfront_motor.setVelocity(right_speed) 
    rightback_motor.setVelocity(right_speed)  
    
    