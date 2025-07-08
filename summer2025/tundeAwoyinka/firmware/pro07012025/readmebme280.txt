The code is Interfacing BME 280 with Raspberry Pi for Data Capturing.
The library is adafruit-circuitpython-bme280 library.

In the Raspberry Pi shell, run:
------- sudo pip3 install adafruit-circuitpython-bme280 ------

BME 280 Uses I2C, so for the I²C use: 
----
VIN → 3.3 V

GND → GND

SDA → Pin 3 (standard SDA (GPIO 2)

SCL → Pin 5 (Standard SCL (GPIO 3)
----

To Enable I²C on shell use:
--------  sudo raspi-config -----------
the go to Interface Options → I2C → Enable
