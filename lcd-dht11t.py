import utime
import machine 
from machine import I2C,ADC,Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import dht
from time import sleep

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 15

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

sensor = dht.DHT11(Pin(16))

try:
    while True:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        # Clear the LCD
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Temp: %3.1f F' %temp_f)
        lcd.move_to(0, 1)
        lcd.putstr('Humidity: %3.1f%%' %hum)
        sleep(2)
except OSError as e:
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr('Failed to read sensor.')