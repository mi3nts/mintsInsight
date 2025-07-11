import smbus2
import bme280
            
# Define I2C port and address
port = 5
address = 0x77 # Default I2C address for BME280 is 0x76

# Initialize I2C bus
bus = smbus2.SMBus(port)

# Load calibration parameters
calibration_params = bme280.load_calibration_params(bus, address)

# Read sensor data
data = bme280.sample(bus, address, calibration_params)

# Print sensor readings
print(f"Temperature: {data.temperature:.2f} °C")
print(f"Pressure: {data.pressure:.2f} hPa")
print(f"Humidity: {data.humidity:.2f} %")




