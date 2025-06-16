from ina219Driver import INA219
import time

ina219 = INA219()

while True:
    ina219.read()
    time.sleep(1)