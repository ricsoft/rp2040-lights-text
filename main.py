"""
VCC -> VBUS
GND -> GND
DIN -> GPIO3
CS -> GPIO5
CLK -> GPIO2
"""

from machine import Pin, SPI
import max7219
import time

spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(4, Pin.OUT)

display = max7219.Matrix8x8(spi, ss, 4)
display.brightness(1)

text = "SCROLLING TEXT"
column = (len(text) * 8)

while True:
    for x in range(32, -column, -1):
        display.fill(0)
        display.text(text, x, 0, 1)
        display.show()
        time.sleep(0.06)
