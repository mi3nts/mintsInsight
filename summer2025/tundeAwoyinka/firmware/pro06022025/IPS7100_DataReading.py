import serial
import time
from collections import OrderedDict
import csv

# Serial port setup
port = 'COM4'
baud_rate = 115200
ser = serial.Serial(port=port, baudrate=baud_rate, timeout=1)

# Keys Setup 
valid_keys = [
    "PC0.1", "PC0.3", "PC0.5", "PC1.0", "PC2.5", "PC5.0", "PC10",
    "PM0.1", "PM0.3", "PM0.5", "PM1.0", "PM2.5", "PM5.0", "PM10"
]

# Open CSV file
with open('ips7100_dict_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp"] + valid_keys)

    print("Starting data collection every 10 seconds. Press Ctrl+C to stop.")

    try:
        while True:
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Raw data: {raw_line}")

            parts = raw_line.split(',')

            data_dict = OrderedDict()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            data_dict["Timestamp"] = timestamp

            try:
                # To Pair items: key, value
                for i in range(0, len(parts) - 1, 2):  # -1 to avoid stray serial number
                    key = parts[i].strip()
                    value = parts[i + 1].strip()

                    if key in valid_keys:
                        data_dict[key] = float(value)

                # To Ensure all keys are present (incase some could be missing in data)
                for key in valid_keys:
                    data_dict.setdefault(key, None)

                print(data_dict)
                writer.writerow([data_dict["Timestamp"]] + [data_dict[key] for key in valid_keys])
                time.sleep(10)

            except Exception as e:
                print(f"Error parsing line: {e}")

    except KeyboardInterrupt:
        print("Data collection stopped.")
    finally:
        ser.close()
