import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
from csv_logger import log_to_csv


# ---------- BME280 Sensor Setup ----------
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25  # Optional: adjust for your location

# ---------- CSV File Setup i.e  Define your CSV structure ----------
CSV_FILE = "bme280_data.csv"
FIELDS = ["Timestamp", "Temperature", "Humidity", "Pressure", "Altitude"]

# ---------- Main Loop ----------
print("Reading BME280 data every 10 seconds and logging to CSV... Press Ctrl+C to stop.")

try:
    while True:
        temp = bme280.temperature
        hum = bme280.relative_humidity
        pres = bme280.pressure
        alt = bme280.altitude

        print(f"🌡 Temp: {temp:.2f} °C | 💧 Humidity: {hum:.2f}% | ⚖ Pressure: {pres:.1f} hPa | 🏔 Altitude: {alt:.2f} m")

        # Prepare data dictionary
        data = {
            "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "Temperature": temp,
            "Humidity": hum,
            "Pressure": pres,
            "Altitude": alt
        }

        # Now Applying Log to CSV Funtion
        log_to_csv(CSV_FILE, FIELDS, data)

        time.sleep(10)

except KeyboardInterrupt:
    print("✅ Data logging stopped by user.")
