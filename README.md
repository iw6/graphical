# graphical
To run any of these files RPi needs Python 3 and Matplotlib.
Graphical representation of real time data using matplotlib + data logging. 

1. MightyOhm geiger counter (mightyohm.com) via RPi serial data GPIO pins. Geiger.png shows backgroung radiation data. This programs will also work with other computers with matplotlib installed (or RPi) via USB using a FTI Friend USB connector (Amazon.com) and modifing the script as outlined in geiger.py

2. SenseAir CO2 using S8 CO2 sensor (CO2meter.com), its 5v supply taken from RPi. Room.png shows CO2 levels in a bedroom overnight and the exquisite sensitivity of this detector. Running on RPi zero takes some time to load and time values to appear on the x-axis. Wait a while for things to happen!

3. The programs bme680ani.py and bme280ani.py from Pimoroni graphically animate in real time, updated in a 12 hour period, atmospheric temperature/humidity/pressure - (and resistance for bme680). The results are shown in bme680ani.tif and bme280ani.tif.  These programs show the data but the graphical representation is lost on power failure (or a change of battery) 

4. air_logger.py uses pandas re-read the existing file and show it on screen - while continuing to log data. Example in air_logger.jpg shows data for a 12h run. Deleting air_logger.csv allows data aquisition to be started from new.

5.  Adafruit bme688 has 7 connections. sck goes to scl and sdi goes to sda on RPi as well as the power and ground lines. Adafruit board has the advantage on a green led  to show that all is well. sudo i2cdetect -y 1 will show if the i2c connections are OK. Ploughing through their obfuscating Adafruit web site, the required library       download for RPi is: sudo pip3 install adafruit-circuitpython-bme680. adafruitbme688.jpg shows data for a 12h run. 
 
6. Inkyphat.  If the pins on RPi GPIO header extender, (Pimoroni.com) ususally used by BME680 (3.3v 2,3,4,& GND) are bent through 90 degrees, the sensor can be attached with jumper wires and Inkyphat can use the remaining (upright) pins. inkybme680.py updates temperature, humidity and pressure every hour plus readings from the previous hour - shown in inky.jpg. This program and graphical (air_logger.py) are combined in inky_air.py  --   after power outage, previous readings are restored to graph and inkyphat.  

