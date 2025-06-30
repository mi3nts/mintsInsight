import csv
from datetime import datetime, timezone
import os

class dataTools:
    def __init__(self, csv_file, fieldnames):
        """
        Initialize the utility class with target CSV file and column headers.

        :param csv_file: Path to the CSV file.
        :param fieldnames: List of all field names to be used as CSV headers.
        """
        self.csv_file = csv_file
        self.fieldnames = fieldnames

        # Create the file with headers if it doesn't exist
        try:
            with open(self.csv_file, mode='x', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
        except FileExistsError:
            pass  # File already exists, no need to write headers

    def write_to_csv(self, data):
        """
        Write a row of sensor data to the CSV file.

        :param data: Dictionary with keys: 'timestamp', 'bme688', 'ips7100'
        """
        row = {'timestamp': data['timestamp']}
        row.update(data.get('bme688', {}))
        row.update(data.get('ips7100', {}))

        with open(self.csv_file, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(row)

    def storeCSVDataInPath(sensor1_data, sensor2_data, userFolder, filePrefix = 'mints'):
        """
        Write INA219 data from two sensors to a CSV file inside a dated folder structure.
        
        :param sensor1_data: List of sensor 1 readings (e.g., [V, mW, mV, mA])
        :param sensor2_data: List of sensor 2 readings (e.g., [V, mW, mV, mA])
        :param userFolder: select what user folder will be used to store csv file
        :parm filePrefix: (string) write what the first word of the file header will be, pass as string.
        """

        now = datetime.now(timezone.utc)
        year = now.strftime('%Y')
        month = now.strftime('%m')
        day = now.strftime('%d')

        folder_path = os.path.join(userFolder, year, month, day)
        os.makedirs(folder_path, exist_ok=True)

        csv_name = f"{file_prefix}_{year}_{month}_{day}.csv"
        csv_path = os.path.join(folder_path, csv_name)

        # Check if file exists — write header if not
        file_exists = os.path.exists(csv_path)

        with open(csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(['Timestamp', 'Sensor', 'Bus Voltage (V)', 'Power (mW)', 'Shunt Voltage (mV)', 'Bus Current (mA)'])

            timestamp = now.strftime('%Y-%m-%dT%H:%M:%SZ')
            writer.writerow([timestamp, 'Sensor 1'] + sensor1_data)
            writer.writerow([timestamp, 'Sensor 2'] + sensor2_data)
