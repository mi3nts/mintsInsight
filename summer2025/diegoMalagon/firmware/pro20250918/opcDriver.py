# summer2025/diegoMalagon/firmware/pro20250918/opcDriver.py
# OPC-N2 Driver for Raspberry Pi
# Uses SPI interface via spidev and RPi.GPIO libraries

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
def spiTransfer(cmd, rx_bytes=0):
    """Single-byte command + readback"""
    if not _initialized:
        raise RuntimeError("opcDriver not initialized. Call init() first.")
    GPIO.output(CS_PIN, GPIO.LOW)
    sleep(0.001)
    tx = [cmd] + [0x00] * rx_bytes
    sleep(0.01)
    rx = spi.xfer2(tx)
    GPIO.output(CS_PIN, GPIO.HIGH)
    return rx

def spiMulti(tx_bytes, rx_bytes=0):
    """Multi-byte command (ex. power control) + optional readback"""
    if not _initialized:
        raise RuntimeError("opcDriver not initialized. Call init() first.")
    GPIO.output(CS_PIN, GPIO.LOW)
    sleep(0.001)
    rx = spi.xfer2(tx_bytes + [0x00] * rx_bytes)
    GPIO.output(CS_PIN, GPIO.HIGH)
    return rx

# === OPC COMMANDS ===
cmdPower = 0x03
cmdInfo = 0x3F
cmdSerial = 0x10
cmdFwver = 0x12
cmdStatus = 0x13
cmdHist = 0x30
cmdPm =  0x32

def opcOn():
    # Fan + Laser ON
    spiMulti([cmdPower, 0x00])   # send 0x03

def opcOff():
    # Fan + Laser OFF
    spiMulti([cmdPower, 0x01])

def opcPm():
    resp = spiTransfer(cmdPm, 13)  # ACK + 12 bytes
    print("raw pm response:", resp)
    if resp[0] != 0xF3:
        raise RuntimeError("No ACK from OPC pm data command")
    pm1, pm25, pm10 = struct.unpack('<fff', bytes(resp[1:13]))
    return {"PM1": pm1, "PM2.5": pm25, "PM10": pm10}

def opcHistogram():
    resp = spiTransfer(cmdHist, 86)  # ACK + 85 data bytes
    if resp[0] != 0xF3:
        raise RuntimeError("No ACK from OPC histogram command")

    data = resp[1:]
    bins = []
    nBins = 14 if len(data) < 64 else 16
    for i in range(nBins):
        start = i*4
        end   = start + 4
        bins.append(struct.unpack('<I', bytes(data[start:end]))[0])

    sfr   = struct.unpack('<f', bytes(data[64:68]))[0]
    temp  = struct.unpack('<f', bytes(data[68:72]))[0]
    press = struct.unpack('<f', bytes(data[72:76]))[0]
    period= struct.unpack('<f', bytes(data[76:80]))[0]

    return {"bins": bins, "SFR": sfr, "Temp": temp, "Press": press, "Period": period}
def opcInfo():
    """Read information string (60 ASCII chars)"""
    resp = spiTransfer(cmdInfo, 60)
    if resp[0] != 0xF3:
        raise RuntimeError("No ACK from OPC info command")
    return ''.join(chr(b) if 32 <= b < 127 else '.' for b in resp[1:])

def opcSerial():
    """Read serial number string (60 ASCII chars)"""
    resp = spiTransfer(cmdSerial, 60)
    if resp[0] != 0xF3:
        raise RuntimeError("No ACK from OPC serial command")
    return ''.join(chr(b) if 32 <= b < 127 else '.' for b in resp[1:])

def opcFwver():
    """Read firmware version (2 bytes: major, minor)"""
    resp = spiTransfer(cmdFwver, 2)
    if resp[0] != 0xF3:
        raise RuntimeError("No ACK from OPC firmware version command")
    major, minor = resp[1], resp[2]
    return f"{major}.{minor}"
def opcStatus():
    resp = spiTransfer(cmdStatus, 4)
    if resp[0] != 0xF3:
        raise RuntimeError("No ACK from OPC status command")
    fan_on, laser_on, fan_dac, laser_dac = resp[1:5]
    return {"Fan": bool(fan_on), "Laser": bool(laser_on),
            "FanDAC": fan_dac, "LaserDAC": laser_dac}



