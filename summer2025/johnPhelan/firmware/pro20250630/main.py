# # testing module for cozir.py

from cozir import Cozir
from collections import deque

sensor = Cozir('/dev/serial0') 
dequeCO2 = deque()

while True:
    currentCO2 = sensor.readCO2()
    currentTemp = sensor.readTemperature()
    currentHumidity = sensor.readHumidity()

    dequeCO2.append(currentCO2)
    print("CO₂:", currentCO2, "ppm")
    print("CO2 deque: ", dequeCO2)
    print("Temperature:", currentTemp, "°C")
    print("Humidity:", currentHumidity, "%")

