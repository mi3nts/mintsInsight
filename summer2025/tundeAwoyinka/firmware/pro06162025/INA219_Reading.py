import time
from ina219 import INA219

# Constants
SHUNT_OHMS = 0.1  # default value used in most INA219 modules

# Initialize both sensors on I2C bus 1 (Note: change busnum if needed)
ina1 = INA219(SHUNT_OHMS, address=0x40, busnum=5)
ina2 = INA219(SHUNT_OHMS, address=0x41, busnum=5)

# Configure sensors
ina1.configure()
ina2.configure()

print("Reading from INA219 sensors every 10 seconds. Press Ctrl+C to stop.")

try:
    while True:
        # Sensor 1 readings
        v1 = ina1.voltage()
        c1 = ina1.current()
        p1 = ina1.power()

        # Sensor 2 readings
        v2 = ina2.voltage()
        c2 = ina2.current()
        p2 = ina2.power()

        print(f"\n[Sensor 1] Voltage: {v1:.2f} V | Current: {c1:.2f} mA | Power: {p1:.2f} mW")
        print(f"[Sensor 2] Voltage: {v2:.2f} V | Current: {c2:.2f} mA | Power: {p2:.2f} mW")

        time.sleep(10)

except KeyboardInterrupt:
    print("Stopped by user.")