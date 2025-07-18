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
2          SDA    I/0 or Data  Pin-16   GPIO 23 (SDA)           
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

  
Pre-requisites
--------------
1. Remove I2C from Blacklist: Run the command:: 
    sudo nano /etc/modprobe.d/raspi-blacklist.conf 
and comment out the I2C line by adding a hash # before it.

2. Load I2C Kernel Module using::
   $ dmesg | grep i2c
  [    4.925554] bcm2708_i2c 20804000.i2c: BSC1 Controller at 0x20804000 (irq 79) (baudrate 100000)
  [    4.929325] i2c /dev entries driver

or::

  $ lsmod | grep i2c
  i2c_dev                 5769  0
  i2c_bcm2708             4943  0
  regmap_i2c              1661  3 snd_soc_pcm512x,snd_soc_wm8804,snd_soc_core

If you have no kernel modules listed and nothing is showing using ``dmesg`` then this implies
the kernel I2C driver is not loaded. Enable the I2C as follows:

#. Run ``sudo raspi-config``
#. Use the down arrow to select ``9 Advanced Options``
#. Arrow down to ``A7 I2C``
#. Select **yes** when it asks you to enable I2C
#. Also select **yes** when it asks about automatically loading the kernel module
#. Use the right arrow to select the **<Finish>** button
#. Select **yes** when it asks to reboot

After rebooting re-check that the ``dmesg | grep i2c`` command shows whether
I2C driver is loaded before proceeding.

Optionally, to improve permformance, increase the I2C baudrate from the default
of 100KHz to 400KHz by altering ``/boot/config.txt`` to include::

  dtparam=i2c_arm=on,i2c_baudrate=400000

Then reboot.

Then add your user to the i2c group::

  $ sudo adduser pi i2c

Install some packages::

  $ sudo apt-get install i2c-tools python-pip

Next check that the device is communicating properly (if using a rev.1 board,
use 0 for the bus not 1)::

  $ i2cdetect -y 1
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- --
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    70: -- -- -- -- -- -- 76 --

Installing the Python Package
-----------------------------
From the bash prompt, enter::
  
  $ sudo python3 setup.py install

Install SMbus Library and tools 
^^^^^^^^^^^^
Install I2C Tools and Python SMBus Library, just do::

  $ sudo apt-get install i2c-tools
  $ sudo apt-get install python-smbus

Optional
^^^^^^^^^^
To Grant User Access: Add the Pi user to the I2C access group by running::
  $ sudo adduser pi i2c
