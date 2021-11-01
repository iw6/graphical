#!/usr/bin/python3
#-*- coding:utf-8 -*-

# Enables existing data to be plotted after power failure/shutdown
# Must run on Python 3 and have network access to get time
# Heavily based on pimoroni.com bme680 software
# In terminal: run pi@raspberrypi:~ $ curl https://get.pimoroni.com/bme680 | bash
# Install matplotlib: sudo apt-get install python3-matplotlib
# Install pandas:sudo apt-get install python3-pandas


# To autostart 
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# add to end of file:
# @sudo /usr/bin/python3 /home/pi/air_logger.py &

import bme680
import os.path
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import matplotlib.dates as mdates

from datetime import datetime
sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)

print("\n\nConnection to BME688 via I2C successful")
print ('Time    Date,     Temp,   RH,    Press, Res')

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

if os.path.exists('/home/pi/Desktop/air_logger.csv'):
    filename = '/home/pi/Desktop/air_logger.csv'
    fieldnames = ['Time', 'Temp', 'RH', 'Press','Res']                         
    with open (filename, 'a') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)         
else:
    filename = '/home/pi/Desktop/air_logger.csv'
    fieldnames = ['Time', 'Temp', 'RH', 'Press',  'Res']
    with open (filename, 'w') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()

def animate(i, x, y, y1, y2, y3):
# Read BME680 data
    x_time = (dt.datetime.now().strftime('%d-%m-%Y %H:%M'))
    sensor.get_sensor_data()         
    temp = round((sensor.data.temperature),1)
    hum = round(sensor.data.humidity,1)   
    press = round(sensor.data.pressure,1)
    res = round((sensor.data.gas_resistance/1000),1)       
    
# Write to file     
    with open (filename, 'a') as csv_file:       
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Time": x_time,"Temp": temp, "RH": hum, "Press": press, "Res": res}                                          
        csv_writer.writerow(info)
        
    x.append(x_time)
    y.append(temp)
    y1.append(hum)
    y2.append(press)
    y3.append(res)
       
    data = pd.read_csv(filename)
    x = data['Time']
    y = data['Temp']
    y1 = data['RH']
    y2 = data['Press']
    y3 = data['Res']
        
# Rolling time window of 12 data points
    x = x[-12:]
    y = y[-12:]
    y1 = y1[-12:]
    y2 = y2[-12:]
    y3 = y3[-12:]   
    print('{0:1}, {1:1},   {2:1},  {3:0}, {4:0}'.format(x_time,temp,hum,press,res))
    
# Format plot  
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
    plt.savefig('/home/pi/Desktop/air_logger'+'.jpeg', bbox_inches = 'tight')

nap = 60

ani = animation.FuncAnimation(fig, animate, fargs=(x, y, y1, y2, y3), interval= nap*60000)
plt.show()  