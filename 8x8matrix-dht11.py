from machine import Pin, SPI
from max7219 import Matrix8x8
from time import sleep
import dht

# Initialize SPI and MAX7219
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
cs = Pin(17, Pin.OUT)
sensor = dht.DHT11(Pin(2))

# Set up the display (1 module, 8x8 matrix)
display = Matrix8x8(spi, cs, 4)
display.brightness(5)  # Set default brightness (0 to 15)
display.fill(0)

# Function to scroll text
def scroll_text(message, delay=0.1, brightness=5):
    """Scrolls a message across the display with adjustable brightness."""
    display.brightness(brightness)  # Set brightness
    display.fill(0)  # Clear display
    message_length = len(message) * 8  # Each character is 8 pixels wide
    for x in range(8, -message_length - 1, -1):  # Scroll from right to left
        display.fill(0)
        display.text(message, x, 0, 1)  # Draw text at position (x, 0)
        display.show()  # Refresh display
        sleep(delay)  # Delay for smooth scrolling

while True:
    # Measure temperature
    sensor.measure()
    temp = sensor.temperature()
    temp_f = temp * (9 / 5) + 32.0 # convert to fahrenheit 

    # Scroll temperature message with appropriate brightness
    scroll_text("Temp:%3.1fF" % temp_f, delay=0.1)
    #sleep(2)
    
    # Clear the display after scrolling
    display.fill(0)
    display.show()

