from machine import Pin, I2C, PWM
from neopixel import NeoPixel
from time import sleep
import utime
import random

# Initialize Color Sensor Pins
S2 = Pin(5, Pin.OUT)
S3 = Pin(18, Pin.OUT)
OUT = Pin(19, Pin.IN)

# Initialize Neopixel (LED Strip) on Pin 4
NUM_PIXELS = 10
np = NeoPixel(Pin(2), NUM_PIXELS)

# Initialize Servo Motor
servo = PWM(Pin(4), freq=50)

# Initialize I2C for LCD
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# LCD Driver
class I2CLCD:
    def __init__(self, i2c, addr=0x27):
        self.i2c = i2c
        self.addr = addr
        self.init_lcd()

    def send_command(self, cmd):
        self.i2c.writeto(self.addr, bytes([cmd & 0xF0 | 0x0C]))
        self.i2c.writeto(self.addr, bytes([cmd & 0xF0 | 0x08]))
        self.i2c.writeto(self.addr, bytes([(cmd << 4) & 0xF0 | 0x0C]))
        self.i2c.writeto(self.addr, bytes([(cmd << 4) & 0xF0 | 0x08]))

    def send_char(self, char):
        self.i2c.writeto(self.addr, bytes([char & 0xF0 | 0x0D]))
        self.i2c.writeto(self.addr, bytes([char & 0xF0 | 0x09]))
        self.i2c.writeto(self.addr, bytes([(char << 4) & 0xF0 | 0x0D]))
        self.i2c.writeto(self.addr, bytes([(char << 4) & 0xF0 | 0x09]))

    def init_lcd(self):
        self.send_command(0x33)
        self.send_command(0x32)
        self.send_command(0x28)
        self.send_command(0x0C)
        self.send_command(0x06)
        self.send_command(0x01)
        sleep(0.1)

    def clear(self):
        self.send_command(0x01)
        sleep(0.1)

    def move_to(self, row, col):
        addr = 0x80 + (0x40 * row) + col
        self.send_command(addr)

    def print(self, text):
        for char in text:
            self.send_char(ord(char))

# Initialize LCD
lcd = I2CLCD(i2c)

# Color to fate mapping
color_fates = {
    "red": "A forgotten past.",
    "blue": "A secret will soon be revealed.",
    "green": "You will find luck in unexpected places.",
    "yellow": "You are not alone.",
    "purple": "You are destined for wisdom.",
    "white": "A new beginning is on the horizon.",
    "black": "A shadow from the past lingers."
}

# Function to read color sensor
def get_rgb():
    S2.value(0)
    S3.value(0)
    utime.sleep(0.1)
    red = OUT.value()

    S2.value(1)
    S3.value(1)
    utime.sleep(0.1)
    green = OUT.value()

    S2.value(0)
    S3.value(1)
    utime.sleep(0.1)
    blue = OUT.value()

    return red * 255, green * 255, blue * 255

# Function to determine color name
def get_color_name(r, g, b):
    if r > 200 and g < 100 and b < 100:
        return "red"
    elif r < 100 and g < 100 and b > 200:
        return "blue"
    elif r < 100 and g > 200 and b < 100:
        return "green"
    elif r > 200 and g > 200 and b < 100:
        return "yellow"
    elif r > 150 and b > 150:
        return "purple"
    elif r > 200 and g > 200 and b > 200:
        return "white"
    elif r < 50 and g < 50 and b < 50:
        return "black"
    else:
        return "unknown"

# Function to update Neopixel color
def update_neopixel(r, g, b):
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

# Function to control servo movement
def set_servo(angle):
    duty = int((angle / 180) * 102) + 26
    servo.duty(duty)

# Start experience
lcd.clear()
lcd.print("The Oracle is here")
sleep(2)
lcd.clear()
lcd.print("Offer something to")
lcd.move_to(1, 0)
lcd.print("know your fate.")
sleep(3)

update_neopixel(255, 255, 255)  # White light before opening

lcd.clear()
lcd.print("Opening the box...")
set_servo(90)
update_neopixel(0, 0, 255)  # Blue while open
sleep(10)

lcd.clear()
lcd.print("Closing the box...")
set_servo(0)
update_neopixel(128, 0, 128)  # Purple while processing
sleep(2)

# Detect color
r, g, b = get_rgb()
color_name = get_color_name(r, g, b)
fate = color_fates.get(color_name, "The future is unclear.")

lcd.clear()
lcd.print("Communicating with")
lcd.move_to(1, 0)
lcd.print("the cosmos...")
sleep(3)

lcd.clear()
lcd.print("Determining your")
lcd.move_to(1, 0)
lcd.print("fate...")
sleep(3)

lcd.clear()
lcd.print(fate)
sleep(5)

update_neopixel(255, 0, 0)  # Red after fate is revealed
sleep(5)

lcd.clear()
lcd.print("Goodbye.")
sleep(3)

update_neopixel(255, 255, 255)

