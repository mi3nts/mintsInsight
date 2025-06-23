
# mintsInsight  
**INSIGHT** – *IoT Networked Sensing Instructional Guide for Hands-on Training*

---

## MINTS Project Requirements

Each project assigned should follow the folder structure below:

```
lakithaWijeratne  
├── firmware  
│   ├── mintsLib  
│   │   ├── mintsDefinitions.yaml  
│   │   └── commonFirmware.yaml  
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

> **Note:**  
> - `firmware/mintsLib` contains shared definitions and firmware logic.  
> - `firmware/proYYYYMMDD` contains project-specific readers and documentation.  
> - `mintsData/YYYY/MM/DD` stores sensor data in timestamped folders.  
> - `res/` contains diagrams and other resources.  
> - `legacy/` contains older or deprecated firmware.

---
