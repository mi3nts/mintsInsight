# Raspberry Pi setup

### Headless Raspberry pi setup
To set up a Raspberry Pi headlessly (without a monitor, keyboard, or mouse), you'll need to preconfigure the OS image with network settings and enable SSH. Then, you can access it remotely via SSH from another computer on the same network. 

### Here's a step-by-step guide:
1) Download and Install Raspberry Pi Imager: 
Download the [Raspberry Pi Imager](https://www.raspberrypi.com/software) for your operating system.
Install it like any other application.

2) Choose Operating System and SD Card: 
Open Raspberry Pi Imager.
Click "Choose OS" and select the desired Raspberry Pi OS (e.g., Raspberry Pi OS Lite).
Click "Choose SD Card" and select your SD card.

3) Configure Headless Setup: 
- #### Enable SSH:
Click on the gear icon (Advanced options) in Raspberry Pi Imager. Enable SSH and set a hostname and password for your Raspberry Pi. You can also configure your WiFi settings here. 
- #### Alternatively, manually create files: 
SSH: Create an empty file named "ssh" (without any extension) in the `/boot` directory of the SD card. 
WiFi: Create a file named `wpa_supplicant.conf` in the `/boot` directory and add your WiFi network details (country code, SSID, and password)

You can also watch this [video](https://www.youtube.com/watch?v=aG3hmzW03cs&t=335s) to see the process of creating files for SSH and WiFi

4) Write the Image: 
Click "Write" to write the OS image to the SD card.
Wait for the process to complete.

5) Boot Headless and Connect:
Insert the SD card into your Raspberry Pi. 
Power on the Raspberry Pi. 
Wait for it to boot up and connect to your WiFi network. 
Use a tool like nmap to find the IP address of your Raspberry Pi on the network. 
Use SSH to connect to your Raspberry Pi using the username, hostname (or IP), and password you configured

This [video](https://www.youtube.com/watch?v=m6aS9YF-0xo&t=294s) shows how to find the Raspberry Pi's IP address and connect via SSH

Example:
If you set the hostname to "my-rpi" and the username to "pi", you would SSH using: `ssh pi@my-rpi.local` (or `ssh pi@<your_pi_ip_address>`). 


### SD Card setup

Download [Raspbian](https://www.raspberrypi.org/downloads/raspbian/), flash to SD card with [Etcher](https://www.balena.io/etcher/), re-mount boot drive. 

### Wifi, ssh, gpu_mem

```
touch /Volumes/boot/ssh
cp raspi/wpa_supplicant.conf /Volumes/boot/
```

config.txt

```
enable_uart=1
dtparam=i2c_arm=on
dtparam=i2s=on
dtparam=spi=on
```

Memory link: https://www.raspberrypi.org/documentation/configuration/config-txt/memory.md

### Hostname

Update these files:

sudo nano /etc/hostname
sudo nano /etc/hosts

### Password

passwd 

### Serial connection / Bluetooth

By default the primary UART is setup with a linux console. Handy for debugging but we want to turn it off and use it for other purposes. 

Update /boot/cmdline.txt and remove console=serial0,115200 console=tty1

(https://www.raspberrypi.org/documentation/configuration/cmdline-txt.md)

This can be disabled - [see docs](https://github.com/raspberrypi/documentation/blob/master/configuration/uart.md#disabling-linuxs-use-of-console-uart)

See `pi3-miniuart-bt` in /boot/overlays/README for info. Also https://raspberrypi.stackexchange.com/questions/45570/how-do-i-make-serial-work-on-the-raspberry-pi3-pi3b-pizerow/45571#45571

```
dtoverlay=pi3-miniuart-bt
core_freq=250
```

These are GPIO 14 (pin 8) (TXD), and 15 (pin 10) (RXD). 3.3v is Pin 1.

### I2C (optional)

http://ozzmaker.com/i2c/

## Python3

Raspbian buster has python 3 `which python3`.

See Raspberry pi documentation on installing python packages: https://www.raspberrypi.org/documentation/linux/software/python.md

```
sudo apt install -y python-pip3
python3 -m pip install --user pyserial
```

## InfluxDB

Install (Stretch)

```
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
```

Start

```
sudo service influxdb start|restart
```

Config 

```
sudo nano /etc/influxdb/influxdb.conf
```

## Grafana

https://grafana.com/docs/installation/debian/
https://grafana.com/grafana/download?platform=arm

*Links (with good examples)*
http://blog.centurio.net/2018/10/28/howto-install-influxdb-and-grafana-on-a-raspberry-pi-3/
https://www.circuits.dk/install-grafana-influxdb-raspberry/

```
wget https://dl.grafana.com/oss/release/grafana_6.3.5_armhf.deb 
sudo dpkg -i grafana_6.3.5_armhf.deb
```

```
sudo systemctl enable grafana-server.service
sudo systemctl start grafana-server
```

## Links
- [Raspberry pi Pin out](https://pinout.xyz)
- Config.txt options: [link](https://www.raspberrypi.com/documentation/computers/getting-started.html#:~:text=To%20set%20your%20Raspberry%20Pi%20up%20headless%2C,need%20the%20following%20additional%20accessories:%20a%20display.)


