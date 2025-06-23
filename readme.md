# Mints Insight  
**INSIGHT** – *IoT Networked Sensing Instructional Guide for Hands-on Training*

---

## MINTS Project Checklist 
- Download all relevant datasheets.
- Note down power and data communication requirements.
- Record sensor measurements and document them in a YAML file.
    Sensor descriptions in the YAML file (e.g., `bme280.yaml`) should follow the format shown below:
    ```yaml
    BME280:
      description: "Adafruit BME280 Environmental Sensor Breakout"
      protocol: "I2C"
      address: "0x76"  # Default; 0x77 if SDO is tied to VCC
      voltage_range: "3.3V to 5V (regulated onboard)"
      power_draw: "0.6 mA (typical in normal mode)"
      measurements:
        temperature:
          unit: "°C"
          description: "Ambient temperature"
          accuracy: "±1.0°C"
          range: "-40 to 85°C"
          sampling_rate: "1 Hz"
        humidity:
          unit: "%"
          description: "Relative humidity"
          accuracy: "±3% RH"
          range: "0 to 100% RH"
          sampling_rate: "1 Hz"
        pressure:
          unit: "mbar"
          description: "Atmospheric pressure"
          accuracy: "±1 hPa"
          range: "300 to 1100 hPa"
          sampling_rate: "1 Hz"
    ```

- Define `mintsDefinitions.yaml` for project-specific definitions.
    ```yaml
    dataFolder: "/home/teamlary/mintsData"
    ```

- Create a wiring diagram for the project.
- Create a README for the project: [Sample Readme](https://github.com/mi3nts/mintsInsight/blob/main/exampleProjectReadme.md)
- Develop and test your firmware.
- Verify data is being correctly logged in the `mintsData` folder.

## MINTS Project Requirements

Each project should follow the folder structure below:

```
lakithaWijeratne  
├── datasheets 
│   ├── BME280
│   │   ├── ds01BME280.pdf
│   │   └── ds02BME280.pdf
│   └── INA219
│       ├── ds01INA210.pdf
│       └── ds02INA210.pdf
│
├── sensorDefinitionsMaster
│   ├── bme280.yaml
│   └── ina219.yaml
│   
├── firmware  
│   ├── mintsLib  
│   │   ├── mintsDefinitions.yaml  
│   │   └── commonFirmware.py 
│   └── pro20250528  
│       ├── readme.md  
│       ├── ips7100Reader.py  
│       ├── ina219Reader.py
│       │  
│       └── sensorDefinitions
│           ├── bme280.yaml
│           └── ina219.yaml
│          
│  
├── mintsData  
│   └── 2025  
│       └── 06  
│           └── 13  
│               ├── MINTS_INA219_2025_06_13.csv  
│               └── MINTS_BME280_2025_06_13.csv  
│  
├── res  
│   └── pro20250528  
│       ├── ina219connectionDiagram.drawio  
│       └── ina219connectionDiagram.drawio.png  
│  
└── legacy  
    └── olderFirmware.py  
```

---

## 📝 Folder Descriptions

- **`firmware/mintsLib/`**  
  Contains shared firmware resources such as common definitions and YAML configuration files.

- **`firmware/proYYYYMMDD/`**  
  Project-specific code including sensor reader scripts and documentation.

- **`mintsData/YYYY/MM/DD/`**  
  Daily sensor data logs stored in a structured date hierarchy.

- **`res/proYYYYMMDD/`**  
  Visual documentation such as connection diagrams for each project.

- **`legacy/`**  
  Archive for outdated or experimental firmware code.

---

# 🔌 Wiring Diagram Color Codes

## Primary Wire Colors

| Signal             | Color Icon                                                                                     | Hex Code   | Label |
|--------------------|:----------------------------------------------------------------------------------------------:|------------|-------|
| Power              | <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/F97171.png?raw=true" width="20"/></div> | `#F97171`  | Red   |
| Ground             | <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/000000.png?raw=true" width="20"/></div> | `#000000`  | Black |
| I²C SCL            | <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/FBEC5D.png?raw=true" width="20"/></div> | `#FBEC5D`  | Yellow|
| I²C SDA            | <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/C0C0C0.png?raw=true" width="20"/></div> | `#C0C0C0`  | Grey  |
| RX (w.r.t Master)  | <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/3CD184.png?raw=true" width="20"/></div> | `#3CD184`  | Green |
| TX (w.r.t Master)  | <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/1E81B0.png?raw=true" width="20"/></div> | `#1E81B0`  | Blue  |

---

## 🎨 Additional Color Options

| Color Icon                                                                                     | Hex Code   | Label  |
|:----------------------------------------------------------------------------------------------:|------------|--------|
| <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/66BEB2.png?raw=true" width="20"/></div> | `#66BEB2`  | Teal   |
| <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/F99192.png?raw=true" width="20"/></div> | `#F99192`  | Pink   |
| <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/8AD6CC.png?raw=true" width="20"/></div> | `#8AD6CC`  | Aqua   |
| <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/3D6647.png?raw=true" width="20"/></div> | `#3D6647`  | Forest |
| <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/000080.png?raw=true" width="20"/></div> | `#000080`  | Navy   |
| <div align="center"><img src="https://github.com/mi3nts/instructables/blob/master/mintsThemes/icons/FBA85B.png?raw=true" width="20"/></div> | `#FBA85B`  | Orange |

---

### Fonts

- [Montserrat](https://github.com/mi3nts/instructables/tree/master/mintsThemes/Montserrat%2CSankofa_Display/Montserrat)
- [Sankofa_Display](https://github.com/mi3nts/instructables/tree/master/mintsThemes/Montserrat%2CSankofa_Display/Sankofa_Display)

### Logos

- [MINTS Logos](https://github.com/mi3nts/instructables/tree/master/mintsThemes/logos)

You can find more information in the mintsThemes GitHub repository.

---

> ✅ **Reminder:**  
> Ensure your code is well-documented, filenames are descriptive, and updates are committed to GitHub regularly following MINTS conventions.
