from machine import Pin, SoftI2C
import ssd1306
import ds1302
import dht
import time

# RTC on GPIO 0,1,2
ds = ds1302.DS1302(Pin(0),Pin(1),Pin(2)) #(clk, dio, cs)
sensor = dht.DHT11(Pin(3))

# OLED GPIO 5,6
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        temp_f = temp * (9 / 5) + 32.0  # Convert to Fahrenheit
        oled.fill(0)
        oled.text("Date: {}.{}.{}".format(ds.month(), ds.day(), ds.year()), 0, 0)
        oled.text("Time: {}:{}:{}".format(ds.hour(), ds.minute(), ds.second()), 0, 16)
        oled.text("Temp: {:.1f} F".format(temp_f), 0, 32)  # Display temp_f
        oled.text("Humidity: {:.1f} %".format(humidity), 0, 48)  # Display humidity
        oled.show()
    except OSError as e:
        print('Failed to read sensor.')
    
    time.sleep(1)  # Wait 1 second before the next reading