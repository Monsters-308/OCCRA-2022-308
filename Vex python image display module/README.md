# V5 Python Image Display

Vex's support for python is limited in many ways, especially when it comes to displaying images to the brain's screen. Because of this, we decided to create a module that teams can use to display their team's logo to the screen. This module uses multiple compression techniques to ensure that the data for these images is not too large and will be displayed quickly.

## How to Use It:

1. Open "image compression.py" and change the parameter in "im = Image.open('image.png')" to the path of the image you want to use. Additionally, you can also set "colorAmount" to the amount of colors the image will have (8 by default) and you can change "compressRatio" to control how large each pixel is (1x3 by default).

1. Run "image compression.py" and copy the data printed out in the command line.

1. Open vex code.py and set "imageData", "palette", and "compressRatio"  to the data printed out in the command line. When this file is downloaded on the brain and ran, it should display your image on the brain screen. This code can then be copied into your main program and used.  

If you don't have a vex brain on you, you can also paste the image data into "output (debug).py" to see what the image will look like.

