#region VEXcode Generated Robot Configuration
from vex import *

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)
#endregion VEXcode Generated Robot Configuration



#----------------------------------------------------------------------------*/
#                                                                            */
#    Module:       Vex code                                                  */
#    Author:       C:\\Users\\FRC                                            */
#    Created:      Tue Nov 18 2022                                           */
#    Description:  V5 project                                                */
#                                                                            */
#----------------------------------------------------------------------------*/


"""
This file contains the code that is used to print an image to the brain screen.
To test an image, set imageData, compressRatio, and palette to the values printed out by image compression.py.
"""


#This function converts a pixel color from \"#rrggbb\" to (r, g, b)
#This is only used because PIL doesn't take colors in the format \"#rrggbb\"
def hexToTuple(hexString):
    return (int(hexString[1:3], 16), int(hexString[3:5], 16), int(hexString[5:], 16))



imageData = () #set this to the image data

compressRatio = (1, 3) #set this to the image's compression ratio

palette = [] #set this to the image's color palette



def main():
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

main()