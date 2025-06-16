from ina219Driver import INA219DRIVER
import time

ina1 = INA219DRIVER(busnum=5, address=0x40)
ina2 = INA219DRIVER(busnum=5, address=0x41)

while True:
    print("INA1")
    ina1.read()
    print("INA2")
    ina2.read()
    time.sleep(1)
