#!/usr/bin/python3
#-*- coding:utf-8 -*-

# www.CO2Meter.com  Application Note AN168: Raspberry Pi to SenseAir S8 CO2 Sensor via UART
#Setup:sudo apt-get install python3-matplotlib
#sudo apt-get install -y python3-pandas
# modify file name below in the format('co2-dd-mm-yyyy.csv')

filename=('co2-16-08-2020.csv')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()



fig =plt.figure()
ax1 = fig.add_subplot(1,1,1)

df = pd.read_csv(filename, parse_dates=['Time'])
x = df.Time
y = df.CO2

#get pause time from data
df['Time'] = pd.to_datetime(df['Time'])
df['Time'] = df['Time'].dt.strftime('%H:%M:%S')
s1=(df.iat[0,0])
s2=(df.iat[1,0])
FMT = '%H:%M:%S'
pa = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)

#plot data
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gcf().autofmt_xdate()
ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
ax1.plot(x,y, marker = '.', linewidth=1, color='red')
ax1.tick_params(axis="x",labelrotation =30)
ax1.set_ylabel('(CO\u2082 ppm)')
ax1.set_xlabel('Time')
ax1.set_title(f'Pause={pa} (H:M:S), File name={filename}', fontsize = 10)   
fig.suptitle('SenseAir S8 CO\u2082 monitor',fontsize = 12)
fig.subplots_adjust(bottom= 0.15)
ax1.plot(x,y, marker = '.', linewidth=1, color='red')
plt.show()
