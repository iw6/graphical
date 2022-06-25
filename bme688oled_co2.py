#!/usr/bin/env python

# Based on pimoroni.com bme680 software
# Luma oled software driver https://luma-oled.readthedocs.io/en/latest/python-usage.html
# In terminal: curl https://get.pimoroni.com/bme680 | bash
# sudo -H pip3 install --upgrade luma.oled
# sudo apt-get update
# sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y
# sudo -H pip3 install luma.oled
# sudo apt-get install python3-pil
# sudo usermod -a -G spi,gpio,i2c pi

# To calulate altitude in meters: https://keisan.casio.com/exec/system/1224585971
#                   1/5.257
# h = (p0/P)        -1 x Temp +273.15
#      ________________________________________
#                            0.0065
# or if your altitude is known: https://keisan.casio.com/keisan/image/Convertpressure.pdf
# To calulate pressure at sea level P0: https://keisan.casio.com/exec/system/1224585971
# P = current barometric pressure in hPa, T = current temperature oC and h current altitude in metres
#                                                  5.257
# Po =              (1-          (0.0065*h))
#        (P*  (  _____________________________
#                       ((T+273.15)+(0.0065 *h))

import bme680
import serial
import math
import sys
import subprocess
from luma.core.interface.serial import i2c
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from time import sleep
ser = serial.Serial('/dev/ttyS0',baudrate = 9600, timeout = 0.5)

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)    
serial = i2c(port=1, address=0x3C)
# substitute ssd1306, ssd1331(...) or sh1106(...) below if using that device
device = sh1106(serial)
# Read BME688
sensor.get_sensor_data()          
t = sensor.data.temperature
p = sensor.data.pressure

# Enter current altitude (m)
h=140

p0= round(p*(pow((1-(0.0065 *h)/((t+273.15)+(0.0065*h))),-5.275)),1) 
print("Pressure at sea level, po=",p0,"hPa")
print("p0=",p0,"hPa")

def show(temp):           
    draw.text((15, 10), (" CO2"), fill="white")
    draw.text((60, 10), co2, fill="white")  
    draw.text((100, 10), ("ppm"), fill="white") 
      
    draw.text((15, 20), (" Temp"), fill="white")
    draw.text((60, 20), temp_str, fill="white")
    draw.text((100, 20), ("\u00B0C"), fill="white")
        
    draw.text((15, 30), (" Hum"), fill="white")
    draw.text((60, 30), hum_str, fill="white")
    draw.text((100, 30), ("%"), fill="white")
        
    draw.text((15, 40), (" Press"), fill="white")
    draw.text((60, 40), p_str, fill="white")
    draw.text((100, 40), ("hPa"), fill="white")
    
    draw.text((15, 50), (" Alt"), fill="white")
    draw.text((60, 50), alt_str, fill="white")
    draw.text((100, 50), ("feet"), fill="white")

while True:
    try:
        with canvas(device) as draw:
        #draw.rectangle(device.bounding_box, outline="white", fill="black")        
# Read CO2      
            ser.flushInput()    
            ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25')   
            resp = ser.read(7)
            high = (resp[3])
            low = (resp[4])
            co2 = str(((high*256) + low)-6500)          
# Read BME688
            sensor.get_sensor_data()
            temp = sensor.data.temperature
            temp_str = str(round((temp),1))
            hum_str = str(round(sensor.data.humidity,1))
            p_str = str(math.trunc(sensor.data.pressure))
        
# Or input pressure at sea level hPa
            #p0 = 1017   
            alt = ((((pow((p0/p),(1/5.275))-1)*(temp + 273.15))/0.0065)*3.2808)#in feet
            alt_str = str(math.trunc(alt))       
            show(temp)
            print ("Altitude", alt_str, "(ft)")   
            sleep(2)
    except KeyboardInterrupt:
        sys.exit()
            