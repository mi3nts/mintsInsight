import csv
from datetime import datetime

class dataUtils:
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
