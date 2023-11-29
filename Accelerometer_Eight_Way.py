# The MIT License (MIT)
#
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Eight Way Tilt Indicator.
# Uses the accelerometer to detect tilt in eight directions.
#
# Version:  0.2.2
# Date:     01-Apr-2018
# Purpose;  Added sensitivity (sens) and multiplier (mult) parameters to
#             the tiltDirection() function so these can be changed on the
#             fly. They default to SENSITIVITY and MULTIPLIER respectively.
# Author:   Dale Weber <hybotics@hybotics.org>
#
# Version:  0.2.1
# Date:     26-Mar-2018
# Purpose;  Added SENSITIVITY parameter to allow tuning tilt sensitivity
# Author:   Dale Weber <hybotics@hybotics.org>
#
# Version:  0.2.0
# Date:     21-Mar-2018
# Purpose;  Corrected backwards orientation of board; added color
# Author:   Dale Weber <hybotics@hybotics.org>
#
# Version:  0.1.0
# Date:     15-Mar-2018
# Purpose:  Added the tiltDirection function to get tilt direction
# Author:   Dale Weber <hybotics@hybotics.org>
#
import time
import board
import busio
import neopixel
import adafruit_lis3dh

# Change this to alter the sensitivity of the tilt detection.
# Greater makes the detection less sensitive, and less makes it more
#   sensitive.
# Positive values ONLY, since this is handled in detection. This must be
#   greater than 0 (zero) and less than MULTIPLIER * (x, y, z).
SENSITIVITY = 300

# The multiplier for the x, y, and z accelerometer readings
MULTIPLIER = 1000

RED = 0x100000 # (0x10, 0, 0) also works
YELLOW=(0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.1)
pixels.show()

# Hardware I2C setup on CircuitPlayground Express:
i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

def tiltDirection(x, y, z, sens = SENSITIVITY, mult = MULTIPLIER):
  xm, ym, zm = int(x * mult), int(y * mult), int(z * mult)
  print('xm = {0}, ym = {1}, zm = {2}'.format(xm, ym, zm))

  if (mult < 0) or (mult < sens):
    print("Invalid multiplier value: {0}".format(mult))
    return -1
  if (sens < 0) or (sens > mult):
    print("Invalid sensitivity value: {0}".format(sens))
    return -2
  elif (xm > -sens) and (xm < sens) and (ym < sens) and (ym > -sens):
    # Level
    return 1
  elif (ym > sens) and (xm > sens):
    # Bacward and right
    return 2
  elif (ym > sens) and (xm < -sens):
    # Backward and left
    return 3
  elif (ym < -sens) and (xm > sens):
    # Forward and right
    return 4
  elif (ym < -sens) and (xm < -sens):
    # Forward and left
    return 5
  elif (xm > sens):
    # Left
    return 6
  elif (xm < -sens):
    # Right
    return 7
  elif (ym > sens):
    # Backward
    return 8
  elif (ym < -sens):
    # Forward
    return 9
  else:
    # Invalid
    return 0

def showTiltDirection(tilt):
  if (tilt == 1):
    print("Leveled Out")
    pixels[0] = BLUE
    pixels[4] = BLUE
    pixels[5] = BLUE
    pixels[9] = BLUE
    pixels[1] = BLUE
    pixels[3] = BLUE
    pixels[6] = BLUE
    pixels[8] = BLUE
    pixels.show()
  elif (tilt == 2):
    print("Tilting Backward and Left")
    pixels[3] = PURPLE
    pixels[4] = PURPLE
    pixels.show()
  elif (tilt == 3):
    print("Tilting Backward and Right")
    pixels[5] = PURPLE
    pixels[6] = PURPLE
    pixels.show()
  elif (tilt == 4):
    print("Tilting Forward and Left")
    pixels[0] = PURPLE
    pixels[1] = PURPLE
    pixels.show()
  elif (tilt == 5):
    print("Tilting Forward and Right")
    pixels[8] = PURPLE
    pixels[9] = PURPLE
    pixels.show()
  elif (tilt == 6):
    print("Tilting Left")
    pixels[1] = GREEN
    pixels[3] = GREEN
    pixels.show()
  elif (tilt == 7):
    print("Tilting Right")
    pixels[6] = GREEN
    pixels[8] = GREEN
    pixels.show()
  elif (tilt == 8):
    print("Tilting Backward")
    pixels[4] = GREEN
    pixels[5] = GREEN
    pixels.show()
  elif (tilt == 9):
    print("Tilting Forward")
    pixels[0] = GREEN
    pixels[9] = GREEN
    pixels.show()

  print("Result = {0}".format(tilt))

# Loop forever printing accelerometer values
while True:
  # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
  # z axis values.  Divide them by 9.806 to convert to Gs.
  x, y, z = lis3dh.acceleration
  print("x = {0:.10f}, y = {1:.10f}, z = {2:.10f}".format(x, y, z))

  xG, yG, zG = x / 9.806, y / 9.806, z / 9.806
  print("xG = {0:.10f}G, yG = {1:.10f}G, zG = {2:.10f}G".format(xG, yG, zG))

  tilt = tiltDirection(x, y, z)
  showTiltDirection(tilt)

  print()

  time.sleep(2)
  pixels.fill(BLACK)
  pixels.show()
