import time
import board
import digitalio
import neopixel

# Power on the NeoPixel (required for XIAO RP2040)
power = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
power.direction = digitalio.Direction.OUTPUT
power.value = True

# Initialize the NeoPixel on Pin 12
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

while True:
    pixels.fill((255, 0, 0))    # Red
    time.sleep(0.5)
    pixels.fill((0, 255, 0))    # Green
    time.sleep(0.5)
    pixels.fill((0, 0, 255))    # Blue
    time.sleep(0.5)
