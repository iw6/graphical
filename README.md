# graphical
To run any of these files RPi needs Python 3 and Matplotlib.
Graphical representation of real time data using matplotlib + data logging. 

1. MightyOhm geiger counter (mightyohm.com) via RPi serial data GPIO pins. Geiger.png shows backgroung radiation data. This programs will also work with other computers with matplotlib installed (or RPi) via USB using a FTI Friend USB connector (Amazon.com) and modifing the script as outlined in geiger.py

2. SenseAir CO2 using CO2 sensor(CO2meter.com). Room.png shows CO2 levels in a bedroom overnight and the exquisite sensitivity of this detector. Running on RPi zero takes some time to load and time values to appear on the x-axis. Wait a while for things to happen!

3. The programs bme680ani.py and bme280ani.py graphically animate in real time, updated in a 12 hour period, atmospheric temperature/humidity/pressure - (and resistance for bme680). The results are shown in bme680ani.tif and bme280ani.tif 
