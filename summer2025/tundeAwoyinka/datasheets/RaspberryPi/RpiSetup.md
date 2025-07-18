# Raspberry Pi setup commands

```sh
startx
ifconfig
sudo nano /etc/network/interfaces 
sudo ifconfig
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git

# Setup some Python stuff
sudo apt-get install python-dev python-serial python-requests python-setuptools python-pip

sudo apt-get install arduino

git clone http://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

# WebIOPi, see:
# https://code.google.com/p/webiopi/wiki/INSTALL
wget http://webiopi.googlecode.com/files/WebIOPi-0.6.0.tar.gz
tar xvzf WebIOPi-0.6.0.tar.gz
cd WebIOPi-0.6.0
sudo ./setup.sh
sudo update-rc.d webiopi defaults

# Make new WebIOPi interface
sudo mkdir garage
cd garage
sudo mkdir html
sudo mkdir python
sudo nano /home/pi/garage/python/script.py
sudo nano /home/pi/garage/html/index.html
sudo nano /etc/webiopi/config
cd garage/html/
sudo wget http://favicon-generator.org/download/2014-08-24/bbc050e1363034113d97e432ff640ebd.ico
sudo mv bbc050e1363034113d97e432ff640ebd.ico favicon.ico
sudo nano /etc/webiopi/config

# Add SSH Key to Github
ls -al ~/.ssh
ssh-keygen -t rsa -C "david.bradway@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
sudo apt-get install xclip
xclip -sel clip < ~/.ssh/id_rsa.pub

ssh-add ~/.ssh/id_rsa
ssh-add -l
cat ~/.ssh/id_rsa.pub
git clone git@bitbucket.org:davidbradway/garageweb.git
git config --global user.email "david.bradway@gmail.com"
git config --global user.name "David Bradway"
git status
git commit -m "add html and python code for first working version of garage opener"
git push -u origin --all
git help branch
git checkout -b macro_one_click

# Add a git submodule to a current project
git submodule add git@github.com:tdicola/rpi_ws281x.git rpi_ws281x

mkdir repos
cd repos/
mkdir garage
cd garage/
git init
cp ../../garage/* . -rf
git add .
git status
touch README.md
nano README.md 

git clone git@bitbucket.org:davidbradway/garageweb.git
ls ~/.ssh
ssh-keygen
ssh-agent /bin/bash

git add .
git commit -m "add sequence button, update script"
git help merge
git checkout master
git pull origin master
git merge macro_one_click
git push origin master
git show
git help branch
git branch macro_one_click -d
git log
git add .
git status
git commit -m "update README to new function of sequence button"
git push origin master

sudo pip install feedparser
sudo easy_install -U distribute
sudo pip install RPi.GPIO

cat <<! > raspi-gmail.py
#!/usr/bin/env python
import RPi.GPIO as GPIO, feedparser, time
DEBUG = 1
USERNAME = "" # just the part before the @ sign, add yours here
PASSWORD = ""
MAIL_CHECK_FREQ = 10       # check mail interval wait [sec]
GPIO.setmode(GPIO.BCM)
GARAGE = 0
GPIO.setup(GARAGE, GPIO.OUT)
                           # my unread messages never goes to zero, yours might
NEWMAIL_OFFSET = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])
while True:
    newmails = int(feedparser.parse("https://" + USERNAME + ":" + PASSWORD +"@mail.google.com/gmail/feed/atom/garage")["feed"]["fullcount"])
    if DEBUG:
        print "There were", newmails, "commands received!"
    if newmails > NEWMAIL_OFFSET:
        print "garage move"
        GPIO.output(GARAGE, False)
        time.sleep(1)
        GPIO.output(GARAGE, True)
        NEWMAIL_OFFSET = newmails
    else:
        NEWMAIL_OFFSET = newmails
    time.sleep(MAIL_CHECK_FREQ)
!

chmod +x raspi-gmail.py
sudo ./raspi-gmail.py 

sudo cp raspigmail.sh /etc/init.d/
sudo chmod 755 /etc/init.d/raspigmail.sh 
sudo /etc/init.d/raspigmail.sh start
sudo /etc/init.d/raspigmail.sh status
sudo update-rc.d raspigmail.sh defaults
ls -l /etc/rc?.d/*raspigmail.sh


# Try to configure Digispark on Raspberry Pi
wget http://sourceforge.net/projects/digistump/files/DigisparkArduino-Linux32-1.0.4-May19.tar.gz/download
mkdir temp
mv download temp/download.tar.gz
cd temp/
tar xzvf download.tar.gz 



# Clean up Garagedoor project
## take down the CRON job
sudo crontab -e
## Stop the raspigmail.sh process
sudo service raspigmail.sh status
sudo service raspigmail.sh stop
sudo service raspigmail.sh status
sudo update-rc.d -f raspigmail.sh remove
sudo /etc/init.d/raspigmail.sh status

# Try NeoPixels on RPi
## https://learn.adafruit.com/neopixels-on-raspberry-pi?view=all
sudo apt-get install build-essential python-dev git scons swig
git clone https://github.com/tdicola/rpi_ws281x.git
cd rpi_ws281x
scons
cd python
sudo python setup.py install

sudo reboot

# Backup RPi
dmesg
lsblk
sudo dd if=/dev/sdb | gzip > image.gz
