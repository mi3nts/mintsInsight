import spidev
import struct
import time

# open SPI
spi = spidev.SpiDev()
spi.open(0, 0)             # bus 0, device 0
spi.max_speed_hz = 500000  # OPC-N3 works up to 2MHz
spi.mode = 1               # OPC-N3 uses SPI mode 1 (CPOL=0, CPHA=1)

# ---- Device Info ----
def opc_info():
    CMD_INFO = 0x3F
    resp = spi.xfer2([CMD_INFO] + [0x00]*59)  # expect 60 bytes back
    return bytes(resp[1:]).decode("ascii", errors="ignore").strip()

# ---- Power On ----
def opc_on():
    CMD_ON = 0x03
    spi.xfer2([CMD_ON])

# ---- Power Off ----
def opc_off():
    CMD_OFF = 0x02
    spi.xfer2([CMD_OFF])

# ---- PM Data (PM1, PM2.5, PM10) ----
def opc_pm():
    CMD_PM = 0x32
    resp = spi.xfer2([CMD_PM] + [0x00]*12)  # 13 bytes total
    # First byte is echo of command, next 12 are floats
    pm1, pm25, pm10 = struct.unpack_from("<fff", bytes(resp[1:]))
    return {"PM1": pm1, "PM2.5": pm25, "PM10": pm10}

# ---- Histogram (24 bins + other data) ----
def opc_histogram():
    CMD_HIST = 0x30
    resp = spi.xfer2([CMD_HIST] + [0x00]*63)  # ~64 byte response
    data = bytes(resp[1:])
    bins = struct.unpack_from("<24H", data, 0)  # 24 unsigned shorts
    return {"bins": bins}
