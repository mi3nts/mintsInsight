# opcTestRead.py
import opcDriver as opc
from time import sleep

def main():
    opc.init()
    opc.opcOn()

    try:
        serial = opc.opcSerial()
        print("Serial:", serial)

        print("Press Ctrl+C to stop...")
        while True:
            pm = opc.opcPm()
            print("PM:", pm)

            hist = opc.opcHistogram()
            if hist:
                print("Histogram Bins:", hist["bins"])
            else:
                print("Histogram: None")

            sleep(2)

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        opc.opcOff()
        opc.cleanup()
        print("Device turned off and GPIO cleaned up.")

if __name__ == "__main__":
    main()
