#!/usr/bin/python3
#-*- coding:utf-8 -*-

# See: www.CO2Meter.com  Application Note AN168: Raspberry Pi to SenseAir S8 CO2 Sensor via UART
# Enables existing data file to be plotted after power failure/shutdown
# Must run on Python 3 and have network access to get time
# Install matplotlib: sudo apt-get install python3-matplotlib
# Install pandas:sudo apt-get install python3-pandas

# In RPi "Preferences - RPi Configuration - Interfaces" make sure Serial Port is Enabled & Serial Console: Disabled

# To autostart 
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# add to end of file:
# @sudo /usr/bin/python3 /home/pi/CO2mm.py &

import os.path
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import matplotlib.dates as mdates
import serial
from datetime import datetime

ser = serial.Serial('/dev/ttyS0',baudrate = 9600, timeout = 0.5)
print (' AN-137: Raspberry Pi to K-30 Via UART\n')

print ('Date       Time      CO2')

if os.path.exists('/home/pi/Desktop/CO2mm.csv'):   
    filename =('/home/pi/Desktop/CO2mm.csv')
    fieldnames = ['Time', 'CO2']         
    with open (filename, 'a') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)        
else:
    filename = ('/home/pi/Desktop/CO2mm.csv')     
    fieldnames = ['Time', 'CO2']
    with open (filename, 'w') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
    
# Create figure
plt.style.use('seaborn')
fig, axs = plt.subplots(1, 1, figsize=(12, 12))
fig.subplots_adjust(bottom = 0.13)
(ax1) = axs
x = []
y = []    


def animate(i, x, y):
## Read Time & CO2
    x_time = (dt.datetime.now().strftime('%d-%m-%Y %H:%M'))          
    ser.flushInput()    
    ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25')
    plt.pause(2)
    resp = ser.read(7)
    high = (resp[3])
    low = (resp[4])
    CO2 = (high*256) + low

# Write to file     
    with open (filename, 'a') as csv_file:       
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Time": x_time,"CO2": CO2}                                          
        csv_writer.writerow(info)        
    print('{0:1},   {1:1}'.format(x_time, CO2))   
    x.append(x_time)
    y.append(CO2)   
    
#read file
    df = pd.read_csv(filename)
    x = df['Time']
    y = df['CO2']        
    
# Rolling time window of 72 data frame points (for a 12 hour graph)
    x = x[-72:]
    y = y[-72:]
    
# Get times when low & high CO2 values occur. (Only one value allowed)
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time'] = df['Time'].dt.strftime('%H:%M on %d-%m-%y')
   
    lowCO2 =(df['CO2'].min())
    index =(df[df['CO2'] ==lowCO2].index.values)
    if len(index)> 0:
        loc = (index)
        le = ((len(index)-1))
        low = (loc[le])
        lCO2=(df.iat[low,1])
        lt=(df.iat[low,0])                
    else:
        lCO2 =(df["CO2"].min())
        lt=(df.iat[index,0])
        
        
    highCO2 =(df['CO2'].max())
    index =(df[df['CO2'] ==highCO2].index.values)
    if len(index)> 0:
        loc = (index)
        le = ((len(index)-1))
        high = (loc[le])
        hCO2=(df.iat[high,1])
        ht=(df.iat[high,0])   
    else:
        hCO2 =(df['CO2'].max()) 
        ht=(df.iat[index,0])     
        
# Format graph  
    nowtime = (dt.datetime.now().strftime('%a %b %d %Y at %H:%M'))
    ax1.clear()
    fig.suptitle('Air Carbon Dioxide',fontsize = 16,fontweight='bold')
    ax1.set_title(f'Last high {hCO2} (ppm) at {ht} (d-m-y) \n Last low {lCO2} (ppm) at {lt} (d-m-y) \n Updated: {nowtime}, Sleep time = {nap} min, file = /home/pi/Desktop/CO2mm.csv') 
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  %d-%m-%y'))
    ax1.plot(a, y, marker = 'o', linewidth=2, color='blue')
    ax1.set_xlabel('Time - Date', fontsize=14,fontweight='bold')
    ax1.set_ylabel('Carbon dioxide (ppm)', fontsize=14,fontweight='bold')
    plt.setp( ax1.xaxis.get_majorticklabels(), rotation = -45, ha="left" ,rotation_mode="anchor")    
   
    plt.savefig('/home/pi/Desktop/CO2mm'+'.jpg')
# Set sleep time (min)    
nap = 10

ani = animation.FuncAnimation(fig, animate, fargs=(x, y), interval= nap*60000)
plt.show()
