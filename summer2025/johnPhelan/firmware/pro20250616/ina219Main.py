from ina219Driver import INA219DRIVER
import time

ina = INA219DRIVER(busnum=5, address=0x40)

while True:
    ina.read()
    time.sleep(1)
