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
    """Send a single-byte command and read back response"""
    if not _initialized:
        raise RuntimeError("opcDriver not initialized. Call init() first.")

    GPIO.output(CS_PIN, GPIO.LOW)
    sleep(0.001)

    spi.xfer2([cmd])             # send command
    sleep(0.01)                  # wait for OPC to prepare data

    rx = spi.xfer2([0x00] * (1 + rx_bytes))  # read ACK/echo + payload

    GPIO.output(CS_PIN, GPIO.HIGH)
    return rx

def spiMulti(tx_bytes, rx_bytes=0):
    """Multi-byte command (ex. power control) + optional readback"""
    if not _initialized:
        raise RuntimeError("opcDriver not initialized. Call init() first.")
    GPIO.output(CS_PIN, GPIO.LOW)
    sleep(0.001)
    spi.xfer2(tx_bytes)  # send bytes
    sleep(0.01)
    rx = spi.xfer2([0x00] * (1 + rx_bytes)) if rx_bytes > 0 else []
    GPIO.output(CS_PIN, GPIO.HIGH)
    return rx

def _validate_frame(resp, cmd, expected_len):
    """
    Normalize response frames:
      - ACK-first: [0xF3, payload...]
      - ACK-last: [payload..., 0xF3]
      - Echo: [cmd, payload...]
    Returns (payload, mode) or (None, reason).
    """
    if not resp:
        return None, "empty"
    if resp[0] == 0xF3:
        return resp[1:], "ack_start"
    if resp[-1] == 0xF3:
        return resp[:-1], "ack_end"
    if resp[0] == cmd:
        return resp[1:], "echo"
    return None, "no_ack"

def decodeASCII(payload):
    """Decode payload into clean ASCII string"""
    return ''.join(chr(b) for b in payload if 32 <= b < 127).strip()

# === OPC COMMANDS ===
cmdPower = 0x03
cmdInfo = 0x3F
cmdSerial = 0x10
cmdFwver = 0x12
cmdStatus = 0x13
cmdHist = 0x30
cmdPm =  0x32

def opcOn():
    spiMulti([cmdPower, 0x00])   # Fan + Laser ON
    sleep(1.0)  # let fan/laser stabilize

def opcOff():
    spiMulti([cmdPower, 0x01])   # Fan + Laser OFF

def opcPm():
    resp = spiTransfer(cmdPm, 12)
    payload, mode = _validate_frame(resp, cmdPm, 12)
    print("raw pm response:", resp, "mode:", mode)
    if payload is None or len(payload) < 12:
        print("No valid PM data")
        return None
    try:
        pm1, pm25, pm10 = struct.unpack('<fff', bytes(payload[:12]))
        return {"PM1": pm1, "PM2.5": pm25, "PM10": pm10}
    except struct.error:
        print("PM unpack failed")
        return None

def opcHistogram():
    resp = spiTransfer(cmdHist, 85)
    payload, mode = _validate_frame(resp, cmdHist, 85)
    print("raw histogram response:", resp, "mode:", mode)
    if payload is None:
        print("No valid histogram data")
        return None

    nBins = 14 if len(payload) < 64 else 16
    bins = []
    for i in range(nBins):
        start = i * 4
        end   = start + 4
        if end <= len(payload):
            bins.append(struct.unpack('<I', bytes(payload[start:end]))[0])
        else:
            bins.append(0)

    sfr   = struct.unpack('<f', bytes(payload[64:68]))[0] if len(payload) >= 68 else 0.0
    temp  = struct.unpack('<f', bytes(payload[68:72]))[0] if len(payload) >= 72 else 0.0
    press = struct.unpack('<f', bytes(payload[72:76]))[0] if len(payload) >= 76 else 0.0
    period= struct.unpack('<f', bytes(payload[76:80]))[0] if len(payload) >= 80 else 0.0

    return {"bins": bins, "SFR": sfr, "Temp": temp, "Press": press, "Period": period}

def opcInfo():
    resp = spiTransfer(cmdInfo, 60)
    payload, mode = _validate_frame(resp, cmdInfo, 60)
    print("raw info response:", resp, "mode:", mode)
    if payload is None:
        return None
    return decodeASCII(payload)

def opcSerial():
    resp = spiTransfer(cmdSerial, 60)
    payload, mode = _validate_frame(resp, cmdSerial, 60)
    print("raw serial response:", resp, "mode:", mode)
    if payload is None:
        return None
    return decodeASCII(payload)

def opcFwver():
    resp = spiTransfer(cmdFwver, 2)
    payload, mode = _validate_frame(resp, cmdFwver, 2)
    print("raw fwver response:", resp, "mode:", mode)
    if payload is None or len(payload) < 2:
        return None
    major, minor = payload[0], payload[1]
    return f"{major}.{minor}"

def opcStatus():
    resp = spiTransfer(cmdStatus, 4)
    payload, mode = _validate_frame(resp, cmdStatus, 4)
    print("raw status response:", resp, "mode:", mode)
    if payload is None or len(payload) < 4:
        return None
    fan_on, laser_on, fan_dac, laser_dac = payload[:4]
    return {"Fan": bool(fan_on), "Laser": bool(laser_on),
            "FanDAC": fan_dac, "LaserDAC": laser_dac}
