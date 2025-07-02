import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# Create I2C bus using default SCL (GPIO3) and SDA (GPIO2)
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BME280 over I2C
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# Optional: adjust sea-level pressure for altitude calibration
bme280.sea_level_pressure = 1013.25

print("Reading BME280 every 10 seconds. Press Ctrl+C to stop.")

try:
    while True:
        temp = bme280.temperature
        hum = bme280.relative_humidity
        pres = bme280.pressure
        alt = bme280.altitude

        print(f"Temp: {temp:.2f} °C | Humidity: {hum:.2f}% | Pressure: {pres:.1f} hPa | Altitude: {alt:.2f} m")
        time.sleep(10)

except KeyboardInterrupt:
    print("Stopped by user.")
