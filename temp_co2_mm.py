#!/usr/bin/python3
#-*- coding:utf-8 -*-

# See: www.CO2Meter.com  Application Note AN168: Raspberry Pi to SenseAir S8 CO2 Sensor via UART
# Thanks to Pimoroni.com for bme680 software
# In terminal: curl https://get.pimoroni.com/bme680 | bash

# Enables existing data file to be plotted after power failure/shutdown
# Must run on Python 3 and have network access to get time
# Install matplotlib: sudo apt-get install python3-matplotlib
# Install pandas:sudo apt-get install python3-pandas

# In RPi "Preferences - RPi Configuration - Interfaces" make sure Serial Port is Enabled & Serial Console: Disabled

# To autostart 
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# add to end of file:
# @sudo /usr/bin/python3 /home/pi/temp_co2_mm.py &

import bme680
import os.path
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import matplotlib.dates as mdates
import serial
from datetime import datetime

sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
ser = serial.Serial('/dev/ttyS0',baudrate = 9600, timeout = 0.5)
print ('1. Raspberry pi to AN-137 K-30 via UART')
print('2. Raspberry pi to BME688 via I2C')

print ('\n Date      Time,   Temp,   RH,    Press,     Res      CO2')
x = []
y = []                                                            
y1 = []
y2 = []
y3 = []
y4 = []

if os.path.exists('/home/pi/Desktop/temp_co2_mm.csv'):
    filename = '/home/pi/Desktop/temp_co2_mm.csv'
    fieldnames = ['Time', 'Temp', 'RH', 'Press','Res', 'CO2']                         
    with open (filename, 'a') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)         
else:
    filename = '/home/pi/Desktop/temp_co2_mm.csv'
    fieldnames = ['Time', 'Temp', 'RH', 'Press',  'Res', 'CO2']
    with open (filename, 'w') as csv_file:        
        csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        csv_writer.writeheader()
        
# Create figure
fig, ax1 = plt.subplots(1, 1, figsize=(12, 12))
fig.subplots_adjust(bottom = 0.14)
ax2 = ax1.twinx()

def animate(i, x, y, y1, y2, y3, y4):

# Read Time & BME680 data
    x_time = (dt.datetime.now().strftime('%d-%m-%Y %H:%M'))  
    sensor.get_sensor_data()         
    temp = round((sensor.data.temperature),1)
    hum = round(sensor.data.humidity,1)   
    press = round(sensor.data.pressure,1)
    res = round((sensor.data.gas_resistance/1000),0)        
# Read co2            
    ser.flushInput()    
    ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25')
    plt.pause(2)
    resp = ser.read(7)
    high = (resp[3])
    low = (resp[4])
    co2 = int(high*256) + low
    
# Write to file     
    with open (filename, 'a') as csv_file:       
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Time": x_time,'Temp': temp, 'RH': hum, 'Press': press,'Res': res,'CO2': co2}                                          
        csv_writer.writerow(info)
        
    x.append(x_time)
    y.append(temp)
    y1.append(hum)
    y2.append(press)
    y3.append(res)
    y4.append(co2)
       
    df = pd.read_csv(filename)
    x = df['Time']
    y = df['Temp']
    y1 = df['RH']
    y2 = df['Press']
    y3 = df['Res']
    y4 = df['CO2']
        
# Rolling time window of 48 data points ie 12h for 15 min readings 
    x = x[-48:]
    y = y[-48:]
    y1 = y1[-48:]
    y2 = y2[-48:]
    y3 = y3[-48:]
    y4 = y4[-48:]
    
# Get times for low & high temp then CO2. (Only one value allowed)
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time'] = df['Time'].dt.strftime('%H:%M on %d-%m-%y')   
    high_temp =(df["Temp"].max())
    index =(df[df['Temp'] ==high_temp].index.values)
    if len(index)>0:
        loc = (index)
        le = (len(index)-1)
        high = (loc[le])
        htemp=(df.iat[high,1])
        htime_temp=(df.iat[high,0])          
    else:       
        htemp_temp =(df["Temp"].max())
        htime_temp=(df.iat[index,0])
    
    low_temp =(df["Temp"].min())
    index =(df[df['Temp'] ==low_temp].index.values)
    if len(index)>0:
        loc = (index)
        le = (len(index)-1)
        low = (loc[le])
        ltemp=(df.iat[low,1])
        ltime_temp=(df.iat[low,0])                 
    else:
        ltemp=(df.iat[index,0])
        ltime_temp =(df["Temp"].min())
 
    df['Time'] = pd.to_datetime(df['Time'])
    df['Time'] = df['Time'].dt.strftime('%H:%M on %d-%m-%y')
   
    lowco2 =(df['CO2'].min())
    index =(df[df['CO2'] ==lowco2].index.values)
    if len(index)> 0:
        loc = (index)
        le = ((len(index)-1))
        low = (loc[le])
        lco2=(df.iat[low,5])
        ltime_co2=(df.iat[low,0])                
    else:
        lco2 =(df["CO2"].min())
        ltime_co2=(df.iat[index,0])
        
        
    highco2 =(df['CO2'].max())
    index =(df[df['CO2'] ==highco2].index.values)
    if len(index)> 0:
        loc = (index)
        le = ((len(index)-1))
        high = (loc[le])
        hco2=(df.iat[high,5])
        htime_co2=(df.iat[high,0])   
    else:
        hco2 =(df['CO2'].max()) 
        htime_co2=(df.iat[index,0])      
    print('{0:1}, {1:1},   {2:1},  {3:1},    {4:1},  {5:1}'.format(x_time,temp,hum,press,res,co2))
    
# Format graph   
    ax1.clear() 
    nowtime = (dt.datetime.now().strftime('%a %b %d %Y at %H:%M'))     
    fig.suptitle(f'Air Temperature, {temp} \u00B0C and Carbon dioxide, {co2} ppm, \n  Updated: {nowtime}, Sleep time = {nap} min, file = {filename}',fontsize = 12,fontweight='bold')
    ax1.set_title(f'Temp max {htemp} \u00B0C at {htime_temp}: Temp min {ltemp} \u00B0C at {ltime_temp} \n CO\u2082 max {hco2} ppm at {htime_co2}, CO\u2082 min {lco2} ppm at {ltime_co2}')   
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]    
    ax1.plot(a, y, marker = '.', linewidth=2, color='red')
    ax1.set_xlabel('Time  Date', fontsize=14,fontweight='bold')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation = -45, ha="left" ,rotation_mode="anchor")
    ax1.set_ylabel('Temperature (\u00B0C)', fontsize=14,fontweight='bold',color='red')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  %d-%m-%y'))
    ax2.clear()
    nowtime = (dt.datetime.now().strftime('%a %b %d %Y at %H:%M'))
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M') for d in x]
    ax2.set_ylabel('Carbon dioxide (ppm)',fontsize=14,fontweight='bold', color='blue')    
    ax2.plot(a, y4, marker = '.', linewidth=2, color='blue')  
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M  %d-%m-%y'))           
    plt.savefig('/home/pi/Desktop/temp_co2_mm'+'.jpg')
    
# Set sleep time (min)    
nap = 15

ani = animation.FuncAnimation(fig, animate, fargs=(x, y, y1, y2, y3, y4), interval= nap*60000)
plt.show()
