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
import random
import asyncio
import _thread

from machine import Pin, SPI


def loop_text():
    text = "MERRY CHRISTMAS"
    column = (len(text) * 8)
    spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
    display = max7219.Matrix8x8(spi, Pin(4, Pin.OUT), 4)
    display.brightness(1)

    while True:
        for x in range(32, -column, -1):
            display.fill(0)
            display.text(text, x, 0, 1)
            display.show()
            time.sleep(0.08)


async def loop_lights():
    led_count = 16
    available_colors = ["red", "white", "green"]
    ring = neopixel.NeoPixel(Pin(6, Pin.OUT), led_count)
    ring.fill((1, 1, 1))

    def update_rgb(color, brightness):
        rgb = None

        if color == "red":
            rgb = (brightness, 0, 0)
        elif color == "white":
            rgb = (brightness, brightness, brightness)
        elif color == "green":
            rgb = (0, brightness, 0)

        return rgb

    async def light_random():
        brightness = 25
        brightness_interval = 2
        dim_time = 0.15

        counter = brightness // brightness_interval
        color = random.choice(available_colors)
        led = random.randrange(0, led_count + 1)

        for i in range(counter):
            ring[led] = update_rgb(color, brightness)
            ring.write()
            brightness = brightness - brightness_interval

            await asyncio.sleep(dim_time)

    while True:
        await asyncio.create_task(light_random())
        await asyncio.sleep(1)


_thread.start_new_thread(loop_text, ())
asyncio.run(loop_lights())
