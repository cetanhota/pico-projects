from machine import Pin, SoftI2C
from time import sleep
import BME280
import ssd1306

#BME I2C pins
i2c_bme = SoftI2C(scl=Pin(5), sda=Pin(4), freq=10000)

#OLED I2C pins
i2c_oled = SoftI2C(scl=Pin(1), sda=Pin(0))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c_oled)

while True:
    try:
        # Initialize BME280 sensor
        bme = BME280.BME280(i2c=i2c_bme)
        
        # Read sensor data
        tempC = bme.temperature
        hum = bme.humidity
        pres = bme.pressure
        
        # Convert temperature to fahrenheit
        tempF = (bme.read_temperature()/100) * (9/5) + 32
        tempF = str(round(tempF, 2)) + 'F'
        
        # Convert pressure to inHg
        pres_value = float(pres[:-3])  # Remove 'hPa' from the string and convert to float
        pres_inHg = round(pres_value * 0.02953, 2)
        pres_inHg = str(pres_inHg) + ' inHg'
        
        # Clear OLED display
        oled.fill(0)
        
        # Display sensor readings on OLED
        oled.text('Temp: ' + tempF, 0,0)
        oled.text('Humidity: ' + hum, 0,16)
        oled.text('Pressure: '+ pres_inHg, 0, 32)
        
        # Update OLED display
        oled.show()
        
    except Exception as e:
        # Handle any exceptions during sensor reading
        print('An error occurred:', e)

    sleep(5)
    oled.show()