import opcDriver as opc
from time import sleep

def main():
    opc.init()
    opc.opcOn()
    sleep(2)  # wait for device to stabilize
    
    print("Device Info:", opc.opcInfo())
    serial = opc.opcSerial()
    if serial:
        print("Serial:", serial)
    else:
        print("Firmware:", opc.opcFwver())
        print("Status:", opc.opcStatus())
    
    for i in range(5):
        print("PM Data:", opc.opcPm())
        print("Histogram:", opc.opcHistogram())
        sleep(2)
    
    opc.opcOff()
    opc.cleanup()
    print("Device turned off.")

if __name__ == "__main__":
    main()
# summer2025/diegoMalagon/firmware/pro20250918/opcDriver.py