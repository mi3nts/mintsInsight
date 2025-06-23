
# Mints Insight  
**INSIGHT** – *IoT Networked Sensing Instructional Guide for Hands-on Training*

---

## MINTS Project Checklist 
- Download All Relavant Data Sheets
- Note down power and data communication requirments
- Note down the each sensor measurments and note it on a yaml file 
    - Eg: BME280
            - temperature (C)
            - humidity (%)
            - pressure (mbar)
            - dewPoint (C)
-            
  


## MINTS Project Requirements

Each project assigned should follow the folder structure below:

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
├── sensorDefinitions
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
│       └── ina219Reader.py  
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

For the sensor descritions the yaml file should follow this format 
``` yaml 
BME280:
  description: "Bosch BME280 Environmental Sensor"
  protocol: "I2C"
  address: "0x76"  # or "0x77", depending on the board wiring
  measurements:
    temperature:
      unit: "°C"
      description: "Ambient temperature"
    humidity:
      unit: "%"
      description: "Relative humidity"
    pressure:
      unit: "mbar"
      description: "Barometric pressure"

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

> ✅ **Reminder:**  
> Ensure your code is well-documented, filenames are descriptive, and updates are committed to GitHub regularly following MINTS conventions.
