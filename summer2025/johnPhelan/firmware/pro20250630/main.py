# # testing module for cozir.py

from cozir import Cozir
from collections import deque

sensor = Cozir('/dev/serial0') 
dequeCO2 = deque()

while True:
    currentUnfilteredCO2 = sensor.readCO2(with_filter=False)
    currentFilteredCO2 = sensor.readCO2(with_filter=True)
    currentTemp = sensor.readTemperature()
    currentHumidity = sensor.readHumidity()
    dequeCO2.append(currentUnfilteredCO2)

    print("CO₂:", currentFilteredCO2, "ppm")
    print("uCO2: ", currentUnfilteredCO2, "ppm")
    print("CO2 deque: ", dequeCO2)
    print("Temperature:", currentTemp, "°C")
    print("Humidity:", currentHumidity, "%")

