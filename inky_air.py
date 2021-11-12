#!/usr/bin/python3
#-*- coding:utf-8 -*-

# Enables existing data to be plotted after power failure/shutdown
# Must run on Python 3 and have network access to get time
# Program is for red/black phat. Adjust line 40 for other colours
# Heavily based on pimoroni.com bme680 software
# In terminal: curl https://get.pimoroni.com/bme680 | bash
# Install matplotlib: sudo apt-get install python3-matplotlib
# Install pandas:sudo apt-get install python3-pandas
# Heavily based on Pimoroni Inky pHAT 
# curl http://get.pimoroni.com/inky | bash

# Based on Pimoroni Inky pHAT and BME680 examples
# See C. Webster, Make an indoor air-quality sensor, Computer Shopper, Issue 375, May 2019

# To autostart 
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# add to end of file:
# @sudo /usr/bin/python3 /home/pi/inky_air.py &

import bme680
import os.path
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import matplotlib.dates as mdates

from datetime import datetime
from time import strftime
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne
plt.style.use('ggplot')
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

# Set the Inky pHAT colour
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)
font1 = ImageFont.truetype(FredokaOne, 20)
font2 = ImageFont.truetype(FredokaOne, 14)

print("\n\nConnection to BME688 via I2C successful")
print ('Date    Time,     Temp,   RH,     Press,      Res')

if os.path.exists('/home/pi/Desktop/inky_air.csv'):   
    filename =('/home/pi/Desktop/inky_air.csv')
    fieldnames = ['Time', 'Temp', 'RH', 'Press', 'Res']         
    with open (filename, 'a') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)        
else:
    filename = ('/home/pi/Desktop/inky_air.csv')     
    fieldnames = ['Time', 'Temp', 'RH', 'Press', 'Res']
    with open (filename, 'w') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
    
# Create figure
plt.style.use('ggplot')
fig, axs = plt.subplots(2, 2, sharex= True, figsize=(12, 12))
fig.subplots_adjust(bottom = 0.1)
(ax1, ax3), (ax2, ax4) = axs
x = []
y = []                                                            
y1 = []
y2 = []
y3 = []

def animate(i, x, y, y1, y2, y3):
# Read BME680 data
    sensor.get_sensor_data() 
    x_time = (dt.datetime.now().strftime('%d-%m-%Y %H:%M'))          
    temp = round((sensor.data.temperature),1)
    hum = round(sensor.data.humidity,1)   
    press = round(sensor.data.pressure,1)
    res = round((sensor.data.gas_resistance/1000),1)        
# Write to file     
    with open (filename, 'a') as csv_file:       
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Time": x_time,"Temp": temp, "RH": hum, "Press": press, "Res": res}                                          
        csv_writer.writerow(info)
# Lenghth of csv file - read next to last values if they don't exist, set to zero
    data = pd.read_csv(filename)
    le = len(data.index)
    if le > 1:
        t_old = (data.iat[(le-2),1])
        h_old = (data.iat[(le-2),2])
        p_old = (data.iat[(le-2),3])
    else:
        t_old = 0
        h_old = 0
        p_old = 0
 
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
    
    x.append(x_time)
    y.append(temp)
    y1.append(hum)
    y2.append(press)
    y3.append(res)
       
# data from pd.read_csv(filename)   
    x = data['Time']
    y = data['Temp']
    y1 = data['RH']
    y2 = data['Press']
    y3 = data['Res']
    
# Rolling time window of 12 data points
    x = x[-24:]
    y = y[-24:]
    y1 = y1[-24:]
    y2 = y2[-24:]
    y3 = y3[-24:]   
    
# Format 4 graphs  
    nowtime = (dt.datetime.now().strftime('%a %b %d %Y at %H:%M'))
    ax1.clear()
    fig.suptitle(f'BME688. Last reading: Temperature, {temp} (\u00B0C), Relative Humidity, {hum} (%), Pressure, {press} (hPa), Resistance, {res} (k\u2126),\n\n Last update: {nowtime}, Sleep time = {nap} min, File name = {filename}')
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  -%d'))
    ax1.plot(a, y,marker = '.', linewidth=2, color='red')
    ax1.set(ylabel='Temperature (\u00B0C)',  title = 'Temperature');       
    
    ax2.clear()
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  -%d'))
    ax2.plot(a, y2, marker = '.', linewidth=2, color='blue')
    ax2.set(ylabel='Pressure (hPa)', xlabel = 'Time -Date', title = 'Pressure');
    plt.setp( ax2.xaxis.get_majorticklabels(), rotation = -45, ha="left" ,rotation_mode="anchor")    

    ax3.clear()
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  -%d'))
    ax3.plot(a, y1,marker = '.', linewidth=2, color='green')
    ax3.set(ylabel='Relative Humidity (%)', title = 'Relative Humidity')
    
    ax4.clear()
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  -%d'))
    ax4.plot(a, y3,marker = '.', linewidth=2, color='purple')
    ax4.set(ylabel='Resistance (k\u2126)', xlabel = 'Time -Date', title = 'Resistance');
    plt.setp( ax4.xaxis.get_majorticklabels(), rotation = -45, ha="left" ,rotation_mode="anchor")    
    plt.savefig('/home/pi/Desktop/inky_air'+'.jpg', bbox_inches = 'tight')
# Set sleep time (min)    
nap = 60

ani = animation.FuncAnimation(fig, animate, fargs=(x, y, y1, y2, y3), interval= nap*60000)
plt.show()  