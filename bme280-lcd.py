from machine import Pin, I2C
from time import sleep
from bmp085 import BMP180
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Initialize I2C for BME280 and LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

# Define LCD parameters
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Initialize BME280 sensor
bmp = BMP180(i2c=i2c)

def scroll_text(line, text, delay=0.3):
    """ Scrolls a long text across the LCD on the specified line """
    text = text + " " * I2C_NUM_COLS  # Add spaces to create a smooth scroll effect
    for i in range(len(text) - I2C_NUM_COLS + 1):
        lcd.move_to(0, line)
        lcd.putstr(text[i:i + I2C_NUM_COLS])  # Display a substring of 16 characters
        sleep(delay)

while True:
    try:
        # Read sensor data as strings
        tempC_str = bmp.temperature  # Example: "25.3C"
        pres_str = bmp.pressure      # Example: "1013.2hPa"

        # Convert to numerical values
        tempC = float(tempC_str[:-1])  # Remove 'C' and convert to float
        hum = float(hum_str[:-1])      # Remove '%' and convert to float
        pres_hPa = float(pres_str[:-3])  # Remove 'hPa' and convert to float

        # Convert temperature to Fahrenheit
        tempF = round((tempC * 9/5) + 32, 1)

        # Convert pressure to inHg
        pres_inHg = round(pres_hPa * 0.02953, 2)

        # Create scrolling text for temperature and humidity
        # scroll_text(0, f"Temp: {tempF:.1f}F  Hum: {hum:.1f}%")

        # Display pressure on the second line
        lcd.move_to(0,0)
        lcd.putstr(f'Temp: {tempF:.1f}F')
        lcd.move_to(0, 1)
        lcd.putstr(f'Pressure: {pres_inHg:.2f}')

        sleep(1)  # Wait before updating

    except OSError:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Sensor Error!')
        sleep(2)
