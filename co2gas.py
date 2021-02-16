#!/usr/bin/python3
#-*- coding:utf-8 -*-

#see: www.CO2Meter.com  Application Note AN168: Raspberry Pi to SenseAir S8 CO2 Sensor via UART
#setup: install matplotlib. sudo apt-get install python3-matplotlib
#to autostart open file:
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# and add to end of file:
# @sudo /usr/bin/python3 /home/pi/co2gas.py &



import serial
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import strftime
from datetime import datetime
import csv

ser = serial.Serial('/dev/ttyS0',baudrate = 9600, timeout = 0.5)
print (' AN-137: Raspberry Pi to K-30 Via UART\n')
ser.flushInput()

plt.ion()
x = []
y = []

fig, ax = plt.subplots(figsize = (12,12))

filename = '/home/pi/Desktop/ co2-'+ strftime('%d-%m-%Y') +'.csv'
fieldnames = ['Time', 'CO2']
with open(filename, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
def write_gas(gas):    
    with open (filename, 'a') as csv_file:        
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={'Time':time,'CO2':gas}                                          
        csv_writer.writerow(info)
        x.append(time) 
        y.append(gas)       

def graph(gas):
    ax.clear()
    # find the highest co2 value and add 100 to autoscale y-axis 
    hico2 = int(max(y) + 100)
    
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M:%S') for d in x]  
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))     
    ax.plot(a,y, marker = '.', linewidth = 1, color='red')
    ax.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax.tick_params(axis='x',labelrotation = 30)
    ax.set_ylabel('CO\u2082 (ppm)',fontsize = 12)
    ax.set_ylim(400,hico2)
    ax.set_xlabel('Time', fontsize = 12)
    ax.set_title(f' Last update {t_time}  Pause ~ {round((pa+20)/60,2)}min. Path + file name: {filename}', fontsize = 12)
    fig.suptitle('SenseAir S8 CO\u2082 monitor',fontsize = 14)    
    
while True:
    #Enter pause time pa seconds
    pa = 900
    
    ser.flushInput()    
    ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25')
    plt.pause(2)
    resp = ser.read(7)
    high = (resp[3])
    low = (resp[4])
    gas = (high*256) + low
    time = strftime('%d-%m-%Y %H:%M:%S')
    t_time = (time[10:])
    write_gas(gas)
    graph(gas)   
    plt.savefig('/home/pi/Desktop/CO2.png', bbox_inches = 'tight')
    plt.pause(pa)