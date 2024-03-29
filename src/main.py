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

lift = Motor29(brain.three_wire_port.f, False)# DOWN=HOME(LEVEL2), RIGHT=LEVEL3, UP=LEVEL4, LEFT=RESET 

controller_1 = Controller(PRIMARY)
controller_2 = Controller(PARTNER)

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
#    Created:      Thurs Nov 10 2022                                         */
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

    #set speed makes it so the driver can control driving speeds, up is more, down is less
    speedSet = 1.5
    speedSet2 = .8
    if controller_1.buttonDown.pressing():
        speedSet = 2
        speedSet2 = .6
    if controller_1.buttonUp.pressing():
        speedSet = 1.4
        speedSet2 = .8
    #get controller axis positions
    Axis3=controller_1.axis3.position()/speedSet #makes robot slower by dividing higher vaules
    Axis1=controller_1.axis1.position()*(speedSet2) #makes robot slower by multiplying lower vaules
    
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

    #this allows the robot to steer by adding Axis1 to one side and subtracting it from the other side
    if Axis1 > 0:
        leftSpeed = leftSpeed + Axis1 
        rightSpeed = rightSpeed - Axis1
    elif Axis1 < 0:
        leftSpeed = leftSpeed + Axis1
        rightSpeed = rightSpeed - Axis1 


    #adjusts for motor biases to make robot go straight
    if leftSpeed > 0:
        leftSpeed = leftSpeed + 2.8
    if rightSpeed < 0:
        rightSpeed = rightSpeed -9.3 # 10/10/22 is this "minus 9.3" or "negative 9.3" -Noah

    #set drive motor speeds
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
    conveyor1.set_velocity(100, PERCENT)
    conveyorIntakeWheels.set_velocity(100, PERCENT)
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

#This function converts a pixel color from "#rrggbb" to (r, g, b)
#This is only used because PIL doesn't take colors in the format "#rrggbb"
def hexToTuple(hexString):
    return (int(hexString[1:3], 16), int(hexString[3:5], 16), int(hexString[5:], 16))


imageData = (((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,119),(1,24),(0,97)),((0,114),(1,33),(0,93)),
((0,111),(1,11),(2,18),(1,10),(0,90)),((0,107),(1,9),(2,30),(1,8),(0,86)),((0,105),(1,8),(2,36),(1,8),(0,83)),((0,102),(1,7),(2,43),(1,8),(0,80)),((0,100),(1,6),(2,49),(1,6),(0,79)),
((0,98),(1,6),(2,54),(1,5),(0,77)),((0,96),(1,6),(2,57),(1,6),(0,75)),((0,95),(1,5),(2,61),(1,6),(0,73)),((0,93),(1,5),(2,65),(1,6),(0,71)),((0,91),(1,5),(2,69),(1,6),(0,69)),
((0,90),(1,5),(2,72),(1,5),(0,68)),((0,89),(1,5),(2,74),(1,5),(0,67)),((0,87),(1,5),(2,78),(1,5),(0,65)),((0,86),(1,5),(2,80),(1,5),(0,64)),((0,85),(1,4),(2,83),(1,5),(0,63)),
((0,55),(1,2),(0,27),(1,4),(2,86),(1,4),(0,62)),((0,41),(1,31),(0,10),(1,5),(2,88),(1,4),(0,61)),((0,36),(1,12),(3,12),(1,26),(2,90),(1,4),(0,60)),((0,35),(1,8),(3,10),(1,16),(3,6),(1,10),(2,92),(1,4),(0,59)),
((0,34),(1,5),(3,16),(1,18),(3,3),(1,8),(2,94),(1,5),(0,57)),((0,32),(1,5),(3,26),(1,1),(3,3),(1,18),(2,94),(1,5),(0,56)),((0,32),(1,4),(3,34),(1,15),(2,94),(1,5),(0,56)),
((0,31),(1,4),(3,36),(1,3),(3,1),(1,10),(2,96),(1,5),(0,54)),((0,31),(1,3),(3,42),(1,11),(2,9),(1,1),(2,5),(1,5),(2,54),(1,10),(2,10),(1,5),(0,54)),((0,31),(1,3),(3,43),(1,31),(2,51),(1,16),(2,8),(1,4),(0,53)),
((0,31),(1,2),(3,35),(1,2),(3,1),(1,6),(3,4),(1,27),(2,49),(1,19),(2,8),(1,3),(0,53)),((0,31),(1,2),(3,15),(1,2),(3,21),(1,21),(0,6),(1,10),(2,47),(1,5),(0,8),(1,8),(2,8),(1,4),(0,52)),
((0,31),(1,1),(3,17),(1,4),(3,14),(1,1),(3,3),(1,2),(3,3),(1,15),(0,12),(1,5),(2,18),(1,8),(2,21),(1,4),(0,11),(1,6),(2,9),(1,3),(0,52)),((0,31),(1,1),(3,18),(1,3),(3,11),(1,1),(3,12),(1,14),(0,12),(1,5),(2,16),(1,14),(2,18),(1,2),(0,12),(1,6),(2,10),(1,3),(0,51)),
((0,31),(1,1),(3,16),(1,5),(3,12),(1,1),(3,13),(1,13),(0,11),(1,5),(2,13),(1,18),(2,17),(1,2),(0,13),(1,5),(2,10),(1,4),(0,50)),((0,31),(1,2),(3,13),(1,6),(3,10),(1,6),(2,5),(1,1),(3,6),(1,12),(0,11),(1,5),(2,12),(1,3),(0,6),(1,10),(2,17),(1,1),(0,14),(1,5),(2,11),(1,4),(0,49)),
((0,31),(1,3),(3,4),(1,4),(3,15),(1,8),(2,10),(3,7),(1,12),(0,9),(1,5),(2,10),(1,2),(0,13),(1,6),(2,16),(1,2),(0,14),(1,5),(2,11),(1,5),(0,48)),((0,31),(1,3),(3,4),(1,4),(3,15),(1,7),(2,12),(3,8),(1,10),(0,9),(1,5),(2,8),(1,3),(0,14),(1,5),(2,17),(1,2),(0,14),(1,5),(2,12),(1,4),(0,48)),
((0,31),(1,4),(3,22),(1,6),(2,14),(3,8),(1,10),(0,8),(1,5),(2,6),(1,3),(0,16),(1,5),(2,17),(1,1),(0,14),(1,6),(2,12),(1,5),(0,47)),((0,33),(1,5),(3,19),(1,6),(2,16),(3,7),(1,10),(0,7),(1,5),(2,3),(1,4),(0,17),(1,6),(2,17),(1,1),(0,14),(1,5),(2,14),(1,4),(0,47)),
((0,36),(1,4),(3,16),(1,4),(2,21),(3,6),(1,9),(0,6),(1,10),(0,21),(1,6),(2,15),(1,2),(0,14),(1,5),(2,14),(1,5),(0,46)),((0,39),(1,3),(3,5),(1,3),(3,6),(1,5),(2,21),(1,1),(3,5),(1,8),(0,6),(1,8),(0,23),(1,6),(2,14),(1,2),(0,15),(1,5),(2,15),(1,4),(0,46)),
((0,41),(1,2),(3,5),(1,4),(3,5),(1,7),(2,19),(1,1),(3,5),(1,7),(0,7),(1,4),(0,26),(1,9),(2,5),(1,7),(0,15),(1,6),(2,16),(1,4),(0,45)),((0,43),(1,2),(3,5),(1,6),(3,4),(1,10),(2,13),(3,8),(1,4),(0,39),(1,19),(0,16),(1,6),(2,16),(1,4),(0,45)),
((0,46),(1,3),(3,8),(1,2),(3,6),(1,20),(3,5),(1,4),(0,41),(1,14),(0,20),(1,5),(2,18),(1,4),(0,44)),((0,49),(1,1),(0,2),(1,8),(3,6),(1,21),(3,1),(1,5),(0,76),(1,5),(2,18),(1,5),(0,43)),
((0,54),(1,39),(0,75),(1,5),(2,20),(1,4),(0,43)),((0,57),(1,33),(0,77),(1,5),(2,21),(1,4),(0,43)),((0,63),(1,24),(0,29),(1,4),(0,46),(1,4),(2,23),(1,4),(0,43)),((0,54),(1,2),(0,2),(1,20),(2,5),(1,4),(0,27),(1,6),(0,45),(1,3),(2,26),(1,4),(0,42)),
((0,33),(1,45),(2,5),(1,3),(0,27),(1,3),(2,2),(1,2),(0,43),(1,3),(2,28),(1,4),(0,42)),((0,30),(1,4),(3,12),(1,10),(3,1),(1,3),(3,5),(1,12),(2,6),(1,3),(0,24),(1,4),(2,5),(1,2),(0,38),(1,5),(2,30),(1,4),(0,42)),
((0,27),(1,3),(3,15),(1,33),(2,5),(1,4),(0,21),(1,4),(2,7),(1,4),(0,33),(1,5),(2,33),(1,5),(0,41)),((0,25),(1,3),(3,24),(1,27),(2,4),(1,5),(0,15),(1,6),(2,12),(1,4),(0,29),(1,3),(2,38),(1,4),(0,41)),
((0,23),(1,3),(3,28),(1,2),(3,8),(1,16),(2,4),(1,24),(2,15),(1,31),(2,41),(1,4),(0,41)),((0,22),(1,3),(3,25),(1,8),(3,7),(1,15),(2,7),(1,4),(2,8),(1,41),(2,55),(1,4),(0,41)),
((0,21),(1,3),(3,8),(1,3),(3,31),(1,16),(2,14),(1,64),(2,36),(1,3),(0,41)),((0,21),(1,3),(3,9),(1,5),(3,12),(1,5),(3,9),(1,8),(3,3),(1,10),(2,9),(1,76),(2,26),(1,4),(0,40)),
((0,20),(1,3),(3,11),(1,5),(3,26),(1,5),(3,6),(1,10),(2,6),(1,6),(0,27),(1,49),(2,22),(1,4),(0,40)),((0,19),(1,3),(3,12),(1,6),(3,20),(1,13),(3,4),(1,11),(2,2),(1,5),(0,63),(1,18),(2,20),(1,4),(0,40)),
((0,19),(1,3),(3,44),(1,3),(3,8),(1,16),(0,75),(1,8),(2,20),(1,4),(0,40)),((0,18),(1,4),(3,11),(1,5),(3,26),(1,1),(2,3),(3,1),(1,6),(3,8),(1,9),(0,78),(1,7),(2,19),(1,4),(0,40)),
((0,18),(1,3),(3,13),(1,6),(3,22),(2,9),(3,1),(1,20),(0,78),(1,7),(2,20),(1,3),(0,40)),((0,18),(1,2),(3,12),(1,8),(3,14),(1,2),(3,4),(2,13),(3,1),(1,1),(3,3),(1,9),(3,1),(1,5),(0,78),(1,6),(2,20),(1,4),(0,39)),
((0,18),(1,2),(3,13),(1,5),(3,16),(1,5),(3,1),(2,15),(1,1),(3,4),(1,14),(0,78),(1,5),(2,20),(1,4),(0,39)),((0,18),(1,3),(3,2),(1,2),(3,6),(1,7),(3,15),(1,3),(3,1),(1,1),(3,1),(2,21),(3,5),(1,10),(0,77),(1,5),(2,20),(1,4),(0,39)),
((0,18),(1,3),(3,2),(1,2),(3,8),(1,5),(3,21),(2,24),(3,9),(1,3),(0,47),(1,1),(0,29),(1,5),(2,20),(1,4),(0,39)),((0,18),(1,3),(3,2),(1,1),(3,9),(1,1),(3,8),(1,3),(3,7),(1,7),(2,25),(3,8),(1,3),(0,13),(1,47),(0,17),(1,6),(2,19),(1,4),(0,39)),
((0,18),(1,4),(3,11),(1,3),(3,7),(1,3),(3,8),(1,6),(2,24),(3,7),(1,3),(0,13),(1,6),(2,12),(1,8),(2,20),(1,2),(0,17),(1,6),(2,19),(1,4),(0,39)),((0,20),(1,3),(3,3),(1,3),(3,5),(1,4),(3,20),(1,2),(2,23),(1,1),(3,5),(1,4),(0,13),(1,8),(2,39),(1,3),(0,16),(1,6),(2,19),(1,4),(0,39)),
((0,21),(1,2),(3,4),(1,4),(3,5),(1,2),(3,15),(1,11),(2,15),(1,5),(3,1),(1,6),(0,16),(1,49),(0,16),(1,5),(2,20),(1,4),(0,39)),((0,22),(1,10),(3,24),(1,1),(3,2),(1,4),(3,2),(1,1),(2,5),(1,1),(3,1),(1,16),(0,18),(1,48),(0,17),(1,5),(2,20),(1,4),(0,39)),
((0,24),(1,9),(3,23),(1,6),(3,2),(1,24),(0,21),(1,46),(0,17),(1,5),(2,20),(1,4),(0,39)),((0,27),(1,11),(3,28),(1,21),(0,47),(1,8),(0,30),(1,5),(2,20),(1,4),(0,39)),
((0,33),(1,8),(3,33),(1,6),(2,5),(1,2),(0,85),(1,5),(2,20),(1,4),(0,39)),((0,38),(1,12),(3,18),(1,10),(2,7),(1,2),(0,85),(1,5),(2,20),(1,4),(0,39)),((0,43),(1,33),(2,9),(1,3),(0,83),(1,5),(2,21),(1,4),(0,39)),
((0,45),(1,31),(2,9),(1,3),(0,83),(1,5),(2,21),(1,4),(0,39)),((0,43),(1,37),(2,6),(1,2),(0,82),(1,4),(2,22),(1,5),(0,39)),((0,43),(1,39),(2,4),(1,3),(0,80),(1,2),(2,25),(1,5),(0,39)),
((0,41),(1,6),(3,3),(1,42),(0,72),(1,5),(2,19),(1,14),(0,38)),((0,40),(1,6),(3,2),(1,30),(3,1),(1,15),(0,67),(1,6),(2,18),(1,19),(0,36)),((0,37),(1,4),(3,2),(1,18),(3,11),(1,26),(0,10),(1,14),(0,5),(1,23),(2,32),(1,6),(2,5),(3,1),(1,13),(0,33)),
((0,35),(1,4),(3,3),(1,15),(3,13),(1,60),(2,51),(1,7),(2,6),(3,1),(1,14),(0,31)),((0,32),(1,5),(3,4),(1,9),(3,18),(1,4),(3,5),(1,15),(3,3),(1,38),(2,9),(1,18),(2,19),(1,9),(2,8),(3,1),(1,14),(0,29)),
((0,31),(1,5),(3,4),(1,3),(3,22),(1,5),(3,26),(1,39),(2,4),(1,33),(2,6),(1,10),(2,8),(3,2),(1,15),(0,27)),((0,31),(1,4),(3,3),(1,2),(3,24),(1,6),(3,2),(2,18),(3,5),(1,5),(0,25),(1,50),(2,2),(1,11),(2,9),(1,1),(3,1),(1,15),(0,26)),
((0,29),(1,5),(3,28),(1,6),(3,3),(2,20),(3,3),(1,5),(0,31),(1,8),(0,22),(1,20),(3,2),(1,6),(2,10),(1,1),(3,1),(1,16),(0,24)),((0,28),(1,5),(3,30),(1,4),(3,3),(2,21),(3,2),(1,5),(0,33),(1,4),(0,34),(1,10),(3,4),(1,4),(2,12),(1,1),(3,2),(1,15),(0,23)),
((0,27),(1,4),(3,33),(1,2),(3,4),(2,20),(3,3),(1,5),(0,34),(1,1),(0,37),(1,9),(3,4),(1,5),(2,12),(3,2),(1,17),(0,21)),((0,27),(1,1),(3,38),(1,4),(3,1),(2,17),(3,4),(1,4),(0,75),(1,9),(3,1),(1,7),(2,13),(3,3),(1,8),(3,1),(1,6),(0,21)),
((0,26),(1,2),(3,38),(1,5),(2,16),(3,3),(1,4),(0,77),(1,17),(2,13),(3,4),(1,7),(3,2),(1,6),(0,20)),((0,26),(1,3),(3,37),(1,4),(3,3),(2,12),(1,1),(3,2),(1,6),(0,77),(1,8),(3,1),(1,8),(2,14),(3,3),(1,8),(3,2),(1,5),(0,20)),
((0,26),(1,3),(3,37),(1,4),(3,4),(1,2),(3,1),(1,1),(3,1),(2,5),(3,2),(1,8),(0,77),(1,6),(3,3),(1,9),(2,13),(3,4),(1,7),(3,2),(1,5),(0,20)),((0,27),(1,1),(3,11),(1,6),(3,21),(1,2),(3,5),(1,20),(0,78),(1,6),(3,4),(1,8),(2,13),(1,1),(3,3),(1,14),(0,20)),
((0,26),(1,2),(3,13),(1,5),(3,24),(1,22),(0,16),(1,13),(0,49),(1,7),(3,4),(1,8),(2,14),(3,4),(1,13),(0,20)),((0,26),(1,2),(3,13),(1,5),(3,9),(1,6),(3,8),(1,14),(3,2),(1,6),(0,15),(1,5),(2,11),(1,1),(0,18),(1,16),(0,13),(1,7),(3,4),(1,3),(3,2),(1,3),(2,6),(3,4),(2,3),(1,1),(3,8),(1,9),(0,20)),
((0,26),(1,2),(3,12),(1,6),(3,27),(1,3),(3,8),(1,5),(0,16),(1,5),(2,12),(1,2),(0,17),(1,6),(2,9),(1,2),(0,12),(1,8),(3,7),(1,7),(3,7),(2,4),(3,9),(1,9),(0,19)),((0,27),(1,2),(3,14),(1,1),(3,39),(1,4),(0,18),(1,19),(0,17),(1,9),(2,1),(1,7),(0,12),(1,8),(3,9),(1,4),(3,2),(1,3),(3,3),(1,2),(3,15),(1,6),(0,18)),
((0,27),(1,2),(3,53),(1,5),(0,18),(1,19),(0,17),(1,17),(0,12),(1,8),(3,1),(1,2),(3,7),(1,9),(3,2),(1,3),(3,6),(1,2),(3,2),(1,1),(3,3),(1,6),(0,18)),((0,28),(1,2),(3,16),(1,4),(3,13),(1,1),(3,14),(1,8),(0,21),(1,9),(0,2),(1,5),(0,18),(1,16),(0,13),(1,12),(3,5),(1,5),(3,7),(1,4),(3,1),(1,6),(3,2),(1,1),(3,3),(1,7),(0,17)),
((0,28),(1,3),(3,22),(1,2),(3,6),(1,10),(3,4),(1,5),(2,2),(1,4),(0,84),(1,11),(3,6),(1,4),(3,8),(1,10),(3,5),(1,9),(0,17)),((0,29),(1,3),(3,4),(1,1),(3,15),(1,3),(3,11),(1,1),(3,7),(1,5),(2,4),(1,2),(0,86),(1,7),(3,21),(1,9),(3,6),(1,9),(0,17)),
((0,30),(1,4),(3,3),(1,3),(3,29),(1,7),(2,7),(1,2),(0,86),(1,8),(3,37),(1,7),(0,17)),((0,31),(1,5),(3,3),(1,2),(3,23),(1,11),(2,8),(1,2),(0,86),(1,9),(3,32),(1,1),(3,3),(1,7),(0,17)),
((0,33),(1,6),(3,18),(1,18),(2,8),(1,3),(0,84),(1,10),(3,21),(1,1),(3,14),(1,8),(0,16)),((0,36),(1,5),(3,14),(1,7),(0,10),(1,4),(2,8),(1,2),(0,84),(1,8),(3,22),(1,4),(3,11),(1,10),(0,15)),
((0,38),(1,11),(0,24),(1,3),(2,8),(1,3),(0,43),(1,2),(0,36),(1,5),(2,1),(1,4),(3,22),(1,3),(3,8),(1,15),(0,14)),((0,73),(1,4),(2,8),(1,3),(0,40),(1,6),(0,32),(1,5),(2,4),(1,3),(3,22),(1,1),(3,9),(1,15),(0,15)),
((0,74),(1,4),(2,8),(1,4),(0,35),(1,5),(2,2),(1,5),(0,7),(1,24),(2,7),(1,4),(3,1),(1,2),(3,16),(1,2),(3,14),(1,10),(0,16)),((0,74),(1,4),(2,11),(1,38),(2,8),(1,24),(2,1),(1,1),(2,14),(1,8),(3,15),(1,1),(3,15),(1,9),(0,17)),
((0,75),(1,4),(2,16),(1,11),(2,2),(1,3),(2,63),(1,8),(3,1),(1,1),(3,20),(1,3),(3,6),(1,9),(0,18)),((0,76),(1,4),(2,94),(1,5),(3,23),(1,6),(3,3),(1,11),(0,18)),((0,76),(1,5),(2,93),(1,9),(3,19),(1,5),(3,2),(1,12),(0,19)),
((0,77),(1,5),(2,91),(1,13),(3,13),(1,7),(3,3),(1,12),(0,19)),((0,78),(1,5),(2,90),(1,19),(3,6),(1,7),(3,7),(1,8),(0,20)),((0,79),(1,5),(2,89),(1,24),(3,15),(1,7),(0,21)),
((0,80),(1,5),(2,91),(1,24),(3,3),(1,5),(3,2),(1,8),(0,22)),((0,81),(1,5),(2,89),(1,32),(3,3),(1,7),(0,23)),((0,83),(1,4),(2,88),(1,40),(0,25)),((0,84),(1,4),(2,85),(1,5),(0,9),(1,24),(0,29)),
((0,85),(1,5),(2,82),(1,5),(0,15),(1,12),(0,36)),((0,86),(1,5),(2,79),(1,6),(0,64)),((0,87),(1,6),(2,76),(1,6),(0,65)),((0,89),(1,5),(2,74),(1,5),(0,67)),((0,90),(1,5),(2,72),(1,5),(0,68)),
((0,92),(1,5),(2,68),(1,5),(0,70)),((0,93),(1,5),(2,65),(1,6),(0,71)),((0,94),(1,7),(2,60),(1,6),(0,73)),((0,96),(1,6),(2,57),(1,6),(0,75)),((0,98),(1,7),(2,52),(1,6),(0,77)),
((0,100),(1,7),(2,47),(1,8),(0,78)),((0,102),(1,8),(2,42),(1,7),(0,81)),((0,106),(1,7),(2,35),(1,9),(0,83)),((0,108),(1,9),(2,28),(1,9),(0,86)),((0,111),(1,14),(2,12),(1,13),(0,90)),
((0,114),(1,33),(0,93)),((0,120),(1,19),(0,101)),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),((0,240),),
((0,240),),((0,240),),((0,240),),)

compressRatio = (1, 3) #set this to the image's compression ratio

palette = ['#d50602', '#000000', '#ffffff', '#08610b']#set this to the image's color palette



x = (480 - len(imageData)*compressRatio[1]) // 2 #this makes sure that images with a width smaller than 480 will be centered

for column in imageData: #for every column in the image
    y = 0

    for colorLength in column: #for every tuple of pixel data in the image
        color = palette[colorLength[0]]
    
        for i in range(0, colorLength[1]): #repeat for length of color
            for j in range(0, compressRatio[0]): #vertical compression
                for k in range(0, compressRatio[1]): #horizontal compression
                    brain.screen.set_pen_color(color)
                    brain.screen.draw_pixel(x+k,y+j)
            
            y += compressRatio[0] #adds change in y for every row of pixels placed
    x += compressRatio[1] #adds change in x for every column of pixels placed



while True:
    main()