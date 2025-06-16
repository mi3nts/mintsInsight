from ina219 import INA219
from ina219 import DeviceRangeError
import smbus2

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

class INA219:
    def __init__(self, port=5, address=0x40):
        self.port = port
        self.address = address
        self.data = None

    def read():
        ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, 5)
        ina.configure(ina.RANGE_16V)

        print("Bus Voltage: %.3f V" % ina.voltage())
        try:
            print("Bus Current: %.3f mA" % ina.current())
            print("Power: %.3f mW" % ina.power())
            print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resistor
            print(e)