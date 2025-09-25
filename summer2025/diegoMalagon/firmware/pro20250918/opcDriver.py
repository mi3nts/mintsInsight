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

# === OPC COMMANDS ===
cmdPower = 0x03
cmdInfo = 0x3F
cmdSerial = 0x10
cmdFwver = 0x12
cmdStatus = 0x13
cmdHist = 0x30
cmdPm =  0x32

# Command delays (seconds)
_CMD_DELAYS = {
    cmdInfo:   0.05,
    cmdSerial: 0.05,
    cmdFwver:  0.05,
    cmdStatus: 0.05,
    cmdPm:     0.2,
    cmdHist:   0.5,
}

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
def spiTransfer(cmd, rx_bytes=0, delay=None):
    """Send a single-byte command, wait, then read back"""
    if not _initialized:
        raise RuntimeError("opcDriver not initialized. Call init() first.")

    # Pick delay from table if not given
    if delay is None:
        delay = _CMD_DELAYS.get(cmd, 0.05)

    GPIO.output(CS_PIN, GPIO.LOW)
    sleep(0.01)

    spi.xfer2([cmd])       # send command
    sleep(delay)           # wait for device to prepare response

    rx = spi.xfer2([0x00] * (1 + rx_bytes))

    GPIO.output(CS_PIN, GPIO.HIGH)
    return rx


def opcRaw(cmd, rx_bytes):
    """Send a command and return raw payload with mode."""
    resp = spiTransfer(cmd, rx_bytes)
    payload, mode = _validate_frame(resp, cmd, rx_bytes)
    if payload is None:
        # fallback: just use full response
        payload = resp
    return payload, mode

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


def opcOn():
    spiMulti([cmdPower, 0x00])   # Fan + Laser ON
    sleep(1.0)  # let fan/laser stabilize

def opcOff():
    spiMulti([cmdPower, 0x01])   # Fan + Laser OFF

def opcPm():
    payload, mode = opcRaw(cmdPm, 13)
    print("raw PM:", payload, "mode:", mode)
    return payload  # leaving parsing for later

def opcHistogram():
    payload, mode = opcRaw(cmdHist, 86)
    print("raw histogram:", payload, "mode:", mode)
    return payload

def opcInfo():
    resp = spiTransfer(cmdInfo, 60)
    payload, mode = _validate_frame(resp, cmdInfo, 60)
    print("raw info response:", resp, "mode:", mode)
    if payload is None:
        return None
    return decodeASCII(payload)

def opcSerial():
    payload, mode = opcRaw(cmdSerial, 60)
    print("raw serial:", payload, "mode:", mode)
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
