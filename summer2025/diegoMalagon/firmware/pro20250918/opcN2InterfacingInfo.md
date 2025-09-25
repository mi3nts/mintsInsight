# OPC-N2 SPI Command Reference

This document describes the SPI protocol and firmware commands for the **Alphasense OPC-N2 Optical Particle Counter** (firmware v18).  

---

## SPI Interface

- **Mode:** SPI Mode 1 (CPOL=0, CPHA=1)  
- **Word length:** 8 bits  
- **Clock speed:** 300–750 kHz (recommended ~500 kHz)  
- **Slave:** OPC-N2 (no tri-state MISO, so cannot share SPI bus)  
- **Handshake:**  
  - Master sends 1-byte command.  
  - OPC-N2 responds with `0xF3` (ACK).  
  - Data bytes follow depending on command.  
- **Delays:**  
  - Wait ~10 ms after command byte before reading data.  
  - Wait ~10 µs between subsequent data bytes.  

---

## Power / Control Commands

| Command (Hex) | Bytes Out | Response | Description |
|---------------|-----------|----------|-------------|
| `0x03 0x00`   | –         | `0xF3`   | Fan **ON** + Laser **ON** |
| `0x03 0x01`   | –         | `0xF3`   | Fan **OFF** + Laser **OFF** |
| `0x03 0x04`   | –         | `0xF3`   | Fan **ON only** |
| `0x03 0x05`   | –         | `0xF3`   | Fan **OFF only** |
| `0x03 0x02`   | –         | `0xF3`   | Laser **ON only** |
| `0x03 0x03`   | –         | `0xF3`   | Laser **OFF only** |

---

## DAC / Power Control

| Command | Example | Response | Notes |
|---------|---------|----------|-------|
| `0x42 0x01 <val>` | `0x42 0x01 0xC8` | `0xF3` | **Set Laser Power** (`<val>` = 0–255) |
| `0x42 0x00 <val>` | `0x42 0x00 0xFF` | `0xF3` | **Set Fan Power** (`<val>` = 0–255) |
| `0x13`            | –       | `0xF3` then 4 status bytes | **Read Fan/Laser status** + DAC values |

**Status response (after 0x13):**  
1. `FanON` (0 or 1)  
2. `LaserON` (0 or 1)  
3. `FanDACVal` (0–255)  
4. `LaserDACVal` (0–255)  

---

## Data Retrieval

| Command | Response | Description |
|---------|----------|-------------|
| `0x30`  | `0xF3` + histogram bytes | **Read histogram** (particle bins + flow/temp/pressure if fitted). Resets counters. |
| `0x32`  | `0xF3` + 12 bytes | **Read PM values**: PM1, PM2.5, PM10 (floats, 4 bytes each). Resets histogram. |

**Example – Read PM Values (0x32):**
```text
Master → 0x32
Slave  → 0xF3
Slave  → PM1 [4 bytes, float]
Slave  → PM2.5 [4 bytes, float]
Slave  → PM10 [4 bytes, float]
