#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Must have network access to get time
#Setup 1 in terminal: run pi@raspberrypi:~ $ curl https://get.pimoroni.com/bme680 | bash
#Setup2: install matplotlib. sudo apt-get install python3-matplotlib

#To autostart 
#sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
#add to end of file:
#@sudo /usr/bin/python3 /home/pi/bme680_ani.py &

import bme680
import csv
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep, strftime, time
plt.style.use('bmh')

sensor = bme680.BME680()

sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

print("\n\nConnection to BME680 via I2C successful")

# Create figure
fig, axs = plt.subplots(2, 2, sharex= True, figsize=(12, 12))
(ax1, ax3), (ax2, ax4) = axs  
x = []
x1 = []
y = []                                                            
y1 = []
y2 = []
y3 = []

#Save data

def animate(i, x, x1, y, y1, y2, y3):

# Read BME680 data
    sensor.get_sensor_data()         
    temp = round((sensor.data.temperature),1)
    hum = round(sensor.data.humidity,1)   
    press = round(sensor.data.pressure,1)
    res = round((sensor.data.gas_resistance/1000),1)
    
    
# Write to file
    filename = "/home/pi/Desktop/ bme680_"+(dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))+'.csv'
    fieldnames =["Date", "Time", "Temp", "RH", "Press", "Res"]
    today = dt.datetime.now().strftime('%A')
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
    
# Rolling time window of 8 data points
    x = x[-12:]
    x1 = x1[-12:]
    y = y[-12:]
    y1 = y1[-12:]
    y2 = y2[-12:]
    y3 = y3[-12:]


# Format plot
    nowtime = (dt.datetime.now().strftime('%a %b %d at %H:%M'))
    ax1.clear()
    fig.suptitle(f'BME680. Last reading: Temperature, {temp} (\u00B0C), Relative Humidity, {hum} (%), Pressure, {press} (hPa), Resistance, {res} (k\u2126),\n\n Last update: {nowtime}, Sleep time = {nod} min, File name = {filename}')
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
    ax4.set(ylabel='Resistance (k\u2126)', xlabel = 'Time', title = 'Resistance');
    ax4.set_xticklabels(x, rotation = 45, ha='right')
    
    plt.savefig('/home/pi/Desktop/bme680'+'.tif', bbox_inches = 'tight')
    
#set sleep time (nod)in minutes
nod = 60

ani = animation.FuncAnimation(fig, animate, fargs=(x, x1,y, y1, y2, y3), interval= nod*60000)
plt.show()