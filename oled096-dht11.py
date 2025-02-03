from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from machine import Pin
from time import sleep
import dht

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
sensor = dht.DHT11(Pin(2))

while True:
  try:
    sleep(2)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    dew = round(temp_f - ((100-hum)/5.0), 2)
    #print('Temperature: %3.1f C' %temp)
    #print('Temperature: %3.1f F' %temp_f)
    #print('Humidity: %3.1f %%' %hum)
    oled.text('Temp: %3.1f F' %temp_f, 0, 0)
    oled.text('Humidity: %3.1f %%' %hum, 0, 16)
    oled.text('DewPoint: %3.1f F' %dew, 0, 32)
    oled.show()
  except OSError as e:
    print('Failed to read sensor.')

#oled.text("Hello World", 0, 25)
#oled.show()