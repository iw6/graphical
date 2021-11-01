# graphical
To run any of these files RPi needs Python 3 and Matplotlib.
Graphical representation of real time data using matplotlib + data logging. 

1. MightyOhm geiger counter (mightyohm.com) via RPi serial data GPIO pins. Geiger.png shows backgroung radiation data. This programs will also work with other computers with matplotlib installed (or RPi) via USB using a FTI Friend USB connector (Amazon.com) and modifing the script as outlined in geiger.py

2. SenseAir CO2 using S8 CO2 sensor (CO2meter.com), its 5v supply taken from RPi. Room.png shows CO2 levels in a bedroom overnight and the exquisite sensitivity of this detector. Running on RPi zero takes some time to load and time values to appear on the x-axis. Wait a while for things to happen!

3. The programs bme680ani.py and bme280ani.py from Pimoroni graphically animate in real time, updated in a 12 hour period, atmospheric temperature/humidity/pressure - (and resistance for bme680). The results are shown in bme680ani.tif and bme280ani.tif.  These programs show the data but the graphical representation is lost on power failure (or a change of battery) air_logger.py uses pandas to look for and re-read the existing file and show it on screen - while continuing to log data. Example shown in air_logger.csv. Deleting the latter file allows data to be started from new.

4.  Adafruit bme688 has 7 connections. sck goes to scl and sdi goes to sda on RPi as well as the power and ground lines. Adafruit board has the advantage on a green led  to show that all is well. sudo i2cdetect -y 1 will show if the i2c connections are OK. Ploughing through their obfuscating Adafruit web site, the required library       download for RPi is: sudo pip3 install adafruit-circuitpython-bme680. The file adafruitbme688.jpg shows data for a 12h run.  

