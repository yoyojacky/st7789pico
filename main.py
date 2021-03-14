"""
240x240 ST7789 SPI LCD
using MicroPython library:
https://github.com/russhughes/st7789py_mpy
"""

import uos
import machine
import st7789py as st7789
from fonts import vga2_8x8 as font1
from fonts import vga1_16x32 as font2
import random
import time
import utime

#SPI(0) default pins
sck  = 2
mosi = 3
rst  = 0 
dc   = 1

width = 240
height = 240

CENTER_Y = int(width/2)
CENTER_X = int(height/2)

print(uos.uname())
spi0 = machine.SPI(0, baudrate=40000000, polarity=1, phase=0, sck=machine.Pin(sck), mosi=machine.Pin(mosi))
print(spi0)
adc = machine.ADC(4)

display = st7789.ST7789(spi0, width, width, reset=machine.Pin(rst, machine.Pin.OUT),dc=machine.Pin(dc, machine.Pin.OUT),xstart=0, ystart=0, rotation=0)

display.fill(st7789.color565(0, 255, 120))
time.sleep(2)
display.fill(st7789.BLACK)
display.text(font2, "Hello!", 10, 10)
time.sleep(.2)
display.text(font2, "RPi Pico", 10, 40)
time.sleep(.2)
display.text(font2, "Piday eetree ", 10, 70)
time.sleep(.2)
display.text(font1, "ST7789 SPI 240*240 IPS", 10, 100)
time.sleep(.2)
display.text(font1, "eetree.cn", 10, 110)
time.sleep(.2)
display.text(font1, "Piday, let's have fun!", 10, 120)
time.sleep(.2)
"""
for i in range(5000):
    display.pixel(random.randint(0, width),
          random.randint(0, height),
          st7789.color565(random.getrandbits(8),random.getrandbits(8),random.getrandbits(8)))
"""


# Helper function to draw a circle from a given position with a given radius
# This is an implementation of the midpoint circle algorithm,
# see https://en.wikipedia.org/wiki/Midpoint_circle_algorithm#C_example 
# for details
def draw_circle(xpos0, ypos0, rad, col=st7789.color565(255, 255, 255)):
    x = rad - 1
    y = 0
    dx = 1
    dy = 1
    err = dx - (rad << 1)
    while x >= y:
        display.pixel(xpos0 + x, ypos0 + y, col)
        display.pixel(xpos0 + y, ypos0 + x, col)
        display.pixel(xpos0 - y, ypos0 + x, col)
        display.pixel(xpos0 - x, ypos0 + y, col)
        display.pixel(xpos0 - x, ypos0 - y, col)
        display.pixel(xpos0 - y, ypos0 - x, col)
        display.pixel(xpos0 + y, ypos0 - x, col)
        display.pixel(xpos0 + x, ypos0 - y, col)
        if err <= 0:
            y += 1
            err += dy
            dy += 2
        if err > 0:
            x -= 1
            dx += 2
            err += dx - (rad << 1)
    
# draw_circle(CENTER_X, CENTER_Y, 100)
for i in range(20,100,20):
    draw_circle(i,160,15)

display.text(font1, "Audi", 20, 180)
for i in range(5):
    display.text(font2, "Last: "+str(i)+" s", 20, 200)
    time.sleep(1)

factor = 3.3 / (65535)
try:
    while True:
        reading = adc.read_u16() * factor
        temperature = 27 - (reading - 0.706)/0.001721
        utime.sleep(2)
        display.text(font2,"CPU_Temp:"+str(temperature), 20,10)
except KeyboardInterrupt:
    display.fill(st7789.color565(255,0,0))
    display.text(font2, "Good Bye!", 20, 110)

"""
for c in range(99):
    draw_circle(CENTER_X, CENTER_Y, c, st7789.color565(255, 0, 0))
    
for c in range(98):
    draw_circle(CENTER_X, CENTER_Y, c, st7789.color565(0, 255, 0))
    
for c in range(97):
    draw_circle(CENTER_X, CENTER_Y, c, st7789.color565(0, 0, 255))
"""
    
print("- bye-")
