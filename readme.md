
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
