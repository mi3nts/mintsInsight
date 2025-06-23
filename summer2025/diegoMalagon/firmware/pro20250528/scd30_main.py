from scd30_i2c import SCD30  # Use the I2C-based library
import time

# Initialize the sensor (adjust parameters if needed by the new library)
sensor = SCD30(i2c_bus=5)  # or just SCD30() if it auto-detects the bus

while True:
    if sensor.get_data_ready():
        time.sleep(0.05)  # Allow sensor to prep the data

        try:
            co2, temp, rh = sensor.read_measurement()
            print(f"CO2: {co2:.2f} ppm")
            print(f"Temp: {temp:.2f} °C")
            print(f"Humidity: {rh:.2f} %")
            print()
        except ValueError as e:
            print(f"[ERROR] CRC mismatch while reading measurement: {e}")
    else:
        print("Data not ready yet.")
    
    time.sleep(2)
