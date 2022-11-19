This folder contains the modules we used to put our team logo on our Brain screen. Even though there are functions listed in the API for displaying bitmap images to the brain, these functions don't actually work, so we had to write our own module for displaying images.

How to use it:

1. Place the image you want to use in the same directory as "image compression.py"

2. Open "image compression.py" and change the parameter in "im = Image.open('image.png')" to the filename of the image. Additionally, you can also set "colorAmount" to the amount of colors the image will have (8 by default) and you can change "compressRatio" to control how large each pixel is (1x3 by default).

3. Run "image compression.py" and copy the data printed out in the command line.

4. Open vex code.v5python and set "imageData", "palette", and "compressRatio"  to the data printed out in the command line. When this file is downloaded on the brain and ran, it should display your image on the brain screen. If you don't have a brain on you, you can also paste the image data into "output (debug).py" to see what the image will look like.

