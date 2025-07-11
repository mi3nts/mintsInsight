import csv
import os
from datetime import datetime

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
