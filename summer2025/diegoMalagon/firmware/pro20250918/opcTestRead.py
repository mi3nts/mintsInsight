import opcDriver as opc
from time import sleep

def main():
    opc.init()
    opc.opcOn()
    try:
        print("Device Info:", opc.opcInfo())
        print("Serial No:", opc.opcSerial())
        print("Firmware:", opc.opcFwver())
        print("Status:", opc.opcStatus())
        
        for i in range(5):
            pm = opc.opcPm()
            print(f"Reading {i+1}: {pm}")
            hist = opc.opcHistogram()
            print(f"Histogram Bins: {hist['bins']}")
            sleep(2)
    finally:
        opc.opcOff()
        opc.cleanup()
        print("Device turned off.")

if __name__ == "__main__":
    main()
# summer2025/diegoMalagon/firmware/pro20250918/opcDriver.py