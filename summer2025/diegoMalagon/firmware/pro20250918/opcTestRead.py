import opcDriver as opc
from time import sleep

def main():
    opc.init()
    opc.opc_on()
    try:
        print("Device Info:", opc.opc_info())
        for i in range(5):
            pm = opc.opc_pm()
            print(f"Reading {i+1}: {pm}")
            hist = opc.opc_histogram()
            print(f"Histogram Bins: {hist['bins']}")
            sleep(2)
    finally:
        opc.opc_off()
        opc.cleanup()
        print("Device turned off.")

if __name__ == "__main__":
    main()
