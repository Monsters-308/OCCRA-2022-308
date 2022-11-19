from PIL import Image

"""
This program takes an image and prints out a tuple containing all of the image data, which can be copied and pasted into the vex program. This program will resize the image
to have a height of 240 and will reduce the color palette to up to 256 colors (8 by default).
You must specify which image you're using, how many colors it will have, and how compressed it is (if at all) by modifying the variables im, colorAmount, and compressRatio respectively.
"""


#converts a tuple (r, g, b) into hexadecimal "#rrggbb"
#used for creating the palette
def convertHex(color):
    if color[0] < 16:
        r = "0" + str(hex(color[0]))[2:]
    else:
        r = str(hex(color[0]))[2:]

    if color[1] < 16:
        g = "0" + str(hex(color[1]))[2:]
    else:
        g = str(hex(color[1]))[2:]

    if color[2] < 16:
        b = "0" + str(hex(color[2]))[2:]
    else:
        b = str(hex(color[2]))[2:]

    return "#" + r + g + b






#IMPORTANT: the three variables below here are the ones that you edit.

im = Image.open('image.png') #set this to the name of the photo you're using.

colorAmount = 8 #set this to the amount of colors the image will have (maximun: 256). Note: adding more colors will create more data.

#compressRatio can be used to compress the image horizontally and/or vertically to save space.
#examples: (1, 1) = no compression, (2, 3) = vertical compression of 2, horizontal compression of 3
compressRatio = (1, 3) #(vertical, horizontal)





im = im.resize((round(im.size[0]/(im.size[1]/240)), 240))
im = im.convert('P', palette=Image.ADAPTIVE, colors=colorAmount)
im = im.convert("RGBA", palette=Image.ADAPTIVE, colors=colorAmount)


palette = []

for x in range(0, im.size[0]):
    for y in range(0, im.size[1]):
        if convertHex(im.getpixel((x,y))) not in palette:
            palette.append(convertHex(im.getpixel((x,y))))


imageData = []

for x in range(0, im.size[0], compressRatio[1]):
    listRow = []
    #each row will contain a list of tuples that have the color of the pixel, followed by how long that color goes on for
    #colorLength = (color, distance)
    colorLength = [palette.index(convertHex(im.getpixel((x,0)))), 1]
    
    for y in range(1, im.size[1], compressRatio[0]):
        colorY = palette.index(convertHex(im.getpixel((x,y))))

        if colorY == colorLength[0]:
            colorLength[1] += 1
        else:
            listRow.append(tuple(colorLength))
            colorLength = [colorY, 1]
    
    listRow.append(tuple(colorLength))
    
    imageData.append(tuple(listRow))





#code for printing the image data to the command line
totalString = "("
stringRow = ""

for column in imageData:
    stringRow += str(column).replace(" ", "") + ','

    if len(stringRow) > 160:
        stringRow += "\n"
        totalString += stringRow
        stringRow = ""


totalString += stringRow
totalString += ")"


print(totalString)
print("size: " + str(totalString.count("\n")) + " lines.")
print("compressRatio = " + str(compressRatio))
print("palette = " + str(palette))


