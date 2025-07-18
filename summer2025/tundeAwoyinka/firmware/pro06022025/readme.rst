IPS 7100 Sensor Driver
====================

Interfacing a IPS7100 an Intelligent Particle Sensor that measures airborne particulate matter, specifically 
focusing on mass and number concentrations of various particle sizes. It can measure particles as small as 
PM0.1 (particles smaller than 0.1 µm) and includes measurements for PM0.3, PM0.5, PM1, PM2.5, PM5, and PM10 in 
Python 3 using I2C on the Raspberry Pi. Further technical details for the
IPS7100 sensor can be found in the `datasheet
<https://github.com/mi3nts/mintsInsight/blob/main/summer2025/tundeAwoyinka/datasheets/IPS7100/da01IPS7100.pdf>`_
[PDF].

.. image:: https://github.com/mi3nts/mintsInsight/blob/main/summer2025/tundeAwoyinka/datasheets/IPS7100/Ips7100_image.png
  

GPIO pin-outs
-------------
The IPS7100  can use both UART AND I2C and so connecting to the RPi is very straightforward:

IPS7100 to RPi using I2C
^^^^^^^^^
For I2C, the IPS7100 pins are connected to RPi pins as follows:

========== ====== ============ ======== ==============
Board Pin  Name   Remarks      RPi Pin  RPi Function  
========== ====== ============ ======== ==============
1          VIN    +5V Power    Pin-2    3V3           
2          SDA    I/0          Pin-16   GPIO 23 (SDA)           
3          SCL    Clock        Pin-18   GPIO 24 (SCL)  
4          SEL    Select       Pin-6    GND: for I2c
5          GND    Ground       Pin-6    GND
========== ====== ============ ======== ==============

IPS7100 to RPi using UART
^^^^^^^^^
For UART, the IPS7100 pins are connected to RPi pins as follows:

========== ====== ============ ======== ==============
Board Pin  Name   Remarks      RPi Pin  RPi Function  
========== ====== ============ ======== ==============
1          VIN    +5V Power    Pin-2    3V3           
2          SDA    I/O or Data  Pin-16   GPIO 23 (SDA)           
3          SCL    Clock        Pin-18   GPIO 24 (SCL)  
4          SEL    Select       None     None
5          GND    Ground       Pin-6    GND
========== ====== ============ ======== ==============

  
