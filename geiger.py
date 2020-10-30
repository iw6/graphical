#!/usr/bin/python3
#-*- coding:utf-8 -*-

# Raspberry pi set up:
# RPi Desktop-Preferences/RPi Configuration/Interfaces/Serial Port enable
# RPi Terminal- sudo nano /boot/cmdline.txt  Remove console-serial0,115300
# Install matplotlib. sudo apt-get install python3-matplotlib

# Two ways to connect to MightyOhm (mightyohm.com)

# 1. Using three jumper leads to RPi gpio pins
# Colours shown in the figure on page 3, https://mightyohm.com/blog/2012/02/tutorial-geiger-counter-data-logging/: Connect
# MightyOhm J7 pin 1 (black) to RPi pin 6 (Gnd) (Colours shown in the figure on page 3 in web site above)
# MightyOhm J7 pin 4 (Rx orange) to RPi pin 8 (Tx)
# MightyOhm J7 pin 5 (Tx yellow) to RPi pin 10 (Rx)
# See raspberrypi.org/magpi Issue 67, Bill Ballard, Simple Pi Geiger Counter Display

#2. Using FTDI Friend USB adapter(Amazon)
# To make it available, plug it in and in RPi terminal: 
# sudo chmod -R 777 /dev/ttyUSB0
# Change  line 31 to: ser = serial.Serial("/dev/ttyUSB0",baudrate =9600, timeout = 0.5)
# Method #2 will also work with with non-Rasperry Pi computers running Ubuntu with matplotlib installed

import serial
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from time import strftime
from datetime import datetime
import csv

ser = serial.Serial("/dev/ttyUSB0",baudrate =9600, timeout = 0.5)
print (" MightyOhm to Raspberry Pi3 Via UART\n")
# If this does not print, serial interface is not working

plt.ion

x = []
y = []

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


filename = "cpm-"+ strftime('%d-%m-%Y %H:%M:%S')+".csv"


fieldnames =["Time", "cpm"]
with open(filename, 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    
def write_cpm(cpm):    
    with open (filename, 'a') as csv_file:        
        csv_writer= csv.DictWriter(csv_file,fieldnames=fieldnames)        
        info={"Time":time,"cpm":cpm}                                          
        csv_writer.writerow(info)
        x.append(time) 
        y.append(cpm)       

def graph(cpm):
    ax1.clear()  
    a = [datetime.strptime(d,'%d-%m-%Y %H:%M:%S') for d in x]  
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))     
    ax1.plot(a,y, marker = '.', linewidth=1, color='red')
    ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax1.tick_params(axis ="x",labelrotation =30)
    ax1.set_ylabel('Radiation (cpm)', fontsize = 12)
    ax1.set_ylim(0,50)
    ax1.set_xlabel('Time',fontsize = 12)
    ax1.set_title(f' Approximate dose: {usv} uSv/Hr. File name: {filename}',fontsize = 11)
    fig.suptitle('MightyOhm radiation monitor',fontsize = 12)
    fig.subplots_adjust(bottom= 0.15)
    
while True:          
    lin=ser.readline()  
    length = len(lin)        
    if length == 37:
        word = lin.decode('utf-8').split(',')
        cpm = int(word[3])             
        usv = word[5]
        time = strftime('%d-%m-%Y %H:%M:%S')
        write_cpm(cpm)
        graph(cpm)
        plt.pause(1)                  
