#!/usr/bin/python3
#-*- coding:utf-8 -*-

#See: www.CO2Meter.com  Application Note AN168: Raspberry Pi to SenseAir S8 CO2 Sensor via UART
#To setup: install matplotlib: sudo apt-get install python3-matplotlib

#To autostart open file:
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# and add to end of file:
# @sudo /usr/bin/python3 /home/pi/co2gas.py &



import serial
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import strftime
from datetime import datetime
import csv

ser = serial.Serial("/dev/ttyS0",baudrate =9600, timeout = 0.5)
print (" AN-137: Raspberry Pi3 to K-30 Via UART\n")
ser.flushInput()

plt.ion()
x = []
y = []

#Enter approximate pause time pa seconds
pa = 6

fig = plt.figure()
ax1 =fig.add_subplot(1,1,1)

#For full screen
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()

filename = "co2-"+ strftime('%d-%m-%Y')+".csv"

fieldnames =["Time", "CO2"]
with open(filename, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
def write_gas(gas):    
    with open (filename, 'a') as csv_file:        
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Time":time,"CO2":gas}                                          
        csv_writer.writerow(info)
        x.append(time) 
        y.append(gas)       

def graph(gas):    
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M:%S') for d in x]
    ax1.clear()    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))     
    ax1.plot(a,y, marker = '.', linewidth=1, color='red')
    ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax1.tick_params(axis="x",labelrotation =30)
    ax1.set_ylabel('(CO\u2082 ppm)')
    ax1.set_ylim(400,1800)
    ax1.set_xlabel('Time')
    ax1.set_title(f' Last update {t_time}  Pause ~ {round((pa+60)/10,2)}min. File name {filename}', fontsize = 10)
    fig.suptitle('SenseAir S8 CO\u2082 monitor',fontsize = 12)
    fig.subplots_adjust(bottom= 0.15)
    
    
while True:    
    ser.flushInput()    
    ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
    plt.pause(2)
    resp = ser.read(7)
    high = (resp[3])
    low = (resp[4])
    gas = (high*256) + low
    time = strftime('%d-%m-%Y %H:%M:%S')
    t_time = (time[10:])
    write_gas(gas)
    graph(gas)
    plt.pause(pa)