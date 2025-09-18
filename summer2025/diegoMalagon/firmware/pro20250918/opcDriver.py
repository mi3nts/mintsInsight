import spidev
import RPi.GPIO as GPIO
from time import sleep
import struct

# === CONFIG ===
CS_PIN = 8  # GPIO8 = CE0
SPI_BUS = 0
SPI_DEV = 0
SPI_SPEED = 500000  # Hz

# === GLOBALS ===
spi = None
_initialized = False

# === INIT ===
def init():
    global spi, _initialized
    if _initialized:
        return  # avoid re-init
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CS_PIN, GPIO.OUT)
    GPIO.output(CS_PIN, GPIO.HIGH)
    spi = spidev.SpiDev()
    spi.open(SPI_BUS, SPI_DEV)
    spi.no_cs = True
    spi.max_speed_hz = SPI_SPEED
    spi.mode = 1
    _initialized = True

def cleanup():
    global spi, _initialized
    if spi:
        spi.close()
    GPIO.cleanup()
    _initialized = False

# === HELPERS ===
def spi_transfer(cmd, rx_bytes=0):
    if not _initialized:
        raise RuntimeError("opcDriver not initialized. Call init() first.")
    GPIO.output(CS_PIN, GPIO.LOW)
    sleep(0.001)
    tx = [cmd] + [0x00] * rx_bytes
    rx = spi.xfer2(tx)
    GPIO.output(CS_PIN, GPIO.HIGH)
    return rx

# === OPC COMMANDS ===
CMD_ON = 0x12
CMD_OFF = 0x13
CMD_INFO = 0x3F
CMD_PM = 0x30
CMD_HIST = 0x32

def opc_on():
    spi_transfer(CMD_ON)
    sleep(1)

def opc_off():
    spi_transfer(CMD_OFF)

def opc_info():
    resp = spi_transfer(CMD_INFO, 60)
    return ''.join(chr(b) if 32 <= b < 127 else '.' for b in resp)

def opc_pm():
    resp = spi_transfer(CMD_PM, 12)
    pm1, pm25, pm10 = struct.unpack('<fff', bytes(resp[1:13]))
    return {"PM1": pm1, "PM2.5": pm25, "PM10": pm10}

def opc_histogram():
    resp = spi_transfer(CMD_HIST, 62)
    data = resp[1:]
    bins = []
    for i in range(24):
        lsb = data[2*i]
        msb = data[2*i+1]
        bins.append(msb << 8 | lsb)
    pm1, pm25, pm10 = struct.unpack('<fff', bytes(data[48:60]))
    return {"bins": bins, "PM1": pm1, "PM2.5": pm25, "PM10": pm10}

