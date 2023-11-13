"""
max7219
VCC -> VBUS
GND -> GND
DIN -> GPO3
CS -> GPO5
CLK -> GPO2

ws2812
VCC -> VBUS
DIN -> GP06
GND -> GND
"""

import max7219
import time
import neopixel
import _thread

from machine import Pin, SPI

text = "SCROLLING TEXT"
column = (len(text) * 8)

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
display = max7219.Matrix8x8(spi, Pin(4, Pin.OUT), 4)
display.brightness(1)

ring = neopixel.NeoPixel(Pin(6, Pin.OUT), 16)


def set_ring_brightness(color1):
    r, g, b = color1
    r = int(r * 0.025)
    g = int(g * 0.01)
    b = int(b * 0.015)
    return r, g, b


def loop_lights():
    while True:
        # Red
        color = (255, 0, 0)
        color = set_ring_brightness(color)
        ring.fill(color)
        ring.write()
        time.sleep(1)

        # Green
        color = (0, 255, 0)
        color = set_ring_brightness(color)
        ring.fill(color)
        ring.write()
        time.sleep(1)

        # Blue
        color = (0, 0, 255)
        color = set_ring_brightness(color)
        ring.fill(color)
        ring.write()
        time.sleep(1)


def loop_text():
    while True:
        for x in range(32, -column, -1):
            display.fill(0)
            display.text(text, x, 0, 1)
            display.show()
            time.sleep(0.06)


_thread.start_new_thread(loop_lights, ())
loop_text()
