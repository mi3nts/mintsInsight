from ina219 import INA219 as SensorINA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

class INA219DRIVER:
    def __init__(self, busnum, address):
        self.busnum = busnum
        self.address = address
        self.sensor = SensorINA219(
            shunt_ohms=SHUNT_OHMS,
            max_expected_amps=MAX_EXPECTED_AMPS,
            address=address,
            busnum=busnum
        )
        self.sensor.configure(self.sensor.RANGE_16V)

    def read(self):
        print("Bus Voltage: %.3f V" % self.sensor.voltage())
        try:
            print("Bus Current: %.3f mA" % self.sensor.current())
            print("Power: %.3f mW" % self.sensor.power())
            print("Shunt Voltage: %.3f mV" % self.sensor.shunt_voltage())
        except DeviceRangeError as e:
            print("Device Range Error:", e)
