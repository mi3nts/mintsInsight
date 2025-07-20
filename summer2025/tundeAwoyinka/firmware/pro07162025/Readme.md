# COZIR-ahe-1 Co2 sensor Setup with Raspberry pi 

Using a CozIR-AHE-1 CO2 sensor with a Raspberry Pi involves connecting the sensor to the Raspberry Pi via its UART serial interface and then writing code to communicate with it and interpret the data.
Further technical details for the IPS7100 sensor can be found in the datasheet [PDF](https://github.com/mi3nts/mintsInsight/blob/main/summer2025/tundeAwoyinka/datasheets/Co2Sensor/ds01CoZIR_AHE_1.pdf).
and also in [COZIR-A sensor](https://www.digikey.com.au/product-detail/en/gas-sensing-solutions-ltd/COZIR-AH-1/2091-COZIR-AH-1-ND/9952878).

## COZIR-ahe-1 Co2 Sensor Image
![ModuleSetup](https://github.com/mi3nts/mintsInsight/blob/main/summer2025/tundeAwoyinka/datasheets/Co2Sensor/CoZIR.png)

## Raspberry Pi Setup

### Goals

- Document the process of setting up a raspberry pi from scratch
- Document the appropriate way to run python scripts on a raspberry pi
- Connect and read COZIR vales
- Create a remote python development environment

### Connect COZIR to  Raspberry GPIO

Connect COZIR pins 1, 3, 5, 7 to [GPIO pins](https://pinout.xyz/pinout/pin8_gpio14) 1 or 17, 6, 8, 10 respectively.

| Board Pin | Name |   Remarks    | RPi Pin |  RPi Function |  
|-----------|------|--------------|---------|-------------- 
|  1        |  VIN |  +3.3V Power |  Pin-1  |  3V3          |  
|  3        |  GND |  Ground      |  Pin-6  |  GND          | 
|  5        |  RXD |  Recieve     |  Pi|n-8 |  GPIO 14 (TXD)|  
|  7        |  TXD |  Transmit    |  Pin-10 |  GPIO 15 (RXD)|

