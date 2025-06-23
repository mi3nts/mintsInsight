from smbus2 import SMBus
import time
from ina219 import INA219, DeviceRangeError
from datetime import datetime
from function import DataUtils  # Make sure class name matches your file

class SMBusINA219:
    def __init__(self, bus=5, address=0x40, csv_file='INA219dataLog.csv'):
        self.bus_num = bus
        self.address = address
        self.ina = INA219(shunt_ohms=0.1, address=self.address, busnum=self.bus_num)
        self.ina.configure()

        # CSV fieldnames
        self.fieldnames = ['timestamp', 'bus_voltage', 'power', 'shunt_voltage', 'current']
        self.csv_logger = DataUtils(csv_file, self.fieldnames)

    def read(self):
        """
        Read INA219 sensor values and log to CSV.
        """
        try:
            bus_voltage = self.ina.bus_voltage()
            power = self.ina.power()
            shunt_voltage = self.ina.shunt_voltage()
            current = self.ina.current()

            print(f"Bus Voltage: {bus_voltage:.3f} V")
            print(f"Power: {power:.3f} mW")
            print(f"Shunt Voltage: {shunt_voltage:.3f} mV")
            print(f"Current: {current:.3f} mA")

            # Format data for CSV
            data = {
                'timestamp': datetime.utcnow().isoformat(),
                'bus_voltage': bus_voltage,
                'power': power,
                'shunt_voltage': shunt_voltage,
                'current': current
            }

            self.csv_logger.write_to_csv(data)

        except DeviceRangeError as e:
            print(f"[INA219 Range Error] {e}")
