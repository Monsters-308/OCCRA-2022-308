#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()


# Robot configuration code
sensors_array = Triport(Ports.PORT20)

leftWheelMotor = Motor29(brain.three_wire_port.h, False)

rightWheelMotor = Motor29(brain.three_wire_port.b, False)

conveyor1 = Motor29(brain.three_wire_port.g, False) #Y BUTTON

conveyorIntakeWheels = Motor29(brain.three_wire_port.e, False) #INTAKE, RUNS WITH CONVEYOR 1 AT SAME TIME

conveyor2 = Motor29(brain.three_wire_port.d, True)#A BUTTON, SHOOTER

lift = Motor29(brain.three_wire_port.f, False)# DOWN=HOME, RIGHT=LEVEL2, UP=LEVEL3 

controller_1 = Controller(PRIMARY)
controller_2 = controller_1

#SonicSensor = Sonar(sensors_array.f)# SonicSensor is used to help determine which level/height for lift to go to

#make 3 bumper swtiches to keep track of where the lift is
bumperLift1 = Bumper(sensors_array.a)
bumperLift2 = Bumper(sensors_array.b)
bumperLift3 = Bumper(sensors_array.c)


#Keeps track of where the lift was last at.
#0 is default value for when robot first activates.
whereLiftAt=0

#FRONT bumpers (not for lift)
bumper1 = Bumper(sensors_array.d)
bumper2 = Bumper(sensors_array.e)

lift.stop()

# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration


#----------------------------------------------------------------------------*/
#                                                                            */
#    Module:       OCCRA-2022-308                                            */
#    Author:       C:\Users\FRC                                              */
#    Created:      Tue Sep 29 2022                                           */
#    Description:  V5 project                                                */
#                                                                            */
#----------------------------------------------------------------------------*/

"""
 ---- START VEXCODE CONFIGURED DEVICES ----
 Three-wire ports:
    rightWheelMotor1 (defunct)       A
    rightWheelMotor                  B
    leftWheelMotor1 (defunct)        C
    conveyor2                        D
    conveyorIntakeWheels             E
    lift                             F
    conveyor                         G
    leftWheelMotor                   H
 
 Ports:
    sensors_array:                  20
        bumperLift1                  A
        bumperLift2                  B
        bumperLift3                  C
        bumper1                      D
        bumper2                      E

 ---- END VEXCODE CONFIGURED DEVICES ----
"""

def main():
    #import global lift variable
    global whereLiftAt

    #get controller axis positions
    Axis3=controller_1.axis3.position()/2 #for failsave set to divide by 6, normal is 1; makes robot slower
    Axis1=controller_1.axis1.position()*(.5) #failsave -1/6, normal 0.8
    
    #controllerPrint(Axis1, (1,1), True, True)

    #left: resets lift variable
    if controller_2.buttonLeft.pressing():
        whereLiftAt = 0 

    #deadzone fix
    if abs(Axis3)<2:
        Axis3=0
    if abs(Axis1)<2:
        Axis1=0

    #this initially sets both axises to moving forward/backward
    leftSpeed = Axis3
    rightSpeed = Axis3

    #this allows the robot to steer using Axis1
    if Axis1 > 0:
        leftSpeed = leftSpeed + Axis1 
        rightSpeed = rightSpeed - Axis1
    elif Axis1 < 0:
        leftSpeed = leftSpeed + Axis1
        rightSpeed = rightSpeed - Axis1 


    #adjusts for motor biases to make robot go straight
    if leftSpeed > 0:
        leftSpeed = leftSpeed +2.8
    if rightSpeed < 0:
        rightSpeed = rightSpeed -9.3




    #set speeds
    driveRight(rightSpeed, PERCENT)
    driveLeft(leftSpeed, PERCENT)

    #keeps track of where the lift is at
    b1 = bumperLift1.pressing()
    b2 = bumperLift2.pressing()
    b3 = bumperLift3.pressing()

    if b1:
        whereLiftAt = 1
        lift.stop()
    if b2:
        whereLiftAt = 2
        lift.stop()
    if b3:
        whereLiftAt = 3
        lift.stop()

    #controllerPrint(whereLiftAt, (3,3), True, True)



    #functions for controller and front bumper inputs

    conveyor1System(controller_2.buttonY.pressing(), controller_2.buttonR1.pressing())

    conveyor2System(controller_2.buttonA.pressing(), controller_2.buttonR1.pressing())
    
    liftSystem(controller_2.buttonDown.pressing(), controller_2.buttonRight.pressing(), controller_2.buttonUp.pressing(), controller_2.buttonLeft.pressing(), whereLiftAt)

    liftManual(controller_2.buttonL1.pressing(), controller_2.buttonL2.pressing(), controller_2.buttonDown.pressing(), controller_2.buttonRight.pressing(), controller_2.buttonUp.pressing())
    
    bumperSystem(bumper1.pressing(), bumper2.pressing())
    
    



#drivetrain functions
def driveLeft(speed: float, units):
    leftWheelMotor.set_velocity(int(speed), units)
    leftWheelMotor.spin(FORWARD)

def driveRight(speed: float, units):
    rightWheelMotor.set_velocity(int(speed), units)
    rightWheelMotor.spin(REVERSE)



#First conveyor belt + intake
def conveyor1System(butnY, butnR1):
    conveyor1.set_velocity(int(100), PERCENT)
    conveyorIntakeWheels.set_velocity(int(100), PERCENT)
    if butnY:
        if butnR1:
            direction = REVERSE
        else:
            direction = FORWARD
        conveyor1.spin(direction)
        conveyorIntakeWheels.spin(direction)
    else:
        conveyor1.stop()
        conveyorIntakeWheels.stop()



#lift system (using arrow buttons)
#spin motor unitl sonic sensor reaches the correct spot while button is held down
def liftSystem(butnDown, butnRight, butnUp, butnLeft, whereLiftAtTrue):
    lift.set_velocity(100, PERCENT)

    #Lower level
    if butnDown and whereLiftAtTrue != 1:
        lift.spin(REVERSE)

    #Middle level
    elif butnRight and whereLiftAtTrue != 2:
        if whereLiftAtTrue >2: 
            lift.spin(REVERSE) 
        elif whereLiftAtTrue<2:
            lift.spin(FORWARD)
    
    #Upper level
    elif butnUp and whereLiftAtTrue != 3:
        lift.spin(FORWARD)


#front bumpers
showing1 = False
showing2 = False
def bumperSystem(bump1Pressing, bump2Pressing):
    global showing1
    global showing2
    #Shows if bumpers are being pressed on the robot.
    #Disappears if bumpers are not being pressed.

    #bumper1
    if bump1Pressing and not showing1:
        controller_1.screen.set_cursor(1,1)
        controller_2.screen.set_cursor(1,1)
        controller_1.screen.print("Bumper1: ")
        controller_1.screen.print(bumper1.pressing())
        controller_2.screen.print("Bumper1: ")
        controller_2.screen.print(bumper1.pressing())
        showing1 = True
    elif not bump1Pressing and showing1:
        controller_2.screen.clear_row(1)
        controller_1.screen.clear_row(1)
        showing1 = False

    #bumper2
    if bump2Pressing and not showing2:
        controller_1.screen.set_cursor(2,1)
        controller_2.screen.set_cursor(2,1)
        controller_1.screen.print("Bumper2: ")
        controller_1.screen.print(bumper2.pressing())
        controller_2.screen.print("Bumper2: ")
        controller_2.screen.print(bumper2.pressing())
        showing2 = True
    elif not bump2Pressing and showing2:
        controller_2.screen.clear_row(2)
        controller_1.screen.clear_row(2)
        showing2 = False



# Second conveyor belt system
def conveyor2System(butnA, butnR1):
    if butnA:
        conveyor2.set_velocity(100, PERCENT)
        if butnR1:
            direction = REVERSE
        else:
            direction = FORWARD
        conveyor2.spin(direction)
    else:
        conveyor2.stop()


# Lift system (Manual)
def liftManual(butnL1, butnL2, butnDown, butnRight, butnUp):
    if butnL1:
        lift.set_velocity(100, PERCENT)
        lift.spin(REVERSE)
    elif butnL2 and whereLiftAt != 3:
        lift.set_velocity(100, PERCENT)
        lift.spin(FORWARD)
    elif butnDown ==False and butnRight == False and butnUp == False:
        lift.stop()


#Printing to controller screens. useful for debugging
def controllerPrint(string, cursor, controller1, controller2):
    string = str(string)
    if controller1:
        controller_1.screen.set_cursor(*cursor)
        controller_1.screen.print(string)
    if controller2:
        controller_2.screen.set_cursor(*cursor)
        controller_2.screen.print(string)

while True:
    main()