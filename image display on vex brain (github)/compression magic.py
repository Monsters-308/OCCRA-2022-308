from PIL import Image

"""
# Make a new image
im = Image.new('RGBA',(16,16))

# Get a pixel from the image
print(im.getpixel((0,0)))

# Modify a pixel
pixel = (0,0)
color = (255,0,0)
im.putpixel(pixel,color)

# Save an image (can be used to save an image to a different file format)
im.save('testimage2.jpg') # Note: an image can be saved multiple times to create
multiple copies

# Open an image
im = Image.open('red.png')

# Show an image
im.show()

# Resize an image
im.thumbnail((64,64)) # resizes to 64x64

"""


#this file takes an image and prints out a tuple containing all of the image data.
#use this on an image that has been resized and recolored using https://onlinejpgtools.com/reduce-jpg-colors


#convert a tuple (r, g, b) into hexadecimal "#rrggbb"
def convertHex(color):
    if color[0] < 10:
        r = "0" + str(hex(color[0]))[2:]
    else:
        r = str(hex(color[0]))[2:]

    if color[1] < 10:
        g = "0" + str(hex(color[1]))[2:]
    else:
        g = str(hex(color[1]))[2:]

    if color[2] < 10:
        b = "0" + str(hex(color[2]))[2:]
    else:
        b = str(hex(color[2]))[2:]

    return "#" + r + g + b

compressRatio = (1, 3)
im = Image.open('faceoutput.png')



imageData = []

for x in range(0, im.size[0], compressRatio[1]):
    listRow = []
    #each row will contain a list of tuples that have the color of the pixel, followed by how long that color goes on for
    #colorLength = (color, distance)
    colorLength = [convertHex(im.getpixel((x,0))), 1]
    
    for y in range(1, im.size[1], compressRatio[0]):
        colorY = convertHex(im.getpixel((x,y)))

        if colorY == colorLength[0]:
            colorLength[1] += 1
        else:
            listRow.append(tuple(colorLength))
            colorLength = [colorY, 1]
    
    listRow.append(tuple(colorLength))
    
    imageData.append(tuple(listRow))


#Debug code
#print(tuple(imageData))
#print(len(imageData))
#print(len(imageData[50]))

"""
for column in imageData:
    print(str(column) + ",")
"""



#code for printing to the command line
totalString = "("
stringRow = ""

for column in imageData:
    stringRow += str(column).replace(" ", "" ) + ','

    if len(stringRow) > 130:
        stringRow += "\n"
        totalString += stringRow
        stringRow = ""


totalString += stringRow
totalString += ")"

print(totalString)
print("compressRatio = " + str(compressRatio))



