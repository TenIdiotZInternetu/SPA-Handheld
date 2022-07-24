import RPi.GPIO as GPIO
import keyboard
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Nastavenie režimu adresovania GPIO pinov
# BCM = relatívne číslo pinu
# BOARD = fyzické číslo pinu
GPIO.setmode(GPIO.BCM)

# Nastavenie vstupných pinov
GPIO.setup((6, 13, 16, 19, 20, 21, 26), GPIO.IN)

time.sleep(20)

# Definícia GPIO pinov pre SPI
spi = busio.SPI(clock=board.D11, MISO=board.D9, MOSI=board.D10)
cs = digitalio.DigitalInOut(board.D8)
mcp = MCP.MCP3008(spi, cs)


# Nekonečná slučka
while 1:
    # Detekcia stlačenia tlačidiel
    if GPIO.input(6): keyboard.press('enter')
    if GPIO.input(13): keyboard.press('l')
    if GPIO.input(19): keyboard.press('space')
    if GPIO.input(16): keyboard.press('esc')
    if GPIO.input(26): keyboard.press('i')
    if GPIO.input(20): keyboard.press('z')
    if GPIO.input(21): keyboard.press('tab')

    # Detekcia pustenia tlačidiel
    if not GPIO.input(6): keyboard.release('enter')
    if not GPIO.input(13): keyboard.release('l')
    if not GPIO.input(19): keyboard.release('space')
    if not GPIO.input(16): keyboard.release('esc')
    if not GPIO.input(26): keyboard.release('i')
    if not GPIO.input(20): keyboard.release('z')
    if not GPIO.input(21): keyboard.release('tab')

    # Čítanie hodnôt z ADC
    xAxis = AnalogIn(mcp, MCP.P0)
    yAxis = AnalogIn(mcp, MCP.P1)

    # Priradenie stlačenej 
    # Value 65472 => úplné vychýlenie páčky hore/vľavo
    # Value 0 => Úplné vychýlenie páčky dole/vpravo
    if xAxis.value > 52000: keyboard.press("left")
    if xAxis.value < 12000: keyboard.press("right")
    if yAxis.value > 52000: keyboard.press("up")
    if yAxis.value < 12000: keyboard.press("down")

    if xAxis.value < 52000: keyboard.release("left")
    if xAxis.value > 12000: keyboard.release("right")
    if yAxis.value < 52000: keyboard.release("up")
    if yAxis.value > 12000: keyboard.release("down")

    time.sleep(0.008)