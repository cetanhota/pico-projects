# Import necessary modules
from machine import Pin
import ds1302

# Initialize DS1302 RTC with specified pins (clk, dio, cs)
ds = ds1302.DS1302(Pin(0),Pin(1),Pin(2))

# Set the date and time on the RTC
ds.year(2025)  # Set the year to 2085
ds.month(1)    # Set the month to January
ds.day(25)     # Set the day to 17th
ds.hour(18)    # Set the hour to midnight (00)
ds.minute(54)  # Set the minute to 17
ds.second(00)  # Set the second to 30

# Print the date and time
print( "Date={}/{}/{}" .format(ds.month(), ds.day(),ds.year()) )
print( "Time={}:{}:{}" .format(ds.hour(), ds.minute(),ds.second()) )