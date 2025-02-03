import _thread
import machine
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import dht
from time import sleep

# LCD Configuration
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C for LCD
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)

# Check if LCD is detected
i2c_scan = i2c.scan()
if I2C_ADDR not in i2c_scan:
    print("LCD not found!")
    while True:
        pass  # Halt if LCD is missing

lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# DHT11 sensor with pull-up resistor enabled
sensor = dht.DHT11(Pin(16, Pin.IN, Pin.PULL_UP))

# Shared variables (use locks for thread safety)
temperature = 0.0
humidity = 0.0
lock = _thread.allocate_lock()

# Function for Core 0: Read sensor data
def read_sensor():
    global temperature, humidity
    while True:
        try:
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            temp_f = temp * (9 / 5) + 32.0  # Convert to Fahrenheit

            with lock:  # Protect shared variables
                temperature = temp_f
                humidity = hum
            
        except OSError:
            print("Sensor Error!")
        
        sleep(2)  # Delay before next reading

# Function for Core 1: Update LCD Display
def update_lcd():
    while True:
        with lock:  # Ensure thread-safe access
            temp_f = temperature
            hum = humidity

        # Update LCD
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(f'Temp: {temp_f:.1f} F')
        lcd.move_to(0, 1)
        lcd.putstr(f'Humidity: {hum:.1f}%')

        sleep(2)  # Refresh display every 2 seconds

# Start Core 1 with the LCD update function
_thread.start_new_thread(update_lcd, ())

# Run the sensor reading function on Core 0 (Main thread)
read_sensor()
