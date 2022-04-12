# graphical
To run any of these files RPi needs Python 3 and Matplotlib.
Graphical representation of real time data using matplotlib + data logging. 

1. MightyOhm geiger counter (mightyohm.com) via RPi serial data GPIO pins. Geiger.png shows backgroung radiation data. This programs will also work with other computers with matplotlib installed (or RPi) via USB using a FTI Friend USB connector (Amazon.com) and modifing the script as outlined in geiger.py

2. S8 CO2 sensor (CO2meter.com). The program CO2_mm.py measures atmospheric CO2 usig a serial interface to RPi and records min and max CO2 levels. Works fine with its 5v supply taken from a RPi zero.   Example CO2_mm_jpg is overnight readings in a bedroom.

3. The programs bme680ani.py and bme280ani.py from Pimoroni graphically animate in real time, updated in a 12 hour period, atmospheric temperature/humidity/pressure - (and resistance for bme680). The results are shown in bme680ani.tif and bme280ani.tif.  These programs show the data but the graphical representation is lost on power failure (or a change of battery) 

4. Pimoroni BME688.  air_logger.py uses pandas re-read the existing file and show it on screen - while continuing to log data. Example in air_logger.jpg shows data for a 12h run. Deleting air_logger.csv allows data aquisition to be started from new.

5.  Adafruit bme688 has 7 connections. sck goes to scl and sdi goes to sda on RPi as well as the power and ground lines. Adafruit board has the advantage on a green led  to show that all is well. sudo i2cdetect -y 1 will show if the i2c connections are OK. Ploughing through their obfuscating Adafruit web site, the required library       download for RPi is: sudo pip3 install adafruit-circuitpython-bme680. adafruitbme688.jpg shows data for a 12h run. 
 
6. Pimoroni BME688. Inkyphat.  If the pins on RPi GPIO header extender, (Pimoroni.com) ususally used by BME680 (3.3v 2,3,4,& GND) are bent through 90 degrees, the sensor can be attached with jumper wires and Inkyphat can use the remaining (upright) pins. inkybme680.py updates temperature, humidity and pressure every hour plus readings from the previous hour - shown in inky.jpg. This program and graphical (air_logger.py) are combined in inky_air.py  --   after power outage, previous readings are restored to graph and inkyphat.  

7. Pimoroni BME688. pressure_mm.py plots just pressure and records min max values.  Example pressure_mm.jpg records pressure changes when storm Eugene passed through in Feb 2022.  temp-hum.py plots temperature and humidity changes on one graph with two axis and records min max temperatures over a 24h period.  See Fig temp_hum.jpg
