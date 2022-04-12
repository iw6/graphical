#!/usr/bin/python3
#-*- coding:utf-8 -*-

# Enables existing df frame to be plotted after power failure/shutdown
# Must run on Python 3 and have network access to get time
# Program is for red/black phat. Adjust line 40 for other colours
# In terminal: curl https://get.pimoroni.com/bme680 | bash
# Install matplotlib: sudo apt-get install python3-matplotlib
# Install pandas:sudo apt-get install python3-pandas
# Heavily based on Pimoroni Inky pHAT and BME680 examples 
# curl http://get.pimoroni.com/inky | bash

# To autostart 
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# add to end of file:
# @sudo /usr/bin/python3 /home/pi/inky_temp.py &

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
print ('Date    Time,     Temp,   RH,     Press,      Res')

if os.path.exists('/home/pi/Desktop/temp_hum.csv'):   
    filename =('/home/pi/Desktop/temp_hum.csv')
    fieldnames = ['Time', 'Temp', 'RH', 'Press', 'Res']         
    with open (filename, 'a') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)        
else:
    filename = ('/home/pi/Desktop/temp_hum.csv')     
    fieldnames = ['Time', 'Temp', 'RH', 'Press', 'Res']
    with open (filename, 'w') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
    
# Create figure
fig, ax1 = plt.subplots(1, 1, figsize=(12, 12))
fig.subplots_adjust(bottom = 0.13)
ax2 = ax1.twinx()

x = []
y = []                                                            
y1 = []
y2 = []
y3 = []

def animate(i, x, y, y1, y2, y3):
# Read BME680 df
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

    x.append(x_time)
    y.append(temp)
    y1.append(hum)
    y2.append(press)
    y3.append(res)
      
# df from pd.read_csv(filename)
    df = pd.read_csv(filename)
    x = df['Time']
    y = df['Temp']
    y1 = df['RH']
    y2 = df['Press']
    y3 = df['Res']  
    
# Rolling time window of 96 df points (24 hours)
    x = x[-96:]
    y = y[-96:]
    y1 = y1[-96:]
    y2 = y2[-96:]
    y3 = y3[-96:]
    
# Get low & high pressures and times and make sure only one value
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time'] = df['Time'].dt.strftime('%H:%M on %d-%m-%y')
   
    lowp =(df["Temp"].min())
    index =(df[df['Temp'] ==lowp].index.values)
    if len(index)>0:
        loc = (index)
        le = (len(index)-1)
        low = (loc[le])
        lp=(df.iat[low,1])
        lt=(df.iat[low,0])          
        
    else:
        lt=(df.iat[index,0])
        lp =(df["Temp"].min())
        
    highp =(df["Temp"].max())
    index =(df[df['Temp'] ==highp].index.values)
    if len(index)>0:
        loc = (index)
        le = (len(index)-1)
        high = (loc[le])
        hp=(df.iat[high,1])
        ht=(df.iat[high,0])          
    else:
        ht=(df.iat[index,0])
        hp =(df["Temp"].min())
        
# Format graph  
    nowtime = (dt.datetime.now().strftime('%a %b %d %Y at %H:%M'))
    ax1.clear()  
    fig.suptitle('Air Temperature and Relative Humidity',fontsize = 16,fontweight='bold')
    ax1.set_title(f'Last high {hp} (\u00B0C) at {ht} (d-m-y) \n Last low {lp} (\u00B0C) at {lt} (d-m-y) \n Updated: {nowtime}, Sleep time = {nap} min, file = /home/pi/Desktop/temp_hum.csv')    
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  %d-%m-%y'))
    ax1.plot(a, y, marker = '.', linewidth=2, color='red', label='Temperature')
    ax1.set_xlabel('Time - Date', fontsize=14,fontweight='bold')
    ax1.set_ylabel('Temperature (\u00B0C)', fontsize=14,fontweight='bold',color='red')
# ax2.clear() 
    ax2.set_ylabel('Relative Humidity (%)',fontsize=14,fontweight='bold', color='green')    
    ax2.plot(a, y1, marker = '.', linewidth=2, color='green',label='Humidity')  
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  %d-%m-%y'))  
    plt.setp( ax1.xaxis.get_majorticklabels(), rotation = -45, ha="left" ,rotation_mode="anchor")      
    plt.savefig('/home/pi/Desktop/temp_hum'+'.jpg')
    
# Set sleep time (min)    
nap = 15
ani = animation.FuncAnimation(fig, animate, fargs=(x, y, y1, y2, y3), interval= nap*60000)
plt.show()  