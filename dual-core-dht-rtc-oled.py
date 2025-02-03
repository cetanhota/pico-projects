from machine import Pin, SoftI2C, I2C
import ssd1306
import ds1302
import dht
import time
import _thread

# RTC on GPIO 0,1,2
ds = ds1302.DS1302(Pin(0), Pin(1), Pin(2))  # (clk, dio, cs)

# DHT11 on GPIO 3                               
sensor = dht.DHT11(Pin(3))

# OLED GPIO 4,5
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Shared variables (global)
temp_f = 0.0
humidity = 0.0
hours, minutes, seconds = 0, 0, 0

# Lock for thread safety
lock = _thread.allocate_lock()

def read_sensor():
    """ Runs on Core 1: Reads sensor data and updates global variables """
    global temp_f, humidity, hours, minutes, seconds
    while True:
        try:
            sensor.measure()
            temp = sensor.temperature()
            humidity = sensor.humidity()
            temp_f = round(temp * (9 / 5) + 32.0, 1)  # Convert to Fahrenheit
            
            # Read RTC time
            hours = ds.hour()
            minutes = "{:02}".format(ds.minute())
            seconds = "{:02}".format(ds.second())

        except OSError:
            print("Sensor Error!")
        
        time.sleep(1)  # Read data every 1 seconds

def display_oled():
    """ Runs on Core 0: Updates the OLED display """
    while True:
        lock.acquire()
        try:
            oled.fill(0)
            oled.text("Date: {}.{}.{}".format(ds.month(), ds.day(), ds.year()), 0, 0)
            oled.text("Time: {}:{}:{}".format(hours, minutes, seconds), 0, 16)
            oled.text("Temp: {:.1f} F".format(temp_f), 0, 32)  # Display temp_f
            oled.text("Humidity: {:.1f} %".format(humidity), 0, 48)  # Display humidity
            oled.show()
        finally:
            lock.release()
        
        time.sleep(1)  # Refresh display every second

# Start sensor reading on Core 1
_thread.start_new_thread(read_sensor, ())

# Run OLED update on Core 0
display_oled()
