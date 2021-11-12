#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Heavily based on Pimoroni Inky pHAT 
# curl http://get.pimoroni.com/inky | bash
# curl https://get.pimoroni.com/bme680 | bash
# Must have network access to get time

# Based on Pimoroni Inky pHAT and BME680 examples
# See C. Webster, Make an indoor air-quality sensor, Computer Shopper, Issue 375, May 2019
# Must have network access to get time

# To autostart 
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# add to end of file:
# @sudo /usr/bin/python3 /home/pi/Pimoroni/inky/examples/inky_bme680.py &
# Running on a time clock? Activate lines 137,138 for RPi to shutdown after one reading.

import os.path
import time
import datetime as dt
import bme680
import sys
import csv
import pandas as pd
import subprocess

from time import strftime
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne
sensor = bme680.BME680()
    
print ('Connected to BME680')
print ('Date       Time,  Temp\u00B0C, RH %, Press hPa,  Res k\u2126 ')

# Set the Inky pHAT colour
if os.path.exists('/home/pi/Desktop/air.csv'):   
    filename =('/home/pi/Desktop/air.csv')
    df= pd.read_csv(filename, parse_dates = True)   
    y = (len(df.index)-1)
    t_old= (df.iat[y,1])
    h_old = (df.iat[y,2])
    p_old = (df.iat[y,3])
    
    fieldnames = ['Time', 'Temp', 'RH', 'Press']         
    with open (filename, 'a') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        
else:
    t_old = 0
    h_old = 0
    p_old = 0
    
    filename = '/home/pi/Desktop/air.csv'
    fieldnames = ['Time', 'Temp', 'RH', 'Press']
    with open (filename, 'w') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()

# Set sleep time (nap) in minutes
nap = 60
sec_nap = (nap * 60)

x = []
y = []
y1= []
y2= []

# Set the Inky pHAT colour
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
font1 = ImageFont.truetype(FredokaOne, 19)
font2 = ImageFont.truetype(FredokaOne, 14)

def write_temp(temp):          
    with open (filename, 'a') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)        
        info = {"Time": x_time,"Temp": temp, "RH":hum, "Press": press}                                          
        csv_writer.writerow(info)    
        x.append(x_time) 
        y.append(temp)
        y1.append(hum)
        y2.append(press)
                
def show(temp):    
    img = Image.new("P",(inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)        
    d_time = (dt.datetime.now().strftime('%H:%M'))   
# Display Headers
    draw.text((130,0), 'Last update', inky_display.BLACK, font2)
    draw.text((130,17), d_time, inky_display.BLACK, font2)
    draw.text((70,0), 'Pause ', inky_display.RED, font2)
    draw.text((60,17), "- {0:1}min".format(nap), inky_display.RED, font2)   
# Display Temp
    draw.text((1,30), "Temp", inky_display.BLACK, font1)
    if t_old == 0:
        draw.text((70,35), "{0:1}".format('--'), inky_display.RED, font2)       
    else:
        draw.text((70,35), "{0:1}".format(t_old), inky_display.RED, font2)
    draw.text((130,30), "{0:1} \u00B0C".format(temp), inky_display.BLACK, font1)
# Display Humidity
    draw.text((5,55), "Hum", inky_display.BLACK, font1)
    if h_old == 0:
        draw.text((70,65), "{0:1}".format('--'), inky_display.RED, font2)       
    else:               
        draw.text((70,60), "{0:1}".format(h_old), inky_display.RED, font2)
    draw.text((130,55), "{0:1} %".format (hum), inky_display.BLACK, font1)
    # Display Pressure
    draw.text((5,80), "Press", inky_display.BLACK, font1)   
    if p_old == 0:
        draw.text((60,86), "{0:1}".format('  --'), inky_display.RED, font2)
    else:
        draw.text((60,86), "{0:1}".format(p_old), inky_display.RED, font2)
    draw.text((110,80), "{0:1} hPa".format(press), inky_display.BLACK, font1)
    
    print('{0:1}, {1:1},   {2:1},   {3:0}     {4:0}'.format(x_time, temp, hum, press, res))    
    inky_display.set_image(img)
    inky_display.show()
        
try:
    while True:              
# Read BME680 data
        sensor.get_sensor_data()
        x_time = time.strftime('%d-%m-%Y %H:%M')
        temp = round((sensor.data.temperature),1)
        hum = round(sensor.data.humidity,1)   
        press = round(sensor.data.pressure,1)
        res = round((sensor.data.gas_resistance/1000),1)
        write_temp(temp)
        show(temp)
        
        t_old = temp
        h_old = hum
        p_old = press                      
        time.sleep(sec_nap)       
       #from subprocess import call
       #call("sudo shutdown -h" now, shell=True)
except KeyboardInterrupt:
    sys.exit(0)