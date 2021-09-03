#!/usr/bin/python3
#-*- coding:utf-8 -*-
# Must have network access to get time
# Note: scl to adafruit sensor sck and sda to sensor sdi + ground & 3 volts
# Install matplotlib: sudo apt-get install python3-matplotlib
# Give ermission: sudo chmod 755 bme688ani.py
# Install Adafruit libraries: sudo pip3 install adafruit-circuitpython-bme680
# To autostart:sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 
# Add to end of file: @sudo /usr/bin/python3 /home/pi/adafruitbme688.py &
# Line 103 changes time in minutes between readings: eg nap = 60.  

import board
import adafruit_bme680
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep, strftime, time
plt.style.use('ggplot')

i2c = board.I2C()
sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
sensor.seaLevelhPa = 1014.5

# Prime gas sensor
sensor = bme680.BME680()
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(300)

print("\n\nConnection to BME688 via I2C successful")

# Create figure
fig, axs = plt.subplots(2, 2, sharex= True, figsize=(12, 12))
(ax1, ax3), (ax2, ax4) = axs

x = []
x1 = []
y = []                                                            
y1 = []
y2 = []
y3 = []

filename = "/home/pi/Desktop/ pimoronibme688 "+(dt.datetime.now().strftime('%d-%m-%Y %H:%M'))+'.csv'
fieldnames =["Date", "Time", "Temp", "RH", "Press", "Res"]

def animate(i, x, x1, y, y1, y2, y3):

# Read BME688 data           
    temp = round((sensor.temperature),1)
    hum = round(sensor.humidity,1)   
    press = round(sensor.pressure,1)
    res = round((sensor.gas/1000),1)
    alt = round((sensor.altitude),1)
# print('Altitude: {} meters'.format(alt))
    
# Write to file     
    with open (filename, 'a') as csv_file:
        x_time = (dt.datetime.now().strftime('%H:%M'))
        x_date = dt.datetime.now().strftime('%d-%m-%Y')
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Date": x_date, "Time": x_time,"Temp": temp, "RH": hum, "Press": press, "Res": res}                                          
        csv_writer.writerow(info)
        
    x.append(x_time)
    x1.append(x_date)
    y.append(temp)
    y1.append(hum)
    y2.append(press)
    y3.append(res)
    
# Rolling time window of 12 data points
    x = x[-12:]
    x1 = x1[-12:]
    y = y[-12:]
    y1 = y1[-12:]
    y2 = y2[-12:]
    y3 = y3[-12:]

# Format plot
    nowtime = (dt.datetime.now().strftime('%a %b %d at %H:%M'))
    ax1.clear()
    fig.suptitle(f'BME688. Last reading: Temperature, {temp} (\u00B0C), Relative Humidity, {hum} (%), Pressure, {press} (hPa), Resistance, {res} (k\u2126),\n\n Last update: {nowtime}, Sleep time = {nap} min, File name = {filename}')
    ax1.plot(x, y,marker = '.', linewidth=1, color='red')
    ax1.set(ylabel='Temperature (\u00B0C)',  title = 'Temperature');
    
    ax2.clear()
    ax2.plot(x, y2, marker = '.', linewidth=1, color='blue')
    ax2.set(ylabel='Pressure (hPa)', xlabel = 'Time', title = 'Pressure');
    ax2.set_xticklabels(x, rotation = 45, ha='right')
    
    ax3.clear()    
    ax3.plot(x, y1,marker = '.', linewidth=1, color='green')
    ax3.set(ylabel='Relative Humidity (%)', title = 'Relative Humidity')
    
    ax4.clear()
    ax4.plot(x, y3,marker = '.', linewidth=1, color='purple')
    ax4.set_ylim(50,150)
    ax4.set(ylabel='Resistance (k\u2126)', xlabel = 'Time', title = 'Resistance');
    ax4.set_xticklabels(x, rotation = 45, ha='right')   
    plt.savefig('/home/pi/Desktop/adafruitbme688'+'.jpg', bbox_inches = 'tight')
    
#set sleep time (nap)in minutes
nap = 60

ani = animation.FuncAnimation(fig, animate, fargs=(x, x1,y, y1, y2, y3), interval= nap*60000)
plt.show()