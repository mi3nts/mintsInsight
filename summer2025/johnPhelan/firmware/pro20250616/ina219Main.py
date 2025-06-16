from ina219Driver import INA219
import time

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x40, busnum=5)

while True:
    ina.read()
    time.sleep(1)