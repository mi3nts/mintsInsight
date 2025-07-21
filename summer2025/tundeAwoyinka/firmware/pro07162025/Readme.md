# COZIR-ahe-1 Co2 sensor Setup with Raspberry pi 

Using a CozIR-AHE-1 CO2 sensor with a Raspberry Pi involves connecting the sensor to the Raspberry Pi via its UART serial interface and then writing code to communicate with it and interpret the data.
Further technical details for the IPS7100 sensor can be found in the datasheet [PDF](https://github.com/mi3nts/mintsInsight/blob/main/summer2025/tundeAwoyinka/datasheets/Co2Sensor/ds01CoZIR_AHE_1.pdf).
and also in [COZIR-A sensor](https://www.digikey.com.au/product-detail/en/gas-sensing-solutions-ltd/COZIR-AH-1/2091-COZIR-AH-1-ND/9952878).

## COZIR-ahe-1 Co2 Sensor Image
![ModuleSetup](https://github.com/mi3nts/mintsInsight/blob/main/summer2025/tundeAwoyinka/datasheets/Co2Sensor/CoZIR.png)

### Connect COZIR to  Raspberry GPIO

Connect COZIR pins 1, 3, 5, 7 to [GPIO pins](https://pinout.xyz/pinout/pin8_gpio14) 1 or 17, 6, 8, 10.

| COZIR Pin | Name |   Remarks    | RPi Pin |  RPi Function |  
|-----------|------|--------------|---------|-------------- 
|  1        |  VIN |  +3.3V Power |  Pin-1  |  3V3          |  
|  3        |  GND |  Ground      |  Pin-6  |  GND          | 
|  5        |  RXD |  Recieve     |  Pin-8  |  GPIO 14 (TXD)|  
|  7        |  TXD |  Transmit    |  Pin-10 |  GPIO 15 (RXD)|

### Raspberry Pi setup

For Headless Raspberry pi setup: [link](https://github.com/mi3nts/mintsInsight/blob/main/summer2025/tundeAwoyinka/datasheets/RaspberryPi/RpiSetup1.md) 

## General guide to Interface COZIR-ahe-1 Co2 with Raspberry pi 
1) Wiring and power
- Connect the CozIR-AHE-1 to the Raspberry Pi's UART pins: GPIO14 (TXD) and GPIO15 (RXD) as shown in the above table.
- Power the sensor: Connect the sensor to the 3.3VDC pin on the Raspberry Pi board for stable operation.
- Ensure proper grounding: Connect the sensor's ground pin to a ground pin on the Raspberry Pi. 

2) Raspberry Pi configuration
- Enable the serial port hardware: Run `sudo raspi-config`, go to "Interfacing Options," select "Serial," and enable the hardware serial port.
- Disable login shell over serial: In the same `raspi-config` menu, ensure that a login shell is not accessible over the serial port to prevent conflicts with the sensor communication.
- Reboot the Raspberry Pi after making these changes.

3) Software setup
- Install necessary libraries: You'll likely need pyserial for serial communication in Python. You can install it using `pip`: `pip install pyserial`.
- Develop a Python script:
- Open the serial port: Use `serial.Serial()` to open the appropriate serial port (e.g., `/dev/ttyS0 or /dev/serial0`) at the correct baud rate (9600 for CozIR sensors).
- Send commands (optional): The CozIR sensor may require commands to set its operating mode or customize its output format. Refer to the CozIR-AHE-1's datasheet or user manual for the specific commands needed.
- Read data: Read data from the serial port. The CozIR sensor outputs CO2 measurements as a string, e.g., "Z ##### z #####\r\n", where "#####" represents the CO2 concentration.
- Parse the data: Extract the CO2 value from the received string and convert it to the desired format (e.g., integer ppm).
- Display or log the data: Print the CO2 concentration to the console, save it to a file, or integrate it into a larger data collection and analysis system.

#### Example Python snippet
This is a simplified example; consult the sensor's documentation and adapt it to your specific needs: 
```
import serial
import time

# Configure the serial port
ser = serial.Serial('/dev/serial0', baudrate=9600, timeout=1)  # Adjust port and baud rate if needed

# Optional: Send commands to the sensor (refer to CozIR documentation)
# ser.write(b'K 2\r\n')  # Example: Set operating mode
# ser.write(b'M 4\r\n')  # Example: Set display mode

try:
    while True:
        # Read a line from the sensor
        line = ser.readline().decode('utf-8').strip()

        # Check if the line contains CO2 data
        if line.startswith('Z'):
            # Parse the CO2 value
            co2_value = int(line.split(' ')[1])

            # Print the CO2 concentration
            print(f"CO2 Concentration: {co2_value} ppm")

        time.sleep(1)  # Wait for a second before reading again

except KeyboardInterrupt:
    print("Exiting...")

finally:
    ser.close()  # Close the serial port when finished

