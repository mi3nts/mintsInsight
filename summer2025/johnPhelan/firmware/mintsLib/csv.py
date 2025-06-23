from datetime import datetime, timezone
import time
import os
import csv

def _write_header(writer, dataFirstRow):
    writer.writeheader()

def write_to_csv(dataFirstRow=None, data=None, fileName=None):
    if dataFirstRow is None or data is None or fileName is None:
        print("Missing arguments: header, data, or fileName")
        return

    dirPath = '../../mintsData/'
    fullPath = os.path.join(dirPath, fileName)

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

    fileExists = os.path.isfile(full_path)

    with open(fullPath, mode='a', newline='') as csv_file:
        fieldnames = list(dataFirstRow.keys())
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if not fileExists:
            _write_header(writer, dataFirstRow)

        for row in data:
            writer.writerow(row)

    print(f"Appended data to {fullPath}")
