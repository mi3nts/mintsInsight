import opcDriver as opc
from time import sleep

def main():
    opc.init()
    opc.opcOn()
    sleep(2)  # warm up

    print("Info:", opc.opcInfo())
    print("Serial:", opc.opcSerial())

    print("Status:", opc.opcStatus())

    print("PM:", opc.opcPm())   # with debug print

        
    opc.opcOff()
    opc.cleanup()
    print("Device turned off.")

if __name__ == "__main__":
    main()
# summer2025/diegoMalagon/firmware/pro20250918/opcDriver.py