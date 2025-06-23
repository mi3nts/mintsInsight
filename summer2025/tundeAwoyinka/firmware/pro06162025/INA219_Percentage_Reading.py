
## Updated Script with Battery Percentage  i.e adding battery percentage estimation based on available power.
# I Estimated battery percentage using:
#V_max: Fully charged voltage (e.g., 4.7V for Li-ion)
#V_min: Empty voltage (e.g., 3.0V for Li-ion)

import time
from ina219 import INA219

# Constants
SHUNT_OHMS = 0.1
V_MAX = 4.2  # Max battery voltage when fully charged
V_MIN = 3.0  # Min battery voltage when considered "empty"

# Initialize INA219 sensors on I2C bus 5
ina1 = INA219(SHUNT_OHMS, address=0x40, busnum=5)
ina2 = INA219(SHUNT_OHMS, address=0x41, busnum=5)

ina1.configure()
ina2.configure()

def calculate_battery_percentage(voltage):
    percentage = ((voltage - V_MIN) / (V_MAX - V_MIN)) * 100
    return max(0, min(percentage, 100))  # clamp between 0 and 100

print("Reading INA219 sensors every 10 seconds with battery percentage...")

try:
    while True:
        # Sensor 1
        v1 = ina1.voltage()
        c1 = ina1.current()
        p1 = ina1.power()
        percent1 = calculate_battery_percentage(v1)

        # Sensor 2
        v2 = ina2.voltage()
        c2 = ina2.current()
        p2 = ina2.power()
        percent2 = calculate_battery_percentage(v2)

        print(f"\n[Sensor 1] Voltage: {v1:.2f} V | Current: {c1:.2f} mA | Power: {p1:.2f} mW | Battery: {percent1:.1f}%")
        print(f"[Sensor 2] Voltage: {v2:.2f} V | Current: {c2:.2f} mA | Power: {p2:.2f} mW | Battery: {percent2:.1f}%")

        time.sleep(10)

except KeyboardInterrupt:
    print("Stopped by user.")
