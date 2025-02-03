from machine import Pin
import ds1302

ds = ds1302.DS1302(Pin(0),Pin(1),Pin(2)) #(clk, dio, cs)

print( "Date={}/{}/{}" .format(ds.month(), ds.day(),ds.year()) )
print( "Time={}:{}:{}" .format(ds.hour(), ds.minute(),ds.second()) )