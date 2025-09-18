import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
import csv
import os
from datetime import datetime

# ---------- CSV Logger Function ----------
def log_to_csv(filename, fieldnames, data_dict):
    """
    Logs a dictionary of data to a CSV file.

    Parameters:
    - filename (str): The path to the CSV file.
    - fieldnames (list): A list of all field/column names.
    - data_dict (dict): A dictionary containing the data to log.
    """
    file_exists = os.path.isfile(filename)
    write_header = not file_exists or os.stat(filename).st_size == 0

    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(data_dict)

# ---------- BME280 Sensor Setup ----------
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
bme280.sea_level_pressure = 1013.25  # Optional: adjust for your location

# ---------- CSV File Setup ----------
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

        # Log to CSV
        log_to_csv(CSV_FILE, FIELDS, data)

        time.sleep(10)

except KeyboardInterrupt:
    print("✅ Data logging stopped by user.")
