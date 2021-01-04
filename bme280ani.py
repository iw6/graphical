#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Based on Pimoroni BME280 examples
#https://github.com/pimoroni/bme280-python
#Must have network access to get time

# In terminal:
#    sudo pip install pimoroni-bme280 smbus
#    git clone https://github.com/pimoroni/bme280-python
#    cd bme280-python
#    sudo ./install.sh
#reboot
#    sudo chmod 755 bme280ani.py

#To autostart 
#sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
#add to end of file:
#@sudo /usr/bin/python3 /home/pi/bme280ani.py &

import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('bmh')

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
 
print("\n\nConnection to BME280 via I2C successful")
                       
gridsize =(2,2)
fig = plt.figure(figsize = (12,12))

ax1 = plt.subplot2grid(gridsize,(0,0),colspan =1, rowspan=1,)
ax2 = plt.subplot2grid(gridsize,(0,1))
ax3 = plt.subplot2grid(gridsize,(1,0),colspan =2, rowspan=1)

x = []
x1 = []
y = []                                                            
y1 = []
y2 = []

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Write file header
filename = "/home/pi/Desktop/ bme280-"+(dt.datetime.now().strftime('%d-%m-%Y'))+'.csv'
fieldnames =["Date", "Time", "Temp", "RH", "Press"]
with open(filename, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

def animate(i, x, x1, y, y1, y2):
# Read BME280 data           
    temp = round(bme280.get_temperature(),1)
    hum = round(bme280.get_humidity(),1)
    press= round(bme280.get_pressure(),1)
    
# Write to file   
    with open (filename, 'a') as csv_file:
        x_time = (dt.datetime.now().strftime('%H:%M'))
        x_date = dt.datetime.now().strftime('%d-%m-%Y')
        csv_writer = csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Date": x_date, "Time": x_time,"Temp": temp, "RH": hum, "Press": press}                                          
        csv_writer.writerow(info)      
        
    x.append(x_time)
    x1.append(x_date)
    y.append(temp)
    y1.append(hum)
    y2.append(press)    
    
# Rolling time window of 12 data points
    x = x[-12:]
    y = y[-12:]
    y1 = y1[-12:]
    y2 = y2[-12:]       
    
# Format plot
    ax1.clear()
    nowtime = (dt.datetime.now().strftime('%a %b %d at %H:%M'))   
    fig.suptitle(f'BME280. Last reading: Temperature, {temp} (\u00B0C), Relative Humidity, {hum} (%), Pressure, {press} (hPa), \n\n Last update: {nowtime}, Sleep time = {nap} min, File name = {filename}', fontsize = 12 )
    ax1.set(ylabel= "Temperature (\u00B0C)", title = "Temperature");           
    ax1.plot(x, y, marker = '.', linewidth=1, color='red')
    ax1.set_xticklabels(x, rotation = 30, ha='right')
    
    ax2.clear()
    ax2.set(ylabel='RH (%)', title = 'Relative Humidity');
    ax2.plot(x, y1,marker = '.', linewidth=1, color='green')
    ax2.set_xticklabels(x, rotation = 30, ha='right')

    ax3.clear()
    ax3.plot(x, y2, marker = '.', linewidth=1, color='blue')
    ax3.set(ylabel='Pressure (hPa)', xlabel = 'Time', title = 'Pressure');  
    ax3.set_xticklabels(x, rotation = 30, ha='right')    
    plt.subplots_adjust( hspace=0.3)                                                  
    plt.savefig('/home/pi/Desktop/bme280ani'+'.tif', bbox_inches = 'tight')
    
#set sleep time (nap)in minutes
nap = 60 #minutes

ani = animation.FuncAnimation(fig, animate, fargs=(x, x1,y, y1, y2), interval = nap*60000)
plt.show()