from machine import Pin, I2C
from time import sleep
from bmp085 import BMP180
from pico_i2c_lcd import I2cLcd

# Initialize I2C for BMP180 and LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

# Define LCD parameters
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Initialize BMP180 sensor
bmp = BMP180(i2c=i2c)

while True:
    try:
        # Read sensor data (already floats)
        tempC = bmp.temperature  # Temperature in Celsius
        pres_Pa = bmp.pressure  # Pressure in Pascals

        # Convert temperature to Fahrenheit
        tempF = round((tempC * 9/5) + 32, 1)

        # Direct conversion from Pascals to inHg
        pres_inHg = pres_Pa * 0.0002953
        inHg_calibrate = pres_inHg * 101.02

        # Debugging: Print raw pressure and converted value
        print(f"Raw Pressure: {pres_Pa} Pa")
        print(f"Temp: {tempF:.1f} F, Pressure: {inHg_calibrate:.2f} inHg")

        # Display temperature and pressure on LCD
        lcd.move_to(0, 0)
        lcd.putstr(f'Temp: {tempF:.1f} F  ')
        lcd.move_to(0, 1)
        lcd.putstr(f'Pressure: {inHg_calibrate:.2f}')

        sleep(1)  # Wait before updating

    except OSError:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Sensor Error!')
        sleep(2)