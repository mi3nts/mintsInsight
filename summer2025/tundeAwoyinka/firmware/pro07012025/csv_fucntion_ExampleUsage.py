from csv_logger import log_to_csv
import time

# Define your CSV structure
CSV_FILE = "bme280_log.csv"
FIELDS = ["Timestamp", "Temperature", "Humidity", "Pressure", "Altitude"]

# Fake sensor data (replace with real BME280 readings)
temp = 25.2
hum = 53.7
pres = 1012.8
alt = 58.3

# Create dictionary with current reading
data = {
    "Timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
    "Temperature": temp,
    "Humidity": hum,
    "Pressure": pres,
    "Altitude": alt
}

# Log it
log_to_csv(CSV_FILE, FIELDS, data)
